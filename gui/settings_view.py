from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QSpinBox, QPushButton, QLabel
from core.data_manager import get_theme, set_theme, get_auto_lock, set_auto_lock

class SettingsView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['light', 'dark', 'neon'])
        self.theme_combo.setCurrentText(get_theme())
        self.theme_combo.currentTextChanged.connect(set_theme)
        self.layout.addWidget(QLabel("Theme:"))
        self.layout.addWidget(self.theme_combo)
        self.auto_lock_spin = QSpinBox()
        self.auto_lock_spin.setRange(60, 3600)
        self.auto_lock_spin.setValue(get_auto_lock())
        self.auto_lock_spin.valueChanged.connect(set_auto_lock)
        self.layout.addWidget(QLabel("Auto-lock (seconds):"))
        self.layout.addWidget(self.auto_lock_spin)
        self.setLayout(self.layout)