#!/usr/bin/env python3
"""Nythsleep - cross-platform terminal power management."""

import argparse
import json
import os
import sys
import time
import urllib.request

from platforms import PlatformError, get_platform

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
CYAN="\033[38;2;100;220;255m"; PINK="\033[38;2;255;120;200m"; GREEN="\033[38;2;120;255;160m"
YELLOW="\033[38;2;255;230;100m"; RED="\033[38;2;255;100;100m"; WHITE="\033[38;2;220;220;230m"; GRAY="\033[38;2;130;130;150m"
P1=P2=P3=P4=P5=P6=""
VERSION="2.0.0"; AUTHOR="Nythsleep"
ACTIONS=[("Shutdown", "Power off machine"), ("Restart", "Reboot machine"), ("Sleep", "Suspend machine"), ("Logout", "Sign out current session")]


def set_theme(name):
    global P1,P2,P3,P4,P5,P6
    palettes={
        "lavender": ("200;140;255","180;100;255","160;70;255","140;50;230","120;30;210","100;20;190"),
        "midnight": ("140;200;255","100;180;255","70;160;255","50;140;230","30;120;210","20;100;190"),
        "sunset": ("255;180;140","255;150;100","255;120;70","230;90;50","210;60;30","190;40;20"),
        "forest": ("140;255;180","100;255;150","70;255;120","50;230;90","30;210;60","20;190;40"),
    }
    P1,P2,P3,P4,P5,P6=("\033[38;2;"+color+"m" for color in palettes[name])


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def banner(platform):
    print(f"\n{P1}{BOLD}  N Y T H S L E E P{RESET}")
    print(f"  {GRAY}{'─'*58}{RESET}")
    print(f"  {P2}{BOLD}{AUTHOR}{RESET} {GRAY}v{VERSION} | {WHITE}{platform.name} Power Management{RESET}")
    print(f"  {GRAY}{'─'*58}{RESET}\n")


def parse_timer(raw):
    raw=raw.strip().lower()
    if raw in ("", "0", "now"): return 0
    total=0; digits=""
    for char in raw:
        if char.isdigit(): digits+=char
        elif char in "hms" and digits:
            total += int(digits)*{"h":3600,"m":60,"s":1}[char]; digits=""
        elif char != " ": return -1
    return -1 if digits else total


def format_duration(seconds):
    if not seconds: return f"{YELLOW}immediately{RESET}"
    units=((3600,"h"),(60,"m"),(1,"s")); parts=[]
    for unit,label in units:
        value,seconds=divmod(seconds,unit)
        if value: parts.append(f"{value}{label}")
    return f"{YELLOW}{' '.join(parts)}{RESET}"


def check_for_update():
    try:
        req=urllib.request.Request("https://api.github.com/repos/fromrha/nythsleep/releases/latest", headers={"User-Agent":"Nythsleep"})
        with urllib.request.urlopen(req,timeout=1) as response:
            return json.loads(response.read().decode()).get("tag_name", VERSION).lstrip("v")
    except Exception: return None


def countdown(seconds, action, platform):
    if not seconds: return True
    print(f"\n  {P2}{BOLD}Countdown{RESET} {GRAY}(Ctrl+C cancels){RESET}\n")
    try:
        for remaining in range(seconds,0,-1):
            if remaining==60: platform.notify("Nythsleep", f"{action} executes in 60 seconds.")
            h,remainder=divmod(remaining,3600); m,s=divmod(remainder,60)
            print(f"\r  {CYAN}{h:02d}:{m:02d}:{s:02d}{RESET} {GRAY}{action} pending...{RESET}  ",end="",flush=True)
            time.sleep(1)
        print(); return True
    except KeyboardInterrupt:
        print(f"\n  {RED}Cancelled. Action aborted.{RESET}"); return False


def wait_for_battery(target, action, platform):
    print(f"\n  {P2}{BOLD}Waiting for battery to reach {target}%...{RESET}")
    try:
        while True:
            current=platform.battery_percentage()
            if current<=target:
                print(f"\n  {YELLOW}Battery reached {current}%.{RESET}"); return True
            print(f"\r  {CYAN}Battery: {current}%{RESET} {GRAY}(target: {target}%, {action} pending){RESET}  ",end="",flush=True)
            time.sleep(10)
    except KeyboardInterrupt:
        print(f"\n  {RED}Cancelled. Action aborted.{RESET}"); return False


def run_insomnia(seconds, platform):
    platform.start_insomnia()
    print(f"\n  {GREEN}{BOLD}Keep Awake active{RESET} {GRAY}(Ctrl+C stops){RESET}")
    try:
        if seconds:
            return countdown(seconds, "Keep Awake end", platform)
        while True: time.sleep(1)
    except KeyboardInterrupt: return True
    finally:
        platform.stop_insomnia()
        print(f"\n  {P2}Keep Awake disabled.{RESET}")


def ask_choice():
    while True:
        print(f"  {P2}{BOLD}What would you like to do?{RESET}")
        for index,(name,description) in enumerate(ACTIONS,1): print(f"    {CYAN}[{index}]{RESET} {WHITE}{name}{RESET} {GRAY}- {description}{RESET}")
        try:
            choice=int(input(f"\n  {P3}{BOLD}>{RESET} Pick option (0-4): "))
            if 0<=choice<=4: return choice
        except (ValueError, EOFError): pass
        print(f"  {RED}Enter number 0 through 4.{RESET}")


def ask_timer():
    while True:
        raw=input(f"  {P3}{BOLD}>{RESET} Timer (example: 1h 30m; Enter for now): ")
        seconds=parse_timer(raw)
        if seconds>=0: return seconds
        print(f"  {RED}Use h, m, s units. Example: 1h 30m.{RESET}")


def confirm(action, seconds, battery, force):
    print(f"\n  {P2}{BOLD}Summary{RESET}\n    Action: {WHITE}{action}{RESET}\n    Timer: {format_duration(seconds)}")
    if battery is not None: print(f"    Battery: {YELLOW}wait for {battery}%{RESET}")
    if force: return True
    return input(f"\n  {GREEN}[Y]{RESET} Run  {RED}[N]{RESET} Cancel\n  {P3}>{RESET} ").strip().lower() in ("y","yes")


class Parser(argparse.ArgumentParser):
    def error(self,message):
        self.exit(2, f"{RED}Error: {message}{RESET}\nRun nythsleep --help for usage.\n")


def parse_args():
    parser=Parser(description="Nythsleep - cross-platform terminal power management.")
    actions=parser.add_mutually_exclusive_group()
    actions.add_argument("-s","--shutdown",action="store_true",help="Power off machine")
    actions.add_argument("-r","--restart",action="store_true",help="Reboot machine")
    actions.add_argument("-z","--sleep",action="store_true",help="Suspend machine")
    actions.add_argument("-l","--logout",action="store_true",help="Sign out current session")
    parser.add_argument("-t","--timer",help="Timer such as '1h 30m'")
    parser.add_argument("-i","--insomnia",action="store_true",help="Keep system awake; accepts --timer")
    parser.add_argument("-b","--battery",type=int,help="Run action at battery percentage (1-100)")
    parser.add_argument("-y","--yes",action="store_true",help="Skip destructive-action confirmation")
    parser.add_argument("--theme",choices=("lavender","midnight","sunset","forest"),default="lavender")
    parser.add_argument("--version",action="version",version=VERSION)
    return parser.parse_args()


def main():
    args=parse_args(); set_theme(args.theme); platform=get_platform()
    choice=1 if args.shutdown else 2 if args.restart else 3 if args.sleep else 4 if args.logout else 0
    if args.insomnia and choice: print(f"{RED}Error: --insomnia cannot combine with power action.{RESET}"); return 2
    if args.battery is not None and not 1<=args.battery<=100: print(f"{RED}Error: --battery must be 1 through 100.{RESET}"); return 2
    seconds=parse_timer(args.timer or "")
    if seconds<0: print(f"{RED}Error: invalid timer '{args.timer}'. Use h, m, s units.{RESET}"); return 2
    if args.insomnia:
        run_insomnia(seconds,platform); return 0
    if not choice and (args.timer or args.battery is not None or args.yes): print(f"{RED}Error: modifiers require power action or --insomnia.{RESET}"); return 2
    if not choice:
        clear_screen(); banner(platform); choice=ask_choice()
        if not choice: return 0
        seconds=ask_timer()
    action=ACTIONS[choice-1][0]
    if not confirm(action,seconds,args.battery,args.yes): print(f"\n  {GRAY}Cancelled.{RESET}"); return 0
    try:
        if args.battery is not None and not wait_for_battery(args.battery,action,platform): return 0
        if not countdown(seconds,action,platform): return 0
        print(f"\n  {P4}{BOLD}Executing {action}...{RESET}")
        platform.execute(choice)
    except PlatformError as error:
        print(f"\n  {RED}{BOLD}Error:{RESET} {WHITE}{error}{RESET}"); return 1
    return 0


if __name__=="__main__": sys.exit(main())
