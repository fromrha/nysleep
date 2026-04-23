# Changelog

## [Unreleased]
### Added
- Dedicated interactive loop for Insomnia Mode (`-i`) with elapsed time/countdown display.

### Fixed
- Improved strict validation for timer inputs (`-t`), ensuring units (`h`, `m`, `s`) are provided.

## [1.2.0] - 2026-04-22

### Added
- **Pro Features**: Added advanced power management capabilities.
- **Theme System**: Choose between `lavender`, `midnight`, `sunset`, and `forest` themes using the `--theme` flag.
- **Insomnia Mode**: Prevent system and display sleep using the `--insomnia` flag.
- **Battery Monitoring**: Trigger actions at a specific battery percentage using the `--battery` flag.
- **Desktop Notifications**: Native Windows notifications triggered 60 seconds before a scheduled action.
- **Argparse Integration**: Full support for CLI flags (-s, -r, -z, -l, -t, -i, -b).
- **Pre-action Notifications**: Automatic notification 1 minute before the timer ends.

### Changed
- **UI Refactoring**: Colors and banners are now dynamically generated based on the selected theme.
- **Zero-Dependency Core**: All new features implemented using Python's built-in `ctypes`, `argparse`, and `subprocess`.


## [1.1.1] - 2026-04-21

### Fixed
- Fixed global execution issue by moving `nythsleep.bat` to the project root.
- Fixed `UnicodeEncodeError` when rendering the ANSI banner on standard Windows terminals by forcing UTF-8 encoding in the batch script.
- Removed the deprecated `scripts` directory to simplify the project structure.

## [1.1.0] - 2026-04-21

### Added
- **New 3D ANSI Shadow Banner**: Premium "NYTH SLEEP" ASCII art for the main menu.
- **Visual Assets**: Integrated `banner.png` and `demo.png` into the repository and `README.md`.
- **KeyboardInterrupt Handling**: The app now exits gracefully when pressing Ctrl+C.

### Changed
- **Folder Structure Optimization**: Reorganized files into `src`, `assets`, `docs`, and `scripts` for a cleaner repository.
- **Global Setup**: Updated setup instructions to reflect the new file locations.
- **Version Bump**: Official release v1.1.0.

### Fixed
- Error messages when cancelling the program with Ctrl+C.
