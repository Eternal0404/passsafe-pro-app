import sys
from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox, QLineEdit
from core.data_manager import verify_master_password, set_master_password, get_encryption_key, load_settings
from gui.main_window import MainWindow
from gui.themes import get_theme_css

def main():
    app = QApplication(sys.argv)
    settings = load_settings()
    if 'master_hash' not in settings:
        # Set master password
        password, ok = QInputDialog.getText(None, "Set Master Password", "Enter a strong master password:", QLineEdit.EchoMode.Password)
        if not ok or not password:
            return
        confirm, ok2 = QInputDialog.getText(None, "Confirm Master Password", "Confirm master password:", QLineEdit.EchoMode.Password)
        if not ok2 or password != confirm:
            QMessageBox.warning(None, "Error", "Passwords do not match.")
            return
        set_master_password(password)
    else:
        # Verify
        password, ok = QInputDialog.getText(None, "Enter Master Password", "Master Password:", QLineEdit.EchoMode.Password)
        if not ok or not verify_master_password(password):
            QMessageBox.warning(None, "Error", "Incorrect password.")
            return
    key = get_encryption_key(password)
    theme = settings.get('theme', 'light')
    window = MainWindow(key, theme)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()