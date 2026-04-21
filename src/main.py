#!/usr/bin/env python3
"""
NythSleep - A stylish Windows 11 power management CLI tool.
Shutdown, restart, sleep, or logout with optional timers.
"""

import os
import sys
import time
import ctypes
import subprocess
import urllib.request
import json

# ── ANSI Color Codes ──────────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
UNDERLINE = "\033[4m"

# Purple gradient shades
P1 = "\033[38;2;200;140;255m"  # light lavender
P2 = "\033[38;2;180;100;255m"  # soft purple
P3 = "\033[38;2;160;70;255m"   # medium purple
P4 = "\033[38;2;140;50;230m"   # deep purple
P5 = "\033[38;2;120;30;210m"   # darker purpleb
P6 = "\033[38;2;100;20;190m"   # darkest purple

# Accent colors
CYAN    = "\033[38;2;100;220;255m"
PINK    = "\033[38;2;255;120;200m"
GREEN   = "\033[38;2;120;255;160m"
YELLOW  = "\033[38;2;255;230;100m"
RED     = "\033[38;2;255;100;100m"
WHITE   = "\033[38;2;220;220;230m"
GRAY    = "\033[38;2;130;130;150m"

VERSION = "1.0.0"
AUTHOR  = "NythSleep"

# ── ASCII Banner ──────────────────────────────────────────────────────────────

# ANSI Shadow Font: "NYTH SLEEP"
BANNER = f"""
{P1}{BOLD}  ███╗   ██╗██╗   ██╗████████╗██╗  ██╗     ███████╗██╗     ███████╗███████╗██████╗ 
{P2}  ████╗  ██║╚██╗ ██╔╝╚══██╔══╝██║  ██║     ██╔════╝██║     ██╔════╝██╔════╝██╔══██╗
{P3}  ██╔██╗ ██║ ╚████╔╝    ██║   ███████║     ███████╗██║     █████╗  █████╗  ██████╔╝
{P4}  ██║╚██╗██║  ╚██╔╝     ██║   ██╔══██║     ╚════██║██║     ██╔══╝  ██╔══╝  ██╔═══╝ 
{P5}  ██║ ╚████║   ██║      ██║   ██║  ██║     ███████║███████╗███████╗███████╗██║     
{P6}  ╚═╝  ╚═══╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝     ╚══════╝╚══════╝╚══════╝╚══════╝╚═╝     {RESET}
"""

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner(latest_version=None):
    print(BANNER)
    print(f"  {GRAY}{'─' * 104}{RESET}")
    link = f"\033]8;;https://fromrha.com\033\\{UNDERLINE}fromrha.com{RESET}\033]8;;\033\\"
    print(f"  {P2}{BOLD}{AUTHOR}{RESET} {GRAY}v{VERSION}{RESET}  {GRAY}|{RESET}  {WHITE}Windows Power Management Tool{RESET}  {GRAY}|{RESET}  {GRAY}{time.strftime('%Y-%m-%d')}{RESET}  {GRAY}|{RESET}  {P1}{link}{RESET}")
    print(f"  {GRAY}{'─' * 104}{RESET}")
    if latest_version:
        print(f"  {YELLOW}{BOLD}Update Available!{RESET} {WHITE}v{latest_version} is out. Download it from GitHub.{RESET}")
        print(f"  {GRAY}{'─' * 104}{RESET}")
    print()

def check_for_update():
    try:
        url = "https://api.github.com/repos/fromrha/nythsleep/releases/latest"
        req = urllib.request.Request(url, headers={'User-Agent': 'Nythsleep-Update-Checker'})
        with urllib.request.urlopen(req, timeout=1.0) as response:
            data = json.loads(response.read().decode())
            latest_version = data.get("tag_name", VERSION).lstrip('v')
            if latest_version != VERSION:
                return latest_version
    except Exception:
        pass
    return None

# ── Menu ──────────────────────────────────────────────────────────────────────

ACTIONS = [
    ("Shutdown",  "Power off your machine completely"),
    ("Restart",   "Reboot your machine"),
    ("Sleep",     "Put your machine to sleep"),
    ("Logout",    "Sign out of the current user session"),
]

def show_menu():
    print(f"  {P2}{BOLD}What would you like to do?{RESET}\n")
    for i, (name, desc) in enumerate(ACTIONS, 1):
        color = [CYAN, GREEN, YELLOW, PINK][i - 1]
        print(f"    {color}{BOLD}[{i}]{RESET}  {WHITE}{name}{RESET}  {GRAY}- {desc}{RESET}")
    print()
    print(f"    {RED}{BOLD}[0]{RESET}  {WHITE}Exit{RESET}")
    print()

def get_choice():
    while True:
        try:
            raw = input(f"  {P3}{BOLD}>{RESET} Pick an option {GRAY}(0-4){RESET}: ").strip()
            choice = int(raw)
            if 0 <= choice <= 4:
                return choice
            print(f"  {RED}  Please enter a number between 0 and 4.{RESET}")
        except (ValueError, EOFError):
            print(f"  {RED}  Invalid input. Enter a number.{RESET}")

# ── Timer ─────────────────────────────────────────────────────────────────────

def parse_timer(raw: str) -> int:
    """Parse timer string like '1h 30m 10s' into total seconds."""
    raw = raw.strip().lower()
    if raw in ("", "0", "now"):
        return 0

    total = 0
    current_num = ""
    for ch in raw:
        if ch.isdigit():
            current_num += ch
        elif ch in ("h", "m", "s") and current_num:
            val = int(current_num)
            if ch == "h":
                total += val * 3600
            elif ch == "m":
                total += val * 60
            elif ch == "s":
                total += val
            current_num = ""
        elif ch == " ":
            continue
        else:
            return -1  # invalid
    if current_num:
        return -1  # trailing digits with no unit
    return total

def format_duration(seconds: int) -> str:
    if seconds == 0:
        return f"{YELLOW}immediately{RESET}"
    parts = []
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h: parts.append(f"{h}h")
    if m: parts.append(f"{m}m")
    if s: parts.append(f"{s}s")
    return f"{YELLOW}{' '.join(parts)}{RESET}"

def get_timer():
    print(f"\n  {P3}{BOLD}>{RESET} Set a timer {GRAY}(e.g. 1h 30m, 45m, 10s, or press Enter for now){RESET}:")
    while True:
        raw = input(f"  {P3}{BOLD}>{RESET} ").strip()
        if raw == "":
            return 0
        secs = parse_timer(raw)
        if secs < 0:
            print(f"  {RED}  Invalid format. Use combinations like: 1h  30m  90s  1h 30m 10s{RESET}")
        else:
            return secs

# ── Countdown ─────────────────────────────────────────────────────────────────

def countdown(seconds: int, action_name: str):
    if seconds == 0:
        return
    print(f"\n  {P2}{BOLD}Countdown{RESET} {GRAY}(press Ctrl+C to cancel){RESET}\n")
    try:
        remaining = seconds
        while remaining > 0:
            h = remaining // 3600
            m = (remaining % 3600) // 60
            s = remaining % 60
            bar_total = 30
            filled = int((1 - remaining / seconds) * bar_total)
            bar = f"{P4}{'█' * filled}{GRAY}{'░' * (bar_total - filled)}{RESET}"
            line = f"\r  {bar}  {CYAN}{h:02d}:{m:02d}:{s:02d}{RESET}  {GRAY}{action_name} pending...{RESET}  "
            sys.stdout.write(line)
            sys.stdout.flush()
            time.sleep(1)
            remaining -= 1
        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.flush()
    except KeyboardInterrupt:
        print(f"\n\n  {RED}{BOLD}Cancelled!{RESET} Action aborted by user.\n")
        sys.exit(0)

# ── Execute ───────────────────────────────────────────────────────────────────

def execute_action(choice: int):
    if os.name != "nt":
        print(f"\n  {RED}{BOLD}Error:{RESET} {WHITE}This tool only works on Windows.{RESET}\n")
        return

    if choice == 1:    # Shutdown
        subprocess.run(["shutdown", "/s", "/t", "0"], shell=True)
    elif choice == 2:  # Restart
        subprocess.run(["shutdown", "/r", "/t", "0"], shell=True)
    elif choice == 3:  # Sleep
        # SetSuspendState(hibernate, force, disable_wake_events)
        ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)
    elif choice == 4:  # Logout
        subprocess.run(["shutdown", "/l"], shell=True)

# ── Confirmation ──────────────────────────────────────────────────────────────

def confirm(action_name: str, timer_secs: int) -> bool:
    color = {"Shutdown": CYAN, "Restart": GREEN, "Sleep": YELLOW, "Logout": PINK}[action_name]

    print(f"\n  {GRAY}{'─' * 50}{RESET}")
    print(f"  {P2}{BOLD}Summary{RESET}")
    print(f"  {GRAY}{'─' * 50}{RESET}")
    print(f"    {WHITE}Action :{RESET}  {color}{BOLD}{action_name}{RESET}")
    print(f"    {WHITE}Timer  :{RESET}  {format_duration(timer_secs)}")
    print(f"  {GRAY}{'─' * 50}{RESET}")
    print()
    print(f"    {GREEN}{BOLD}[Y]{RESET} {WHITE}Run{RESET}        {RED}{BOLD}[N]{RESET} {WHITE}Go back{RESET}")
    print()

    while True:
        ans = input(f"  {P3}{BOLD}>{RESET} ").strip().lower()
        if ans in ("y", "yes", ""):
            return True
        if ans in ("n", "no", "b", "back"):
            return False
        print(f"  {RED}  Type Y to run or N to go back.{RESET}")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Enable ANSI on Windows
    if os.name == "nt":
        os.system("")  # enables VT100 escape sequences in cmd/powershell
        
    latest_version = check_for_update()

    try:
        while True:
            clear_screen()
            print_banner(latest_version)
            show_menu()

            choice = get_choice()
            if choice == 0:
                print(f"\n  {P2}Goodbye! Sweet dreams.{RESET}\n")
                break

            action_name = ACTIONS[choice - 1][0]
            timer_secs = get_timer()

            if confirm(action_name, timer_secs):
                countdown(timer_secs, action_name)
                print(f"\n  {P4}{BOLD}Executing {action_name}...{RESET}\n")
                execute_action(choice)
                break
            # else loop back to menu
    except KeyboardInterrupt:
        print(f"\n\n  {P2}Goodbye! Session ended.{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
