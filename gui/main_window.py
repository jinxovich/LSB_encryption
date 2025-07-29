from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTextEdit, QFileDialog, QMessageBox, QWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.encoder import encode_image, save_encoded_image
from core.decoder import decode_image
from core.utils import is_valid_image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LSB Steganography")
        self.setGeometry(100, 100, 800, 600)
        self.image_path = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        
        self.image_label = QLabel("Загрузите изображение")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            border: 2px dashed gray; 
            min-height: 300px;
            background-color: #f0f0f0;
        """)
        self.image_label.setAcceptDrops(True)
        self.image_label.dragEnterEvent = self.dragEnterEvent
        self.image_label.dropEvent = self.dropEvent
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Введите текст для шифрования или нажмите 'Дешифровать' для извлечения")
        
        left_layout.addWidget(self.image_label, stretch=2)  
        left_layout.addWidget(self.text_edit, stretch=1)    

        right_layout = QVBoxLayout()
        self.encode_button = QPushButton("Зашифровать")
        self.decode_button = QPushButton("Дешифровать")
        
        self.encode_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.decode_button.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 10px;")
        
        self.encode_button.setFixedWidth(150)
        self.decode_button.setFixedWidth(150)
        self.encode_button.setFixedHeight(50)
        self.decode_button.setFixedHeight(50)
        
        self.encode_button.clicked.connect(self.encode_image)
        self.decode_button.clicked.connect(self.decode_image)
        
        right_layout.addWidget(self.encode_button)
        right_layout.addWidget(self.decode_button)
        right_layout.addStretch()
        
        button_container = QWidget()
        button_container.setLayout(right_layout)
        button_container.setStyleSheet("padding: 20px;")

        main_layout.addLayout(left_layout, stretch=3) 
        main_layout.addWidget(button_container, stretch=1) 
        central_widget.setLayout(main_layout)

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            if is_valid_image(file_path):
                pixmap = QPixmap(file_path)
                self.image_label.setPixmap(pixmap.scaled(
                    self.image_label.size(), 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                ))
                self.image_path = file_path
                self.image_label.setText("")  
            else:
                QMessageBox.warning(self, "ошибка", "неверный формат файла")
        event.accept()

    def encode_image(self):
        if not self.image_path:
            QMessageBox.warning(self, "ошибка", "загрузите изображение")
            return

        text = self.text_edit.toPlainText()
        if not text:
            QMessageBox.warning(self, "ошибка", "введите текст для шифрования.")
            return

        try:
            encoded_image = encode_image(self.image_path, text)
            
            save_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Сохранить зашифрованное изображение", 
                "", 
                "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)"
            )
            
            if save_path:
                save_encoded_image(encoded_image, save_path)
                QMessageBox.information(self, "успех", "изображение успешно зашифровано")
        except Exception as e:
            QMessageBox.critical(self, "ошибка", f"произошла ошибка при шифровании: {str(e)}")

    def decode_image(self):
        if not self.image_path:
            QMessageBox.warning(self, "ошибка", "загрузите изображение.")
            return

        try:
            decoded_text = decode_image(self.image_path)
            self.text_edit.setText(decoded_text)
            QMessageBox.information(self, "цспех", "сообщение успешно расшифровано!")
        except Exception as e:
            QMessageBox.critical(self, "ошибка", f"произошла ошибка при дешифровании: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())