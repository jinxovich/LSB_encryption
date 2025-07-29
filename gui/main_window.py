from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTextEdit, QFileDialog, QMessageBox, QWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from core.encoder import encode_image, save_encoded_image
from core.decoder import decode_image
from core.utils import is_valid_image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LSB Steganography")
        self.setGeometry(100, 100, 600, 400)

        self.main_layout = QVBoxLayout()

        self.image_label = QLabel("Drop image here")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setAcceptDrops(True)
        self.image_label.setStyleSheet("border: 2px dashed gray; min-height: 200px;")
        self.image_label.dropEvent = self.handle_drop_event
        self.image_label.dragEnterEvent = lambda event: event.accept() if event.mimeData().hasUrls() else event.ignore()

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Текст для шифровки/дешифровки")

        self.encode_button = QPushButton("Зашифровать")
        self.decode_button = QPushButton("Дешифровать")

        self.encode_button.clicked.connect(self.encode_image)
        self.decode_button.clicked.connect(self.decode_image)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.encode_button)
        button_layout.addWidget(self.decode_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.text_edit)
        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)

    def handle_drop_event(self, event):

        file_path = event.mimeData().urls()[0].toLocalFile()
        if is_valid_image(file_path):
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image_path = file_path
        else:
            QMessageBox.warning(self, "ошибка", "неверный формат файла")

    def encode_image(self):

        text = self.text_edit.toPlainText()
        if not text:
            QMessageBox.warning(self, "ошибка", "текст для шифрования")
            return

        if not hasattr(self, 'image_path'):
            QMessageBox.warning(self, "ошибка", "загрузите изображение.")
            return

        try:
            encoded_image = encode_image(self.image_path, text)
            save_path, _ = QFileDialog.getSaveFileName(self, "сохранить зашифрованное изображение", "", "Image Files (*.png *.jpg)")
            if save_path:
                save_encoded_image(encoded_image, save_path)
                QMessageBox.information(self, "успех", "изображение успешно зашифровано")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"произошла ошибка: {str(e)}")

    def decode_image(self):

        if not hasattr(self, 'image_path'):
            QMessageBox.warning(self, "ошибка", "загрузите изображение.")
            return

        try:
            decoded_text = decode_image(self.image_path)
            self.text_edit.setText(decoded_text)
            QMessageBox.information(self, "успех", "сообщение успешно расшифровано!")
        except Exception as e:
            QMessageBox.critical(self, "ошибка", f"произошла ошибка: {str(e)}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()