"""Operating-system integration for Nythsleep."""

import ctypes
import getpass
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Optional


class PlatformError(RuntimeError):
    """Raised when an operation is unavailable or cannot run safely."""


class PowerPlatform:
    """Minimal OS adapter. All actions are local, explicit subprocess calls."""

    name = "unsupported"

    def __init__(self):
        self._inhibitor: Optional[subprocess.Popen] = None

    def require_command(self, command: str) -> str:
        found = shutil.which(command)
        if not found:
            raise PlatformError(f"Required command not found: {command}")
        return found

    def run(self, command: list[str]) -> None:
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as exc:
            raise PlatformError(f"Command failed ({exc.returncode}): {' '.join(command)}") from exc
        except OSError as exc:
            raise PlatformError(f"Could not run {' '.join(command)}: {exc}") from exc

    def start_insomnia(self) -> None:
        raise PlatformError(f"Keep Awake is unsupported on {self.name}.")

    def stop_insomnia(self) -> None:
        if self._inhibitor and self._inhibitor.poll() is None:
            self._inhibitor.terminate()
            try:
                self._inhibitor.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self._inhibitor.kill()
        self._inhibitor = None

    def battery_percentage(self) -> int:
        raise PlatformError(f"Battery monitoring is unsupported on {self.name}.")

    def notify(self, title: str, message: str) -> None:
        return None

    def execute(self, choice: int) -> None:
        raise PlatformError(f"Power actions are unsupported on {self.name}.")


class WindowsPlatform(PowerPlatform):
    name = "Windows"
    _continuous = 0x80000000
    _system_required = 0x00000001
    _display_required = 0x00000002

    def start_insomnia(self) -> None:
        ctypes.windll.kernel32.SetThreadExecutionState(
            self._continuous | self._system_required | self._display_required
        )

    def stop_insomnia(self) -> None:
        ctypes.windll.kernel32.SetThreadExecutionState(self._continuous)

    def battery_percentage(self) -> int:
        class SystemPowerStatus(ctypes.Structure):
            _fields_ = [
                ("ACLineStatus", ctypes.c_byte),
                ("BatteryFlag", ctypes.c_byte),
                ("BatteryLifePercent", ctypes.c_byte),
                ("SystemStatusFlag", ctypes.c_byte),
                ("BatteryLifeTime", ctypes.c_ulong),
                ("BatteryFullLifeTime", ctypes.c_ulong),
            ]

        status = SystemPowerStatus()
        if not ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status)):
            raise PlatformError("Windows could not read battery status.")
        if status.BatteryLifePercent == 255:
            raise PlatformError("No battery is available.")
        return status.BatteryLifePercent

    def notify(self, title: str, message: str) -> None:
        script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$n=New-Object System.Windows.Forms.NotifyIcon; "
            "$n.Icon=[System.Drawing.SystemIcons]::Information; "
            f'$n.BalloonTipTitle="{title.replace(chr(34), chr(39))}"; '
            f'$n.BalloonTipText="{message.replace(chr(34), chr(39))}"; '
            "$n.Visible=$true; $n.ShowBalloonTip(10000); Start-Sleep -Seconds 3"
        )
        try:
            subprocess.Popen(
                ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", script],
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except OSError:
            pass

    def execute(self, choice: int) -> None:
        commands = {
            1: ["shutdown", "/s", "/t", "0"],
            2: ["shutdown", "/r", "/t", "0"],
            4: ["shutdown", "/l"],
        }
        if choice == 3:
            ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)
            return
        self.run(commands[choice])


class LinuxPlatform(PowerPlatform):
    name = "systemd Linux"

    def _loginctl(self, action: str) -> None:
        self.run([self.require_command("loginctl"), action])

    def start_insomnia(self) -> None:
        command = self.require_command("systemd-inhibit")
        self._inhibitor = subprocess.Popen(
            [command, "--what=idle:sleep", "--mode=block", "--why=Nythsleep Keep Awake", "sleep", "infinity"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def battery_percentage(self) -> int:
        capacities = []
        for power_supply in Path("/sys/class/power_supply").glob("BAT*"):
            try:
                capacities.append(int((power_supply / "capacity").read_text().strip()))
            except (OSError, ValueError):
                continue
        if not capacities:
            raise PlatformError("No readable battery found in /sys/class/power_supply.")
        return min(capacities)

    def _current_graphical_session(self) -> str:
        session_id = os.environ.get("XDG_SESSION_ID")
        if not session_id:
            raise PlatformError("No current graphical session detected; refusing logout.")
        output = subprocess.check_output(
            [self.require_command("loginctl"), "show-session", session_id,
             "--property=Name", "--property=Type", "--property=Class", "--property=State", "--value"],
            text=True,
        ).splitlines()
        expected_user = getpass.getuser()
        if len(output) < 4 or output[0] != expected_user or output[1] not in {"x11", "wayland"} or output[2] != "user" or output[3] != "active":
            raise PlatformError("Current session is not active graphical user session; refusing logout.")
        return session_id

    def notify(self, title: str, message: str) -> None:
        command = shutil.which("notify-send")
        if command and os.environ.get("DBUS_SESSION_BUS_ADDRESS"):
            subprocess.Popen([command, title, message], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def execute(self, choice: int) -> None:
        actions = {1: "poweroff", 2: "reboot", 3: "suspend"}
        if choice == 4:
            self.run([self.require_command("loginctl"), "terminate-session", self._current_graphical_session()])
            return
        self._loginctl(actions[choice])


class MacOSPlatform(PowerPlatform):
    name = "macOS"

    def start_insomnia(self) -> None:
        self._inhibitor = subprocess.Popen([self.require_command("caffeinate"), "-dis"])

    def battery_percentage(self) -> int:
        output = subprocess.check_output([self.require_command("pmset"), "-g", "batt"], text=True)
        match = re.search(r"(\d+)%", output)
        if not match:
            raise PlatformError("macOS could not read battery status.")
        return int(match.group(1))

    def notify(self, title: str, message: str) -> None:
        script = f'display notification "{message.replace(chr(34), chr(39))}" with title "{title.replace(chr(34), chr(39))}"'
        subprocess.Popen(["osascript", "-e", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def execute(self, choice: int) -> None:
        commands = {
            1: ["sudo", "shutdown", "-h", "now"],
            2: ["sudo", "shutdown", "-r", "now"],
            3: ["pmset", "sleepnow"],
            4: ["osascript", "-e", 'tell application "System Events" to log out'],
        }
        self.run(commands[choice])


def get_platform() -> PowerPlatform:
    if os.name == "nt":
        return WindowsPlatform()
    if sys.platform == "darwin":
        return MacOSPlatform()
    if sys.platform.startswith("linux") and shutil.which("loginctl") and shutil.which("systemd-inhibit"):
        return LinuxPlatform()
    return PowerPlatform()
