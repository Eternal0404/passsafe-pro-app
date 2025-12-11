from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QCheckBox, QPushButton, QLabel, QHBoxLayout
from core.password_generator import generate_password, suggest_stronger
from core.strength_checker import check_strength
from core.clipboard_manager import copy_to_clipboard

class GeneratorView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.length_spin = QSpinBox()
        self.length_spin.setRange(4, 128)
        self.length_spin.setValue(12)
        self.layout.addWidget(QLabel("Length:"))
        self.layout.addWidget(self.length_spin)
        self.upper_check = QCheckBox("Uppercase")
        self.upper_check.setChecked(True)
        self.layout.addWidget(self.upper_check)
        self.lower_check = QCheckBox("Lowercase")
        self.lower_check.setChecked(True)
        self.layout.addWidget(self.lower_check)
        self.digits_check = QCheckBox("Digits")
        self.digits_check.setChecked(True)
        self.layout.addWidget(self.digits_check)
        self.symbols_check = QCheckBox("Symbols")
        self.symbols_check.setChecked(True)
        self.layout.addWidget(self.symbols_check)
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.clicked.connect(self.generate)
        self.layout.addWidget(self.generate_btn)
        self.password_label = QLabel("Generated Password: ")
        self.layout.addWidget(self.password_label)
        self.strength_label = QLabel("Strength: ")
        self.layout.addWidget(self.strength_label)
        self.copy_btn = QPushButton("Copy")
        self.copy_btn.clicked.connect(self.copy)
        self.layout.addWidget(self.copy_btn)
        self.suggest_btn = QPushButton("Suggest Stronger")
        self.suggest_btn.clicked.connect(self.suggest)
        self.layout.addWidget(self.suggest_btn)
        self.setLayout(self.layout)
        self.current_password = ''

    def generate(self):
        length = self.length_spin.value()
        upper = self.upper_check.isChecked()
        lower = self.lower_check.isChecked()
        digits = self.digits_check.isChecked()
        symbols = self.symbols_check.isChecked()
        self.current_password = generate_password(length, upper, lower, digits, symbols)
        self.password_label.setText(f"Generated Password: {self.current_password}")
        strength = check_strength(self.current_password)
        self.strength_label.setText(f"Strength: {strength}")

    def copy(self):
        if self.current_password:
            copy_to_clipboard(self.current_password)

    def suggest(self):
        if self.current_password:
            suggested = suggest_stronger(self.current_password)
            if suggested:
                self.current_password = suggested
                self.password_label.setText(f"Suggested Password: {self.current_password}")
                strength = check_strength(self.current_password)
                self.strength_label.setText(f"Strength: {strength}")