![Nythsleep Banner](assets/banner.png)

# 🌙 Nythsleep — The Ultimate Windows 11 Power Management CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/fromrha/nythsleep?style=flat-square)](https://github.com/fromrha/nythsleep/stargazers)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)

**Because a good night's sleep shouldn't end with a bright screen at 3 AM.**

I have a routine: I can't sleep without some ASMR or ambient music playing in the background. My computer serves as my speaker, but I hated leaving it running all night—and I hated the clunky, bright Windows menus even more. 

As a developer who lives in the terminal, I wanted something that felt right. A sleek, purple-tinted command that does exactly what I need and nothing more. I built Nythsleep for myself, and now I'm sharing it with you.

---

## Features

- **Lightning Fast**: Execute power commands in seconds.
- **Custom Timers**: Set precision timers (e.g., `1h 30m`) for automatic actions.
- **Premium Themes**: Choose between `Lavender`, `Midnight`, `Sunset`, and `Forest`.
- **Insomnia Mode**: Keep your machine awake when you need it most.
- **Battery Triggers**: Trigger actions automatically at specific battery levels.
- **Smart Notifications**: Native Windows notifications 60s before any action.
- **Global Access**: Call it from any terminal with full flag support.

![Nythsleep Demo](assets/demo.png)

---

## Quick Setup

### The "Pro" Way (Recommended)

1. **Clone the repository**:
   ```cmd
   git clone https://github.com/fromrha/nythsleep.git
   ```
2. **Go Global**:
   Add the cloned repository directory to your system **PATH**.
   *Pro Tip: Run this in PowerShell as Admin (replace `C:\path\to\nythsleep` with your actual path):*
   ```powershell
   $targetPath = "C:\path\to\nythsleep"
   [Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "Machine") + ";$targetPath", "Machine")
   ```

---

### CLI Flags (Pro Features)
You can now bypass the interactive menu entirely using flags.
**Pro Tip:** Use the `nsleep` quick-command alias for even faster execution without any confirmation prompts!

| Flag | Action |
| :--- | :--- |
| `-s`, `--shutdown` | Power off completely |
| `-r`, `--restart` | Reboot machine |
| `-z`, `--sleep` | Put to sleep |
| `-l`, `--logout` | Sign out |
| `-t`, `--timer` | Set a timer (e.g. `-t 1h 30m`) |
| `-i`, `--insomnia` | Enable "Keep Awake" mode |
| `-b`, `--battery` | Trigger at battery % (e.g. `-b 20`) |
| `--theme` | Select theme (`midnight`, `sunset`, `forest`) |

**Examples:**
```cmd
nsleep -s -t 20m
nsleep --theme sunset --sleep -t 30m
```

---

## Troubleshooting

- **Python not found?** Ensure Python 3.8+ is installed and in your PATH.
- **Access Denied?** Some actions require Administrator privileges.
- **Visuals Glitchy?** We recommend using [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701) for the best experience.

---

## Credits

Crafted with ❤️ by **Fromrha 2026**.

🔗 **GitHub**: [github.com/fromrha](https://github.com/fromrha)  
🌐 **Website**: [fromrha.com](https://fromrha.com)

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.
