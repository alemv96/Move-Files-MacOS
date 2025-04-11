#Author: Alejandro Veloz
#Description: MAC finder sucks, this app will allow MAC user to move files in an easier way, 
#just like file explorer allows you. 

import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QFileDialog, QMessageBox, QListWidgetItem
)

class FileMoverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Mover App")
        self.setGeometry(100, 100, 600, 400)

        self.source_folder = ""
        self.dest_folder = ""

        self.layout = QVBoxLayout()

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.MultiSelection)

        self.select_source_btn = QPushButton("Select Source Folder")
        self.select_dest_btn = QPushButton("Select Destination Folder")
        self.move_btn = QPushButton("Move Selected Files")

        self.select_source_btn.clicked.connect(self.select_source)
        self.select_dest_btn.clicked.connect(self.select_dest)
        self.move_btn.clicked.connect(self.move_files)

        self.layout.addWidget(self.file_list)
        self.layout.addWidget(self.select_source_btn)
        self.layout.addWidget(self.select_dest_btn)
        self.layout.addWidget(self.move_btn)

        self.setLayout(self.layout)

    def select_source(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.source_folder = folder
            self.load_files()

    def select_dest(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.dest_folder = folder

    def load_files(self):
        self.file_list.clear()
        if self.source_folder:
            for file in os.listdir(self.source_folder):
                full_path = os.path.join(self.source_folder, file)
                if os.path.isfile(full_path):
                    item = QListWidgetItem(file)
                    self.file_list.addItem(item)

    def move_files(self):
        if not self.source_folder or not self.dest_folder:
            QMessageBox.warning(self, "Missing Info", "Please select both source and destination folders.")
            return

        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Files Selected", "Please select at least one file.")
            return

        for item in selected_items:
            file_name = item.text()
            src_path = os.path.join(self.source_folder, file_name)
            dest_path = os.path.join(self.dest_folder, file_name)

            try:
                shutil.move(src_path, dest_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not move {file_name}.\n{e}")

        self.load_files()
        QMessageBox.information(self, "Success", "Files moved successfully.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileMoverApp()
    window.show()
    sys.exit(app.exec_())
