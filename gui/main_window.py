from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QListWidget, QWidget, QStackedWidget
from PyQt6.QtCore import Qt
from .vault_view import VaultView
from .notes_view import NotesView
from .generator_view import GeneratorView
from .settings_view import SettingsView
from .themes import get_theme_css

class MainWindow(QMainWindow):
    def __init__(self, key, theme='light'):
        super().__init__()
        self.key = key
        self.theme = theme
        self.setWindowTitle("PassSafe Pro")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(get_theme_css(theme))
        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.addItem("Vault")
        self.sidebar.addItem("Notes")
        self.sidebar.addItem("Generator")
        self.sidebar.addItem("Settings")
        self.sidebar.currentRowChanged.connect(self.change_view)
        # Stacked widget for views
        self.stack = QStackedWidget()
        self.vault_view = VaultView(self.key)
        self.notes_view = NotesView(self.key)
        self.generator_view = GeneratorView()
        self.settings_view = SettingsView()
        self.stack.addWidget(self.vault_view)
        self.stack.addWidget(self.notes_view)
        self.stack.addWidget(self.generator_view)
        self.stack.addWidget(self.settings_view)
        # Layout
        central_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.sidebar, 1)
        layout.addWidget(self.stack, 4)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def change_view(self, index):
        self.stack.setCurrentIndex(index)