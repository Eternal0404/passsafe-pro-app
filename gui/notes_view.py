from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QLineEdit, QHBoxLayout, QLabel, QFrame, QDialog, QFormLayout, QTextEdit, QDialogButtonBox
from PyQt6.QtCore import Qt
from core.data_manager import load_notes, add_note, update_note, delete_note, search_notes

class NotesView(QWidget):
    def __init__(self, key):
        super().__init__()
        self.key = key
        self.layout = QVBoxLayout()
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search notes...")
        self.search_input.textChanged.connect(self.search)
        self.layout.addWidget(self.search_input)
        # Add button
        self.add_btn = QPushButton("Add Note")
        self.add_btn.clicked.connect(self.add_note)
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
        self.load_notes()

    def load_notes(self):
        notes = load_notes(self.key)
        self.display_notes(notes)

    def display_notes(self, notes):
        # Clear
        for i in reversed(range(self.cards_layout.count())):
            self.cards_layout.itemAt(i).widget().setParent(None)
        for note in notes:
            card = QFrame()
            card.setFrameStyle(QFrame.Shape.Box)
            card_layout = QVBoxLayout()
            content_label = QLabel(note['content'][:100] + '...' if len(note['content']) > 100 else note['content'])
            content_label.setWordWrap(True)
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, n=note: self.edit_note(n))
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda _, u=note['uuid']: self.delete_note(u))
            card_layout.addWidget(content_label)
            btn_layout = QHBoxLayout()
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            card_layout.addLayout(btn_layout)
            card.setLayout(card_layout)
            self.cards_layout.addWidget(card)

    def search(self):
        query = self.search_input.text()
        if query:
            results = search_notes(query, self.key)
            self.display_notes(results)
        else:
            self.load_notes()

    def add_note(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Note")
        form = QFormLayout()
        account_input = QLineEdit()
        content_input = QTextEdit()
        form.addRow("Account UUID:", account_input)
        form.addRow("Content:", content_input)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.save_new_note(account_input.text(), content_input.toPlainText()))
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)
        dialog.setLayout(form)
        dialog.exec()

    def save_new_note(self, account_uuid, content):
        add_note(account_uuid, content, self.key)
        self.load_notes()

    def edit_note(self, note):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Note")
        form = QFormLayout()
        content_input = QTextEdit(note['content'])
        form.addRow("Content:", content_input)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.save_edit_note(note['uuid'], content_input.toPlainText()))
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)
        dialog.setLayout(form)
        dialog.exec()

    def save_edit_note(self, uuid, content):
        update_note(uuid, content, self.key)
        self.load_notes()

    def delete_note(self, uuid):
        delete_note(uuid, self.key)
        self.load_notes()