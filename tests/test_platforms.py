import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
import nythsleep
from platforms import LinuxPlatform, PlatformError


class TimerTests(unittest.TestCase):
    def test_timer_parser(self):
        self.assertEqual(nythsleep.parse_timer("1h 30m 10s"), 5410)
        self.assertEqual(nythsleep.parse_timer("now"), 0)
        self.assertEqual(nythsleep.parse_timer("20"), -1)
        self.assertEqual(nythsleep.parse_timer("1x"), -1)


class LinuxPlatformTests(unittest.TestCase):
    def test_battery_uses_lowest_valid_pack(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, value in (("BAT0", "74"), ("BAT1", "61")):
                (root / name).mkdir()
                (root / name / "capacity").write_text(value)
            with patch("platforms.Path") as path:
                path.return_value.glob.return_value = list(root.glob("BAT*"))
                self.assertEqual(LinuxPlatform().battery_percentage(), 61)

    def test_logout_rejects_non_graphical_session(self):
        platform = LinuxPlatform()
        with patch.dict(os.environ, {"XDG_SESSION_ID": "1"}, clear=True), \
             patch("platforms.getpass.getuser", return_value="user"), \
             patch("platforms.shutil.which", return_value="/usr/bin/loginctl"), \
             patch("platforms.subprocess.check_output", return_value="user\ntty\nuser\nactive\n"):
            with self.assertRaises(PlatformError):
                platform._current_graphical_session()

    def test_insomnia_command(self):
        platform = LinuxPlatform()
        with patch("platforms.shutil.which", return_value="/usr/bin/systemd-inhibit"), \
             patch("platforms.subprocess.Popen") as popen:
            platform.start_insomnia()
        self.assertEqual(
            popen.call_args.args[0],
            ["/usr/bin/systemd-inhibit", "--what=idle:sleep", "--mode=block", "--why=Nythsleep Keep Awake", "sleep", "infinity"],
        )


if __name__ == "__main__":
    unittest.main()
