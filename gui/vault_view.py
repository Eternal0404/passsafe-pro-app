from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QLineEdit, QHBoxLayout, QLabel, QFrame, QDialog, QFormLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from core.data_manager import load_vault, add_vault_entry, update_vault_entry, delete_vault_entry, search_vault
from core.clipboard_manager import copy_to_clipboard

class VaultView(QWidget):
    def __init__(self, key):
        super().__init__()
        self.key = key
        self.layout = QVBoxLayout()
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search vault...")
        self.search_input.textChanged.connect(self.search)
        self.layout.addWidget(self.search_input)
        # Add button
        self.add_btn = QPushButton("Add Entry")
        self.add_btn.clicked.connect(self.add_entry)
        self.layout.addWidget(self.add_btn)
        # Scroll area for cards
        self.scroll = QScrollArea()
        self.cards_widget = QWidget()
        self.cards_layout = QVBoxLayout()
        self.cards_widget.setLayout(self.cards_layout)
        self.scroll.setWidget(self.cards_widget)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)
        self.load_entries()

    def load_entries(self):
        vault = load_vault(self.key)
        self.display_entries(vault)

    def display_entries(self, entries):
        # Clear
        for i in reversed(range(self.cards_layout.count())):
            self.cards_layout.itemAt(i).widget().setParent(None)
        for entry in entries:
            card = QFrame()
            card.setFrameStyle(QFrame.Shape.Box)
            card_layout = QVBoxLayout()
            account_label = QLabel(f"Account: {entry['account']}")
            username_label = QLabel(f"Username: {entry['username']}")
            tags_label = QLabel(f"Tags: {', '.join(entry['tags'])}")
            copy_btn = QPushButton("Copy Password")
            copy_btn.clicked.connect(lambda _, p=entry['password']: copy_to_clipboard(p))
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, e=entry: self.edit_entry(e))
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda _, u=entry['uuid']: self.delete_entry(u))
            card_layout.addWidget(account_label)
            card_layout.addWidget(username_label)
            card_layout.addWidget(tags_label)
            btn_layout = QHBoxLayout()
            btn_layout.addWidget(copy_btn)
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            card_layout.addLayout(btn_layout)
            card.setLayout(card_layout)
            self.cards_layout.addWidget(card)

    def search(self):
        query = self.search_input.text()
        if query:
            results = search_vault(query, self.key)
            self.display_entries(results)
        else:
            self.load_entries()

    def add_entry(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Entry")
        form = QFormLayout()
        account_input = QLineEdit()
        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        tags_input = QLineEdit()
        form.addRow("Account:", account_input)
        form.addRow("Username:", username_input)
        form.addRow("Password:", password_input)
        form.addRow("Tags (comma separated):", tags_input)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.save_new_entry(account_input.text(), username_input.text(), password_input.text(), tags_input.text().split(',')))
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)
        dialog.setLayout(form)
        dialog.exec()

    def save_new_entry(self, account, username, password, tags):
        add_vault_entry(account, username, password, [t.strip() for t in tags], self.key)
        self.load_entries()

    def edit_entry(self, entry):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Entry")
        form = QFormLayout()
        account_input = QLineEdit(entry['account'])
        username_input = QLineEdit(entry['username'])
        password_input = QLineEdit(entry['password'])
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        tags_input = QLineEdit(', '.join(entry['tags']))
        form.addRow("Account:", account_input)
        form.addRow("Username:", username_input)
        form.addRow("Password:", password_input)
        form.addRow("Tags:", tags_input)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.save_edit_entry(entry['uuid'], account_input.text(), username_input.text(), password_input.text(), tags_input.text().split(',')))
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)
        dialog.setLayout(form)
        dialog.exec()

    def save_edit_entry(self, uuid, account, username, password, tags):
        update_vault_entry(uuid, account, username, password, [t.strip() for t in tags], self.key)
        self.load_entries()

    def delete_entry(self, uuid):
        delete_vault_entry(uuid, self.key)
        self.load_entries()