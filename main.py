import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QFileDialog, QTextEdit, QVBoxLayout, QHBoxLayout, QCheckBox
)
import sys


class FileRenamer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bulk File Renamer")
        self.setGeometry(300, 300, 600, 400)

        # Initialize all attributes here
        self.folder_input = QLineEdit()
        self.prefix_input = QLineEdit()
        self.suffix_input = QLineEdit()
        self.replace_from_input = QLineEdit()
        self.replace_to_input = QLineEdit()
        self.numbering_checkbox = QCheckBox("Add numbering (e.g. 001_)")
        self.output_box = QTextEdit()

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Folder selection
        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit()
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(QLabel("Folder:"))
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_btn)
        layout.addLayout(folder_layout)

        # Prefix and Suffix
        self.prefix_input = QLineEdit()
        self.suffix_input = QLineEdit()
        layout.addWidget(QLabel("Prefix:"))
        layout.addWidget(self.prefix_input)
        layout.addWidget(QLabel("Suffix:"))
        layout.addWidget(self.suffix_input)

        # Replace from/to
        replace_layout = QHBoxLayout()
        self.replace_from_input = QLineEdit()
        self.replace_to_input = QLineEdit()
        replace_layout.addWidget(QLabel("Replace:"))
        replace_layout.addWidget(self.replace_from_input)
        replace_layout.addWidget(QLabel("With:"))
        replace_layout.addWidget(self.replace_to_input)
        layout.addLayout(replace_layout)

        # Numbering
        self.numbering_checkbox = QCheckBox("Add numbering (e.g. 001)")
        layout.addWidget(self.numbering_checkbox)

        # Rename button
        rename_btn = QPushButton("Rename Files")
        rename_btn.clicked.connect(self.rename_files)
        layout.addWidget(rename_btn)

        # Output log
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        layout.addWidget(self.output_box)

        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def rename_files(self):
        folder = self.folder_input.text()
        if not os.path.isdir(folder):
            self.output_box.setText("❌ Please select a valid folder.")
            return

        prefix = self.prefix_input.text()
        suffix = self.suffix_input.text()
        replace_from = self.replace_from_input.text()
        replace_to = self.replace_to_input.text()
        numbering = self.numbering_checkbox.isChecked()

        files = os.listdir(folder)
        renamed = []

        for i, filename in enumerate(files):
            full_path = os.path.join(folder, filename)
            if os.path.isfile(full_path):
                name, ext = os.path.splitext(filename)
                new_name = name
                if replace_from:
                    new_name = new_name.replace(replace_from, replace_to)
                if prefix:
                    new_name = prefix + new_name
                if suffix:
                    new_name = new_name + suffix
                if numbering:
                    new_name = f"{str(i+1).zfill(3)}_{new_name}"

                new_filename = new_name + ext
                os.rename(full_path, os.path.join(folder, new_filename))
                renamed.append(f"{filename} → {new_filename}")

        if renamed:
            self.output_box.setText("✅ Files renamed:\n" + "\n".join(renamed))
        else:
            self.output_box.setText("⚠️ No files renamed.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileRenamer()
    window.show()
    sys.exit(app.exec_())