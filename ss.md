# Implementation Plan - Nythsleep Pro Features

This plan outlines the addition of several "Pro" features to the Nythsleep CLI tool, focusing on automation, system integration, and UI personalization while maintaining a zero-dependency (built-in only) architecture.

## User Review Required

> [!IMPORTANT]
> **Zero-Dependency Policy**: All features will be implemented using Python's built-in libraries (`ctypes`, `argparse`, `subprocess`) to ensure the tool remains portable and "Pro" without requiring `pip install`.

> [!NOTE]
> **Notification Method**: Desktop notifications will be triggered via a PowerShell bridge to avoid external notification libraries. This may cause a very brief PowerShell window flash on older Windows versions, though we will attempt to hide it.

## Proposed Changes

### [Core] nythsleep.py

#### [MODIFY] [nythsleep.py](file:///d:/VS%20Code/Project/nysleep/src/nythsleep.py)

1.  **CLI Argument Parsing**:
    *   Integrate `argparse` to support flags:
        *   `-s`, `--shutdown`, `-r`, `--restart`, `-l`, `--logout`, `-z`, `--sleep`.
        *   `-t`, `--timer` (e.g., `1h 30m`).
        *   `-i`, `--insomnia` (Keep Awake mode).
        *   `-b`, `--battery` (Trigger at percentage).
        *   `--theme` (Select UI theme).
2.  **Theme System**:
    *   Refactor hardcoded purple colors into a `Theme` class or dictionary.
    *   Add themes: `Midnight` (Deep Blue), `Sunset` (Orange/Pink), `Forest` (Emerald), and the default `Lavender` (Purple).
3.  **Insomnia Mode**:
    *   Implement `SetThreadExecutionState` via `ctypes` to prevent system/display sleep while the process is active.
4.  **Battery Monitoring**:
    *   Implement `GetSystemPowerStatus` via `ctypes` to check real-time battery levels.
    *   Add logic to wait until a specific percentage is reached before triggering an action.
5.  **Notifications**:
    *   Add a `send_notification(title, message)` function using a `subprocess` call to PowerShell's `NotifyIcon` or `BurntToast` (if available) or a simple fallback popup.
    *   Trigger a "Pre-action" notification 60 seconds before the timer ends.

### [Build] nythsleep.bat

#### [MODIFY] [nythsleep.bat](file:///d:/VS%20Code/Project/nysleep/nythsleep.bat)

*   Ensure the batch script correctly forwards all CLI arguments to the Python script using `%*`. (This is already implemented but will be verified).

## Verification Plan

### Automated Tests
*   `nythsleep --help`: Verify all new flags are documented.
*   `nythsleep -z -t 5s`: Verify sleep (or a safe action like Logout) triggers after 5 seconds with a notification.
*   `nythsleep --theme sunset`: Verify colors change to orange/pink.
*   `nythsleep --insomnia`: Verify the screen does not dim during a long wait.

### Manual Verification
*   Unplug the laptop and run `nythsleep --battery 95 --action sleep` (using a percentage just below current) to verify battery triggering.
*   Check that the desktop notification appears correctly 1 minute before scheduled actions.
