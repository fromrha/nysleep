# 🌙 Nythsleep — The Ultimate Windows 11 Power Management CLI

[![GitHub License](https://img.shields.io/github/license/fromrha/nythsleep?style=flat-square&color=blue)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/fromrha/nythsleep?style=flat-square)](https://github.com/fromrha/nythsleep/stargazers)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)

**Control your computer's rest as easily as you control your own.**

Nythsleep is a lightweight, high-performance CLI utility for Windows 11 that gives you total control over power actions. No more digging through menus—just type `nythsleep` and go to bed.

---

## ✨ Features

- 🚀 **Lightning Fast**: Execute power commands in seconds.
- 🕒 **Custom Timers**: Set precision timers (e.g., `1h 30m`) for automatic actions.
- 🎨 **Beautiful Interface**: Clean, color-coded CLI experience.
- 🌍 **Global Access**: Call it from any terminal (CMD or PowerShell).
- 🛠️ **Multiple Actions**: Shutdown, Restart, Sleep, or Logout.

---

## 🚀 Quick Setup

### The "Pro" Way (Recommended)

1. **Create your toolshed**:
   ```cmd
   mkdir C:\Tools
   ```
2. **Deploy the payload**:
   Move `nythsleep.py` and `nythsleep.bat` to `C:\Tools`.
3. **Go Global**:
   Add `C:\Tools` to your system **PATH**.
   *Pro Tip: Run this in PowerShell as Admin:*
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Tools", "Machine")
   ```

---

## 🎮 How to Use

Simply type:
```cmd
nythsleep
```

### Timer Magic
| Command | Effect |
| :--- | :--- |
| `1h` | Shutdown in 1 hour |
| `30m` | Restart in 30 minutes |
| `2h 15m` | Sleep in 2 hours 15 mins |
| `(Enter)` | Immediate action |

---

## 🛠️ Troubleshooting

- **Python not found?** Ensure Python 3.8+ is installed and in your PATH.
- **Access Denied?** Some actions require Administrator privileges.
- **Visuals Glitchy?** We recommend using [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701) for the best experience.

---

## 💎 Credits

Crafted with ❤️ by **Fromrha 2026**.

🔗 **GitHub**: [github.com/fromrha](https://github.com/fromrha)  
🌐 **Website**: [fromrha.com](https://fromrha.com)

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.
