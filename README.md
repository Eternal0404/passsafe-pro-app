# PassSafe Pro App

A fully offline, open-source password manager for Windows, built with Python, PyQt5, and AES-256 encryption.

## Features

- **Secure Password Vault**: Store, edit, delete, and search passwords with AES-256 encryption.
- **Secure Notes**: Encrypted notes linked to accounts.
- **Password Generator**: Customizable generator with strength checker and suggestions.
- **Modern GUI**: PyQt5-based interface with sidebar navigation, card layouts, animations, and themes (light, dark, neon).
- **Clipboard Management**: Copy passwords with automatic 10-second clear.
- **Backup & Restore**: Export/import encrypted data.
- **Search**: Across passwords and notes by account/website/tags.
- **CSV Import**: Drag-and-drop support.
- **Settings**: Theme toggle, auto-lock configuration.
- **Security**: Master password protection, retry limits, auto-lock.

## Installation

1. Download `passsafe-pro-app.exe` from the [Releases](https://github.com/Eternal0404/passsafe-pro-app/releases) page.
2. No installation required; run the exe directly on Windows.

## Usage

1. **First Run**: Launch the exe and set a strong master password.
2. **Navigation**: Use the sidebar to switch between Vault, Notes, Generator, and Settings.
3. **Vault**: Add/edit/delete entries; search and copy passwords securely.
4. **Notes**: Add notes linked to accounts.
5. **Generator**: Generate strong passwords with options.
6. **Settings**: Change theme and auto-lock settings.

## Security

- Fully offline; no data sent over internet.
- AES-256 encryption for all sensitive data.
- Master password required to access; hashed securely.
- Auto-lock after inactivity; retry limits prevent brute-force.
- Data stored in local `/data` folder as encrypted JSON.

## Screenshots

![Main Interface](assets/screenshots/main.png)
![Vault View](assets/screenshots/vault.png)
![Generator](assets/screenshots/generator.png)

## Building from Source

1. Clone the repo: `git clone https://github.com/Eternal0404/passsafe-pro-app.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`
4. Package: `pyinstaller --onefile --windowed main.py --name passsafe-pro-app --add-data "data;data"`

## License

MIT License - see [LICENSE](LICENSE) for details.