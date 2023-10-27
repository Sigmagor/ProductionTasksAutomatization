from main import *
from random import sample
import cv2
import os
from PIL import Image
from pyzbar.pyzbar import decode
import socket
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush
from PyQt5.QtGui import QImage, QPixmap

sp = []
alphabet = ['q', 'a', 'z', 'x', 's', 'w', 'e', 'd', 'c', 'v', 'f', 'r', 't', 'g', 'b', 'n', 'h', 'y', 'u', 'j', 'm',
            'k', 'i', 'o', 'l', 'p', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'ё', 'й', 'ф', 'я', 'ч', 'ы',
            'ц', 'у', 'в', 'с', 'м', 'а', 'к', 'е', 'п', 'и', 'т', 'р', 'н', 'г', 'о', 'ь', 'б', 'л', 'ш', 'щ', 'щ',
            'д', 'ю', 'ж', 'з', 'х', 'э', 'ъ']


class CameraThread(QThread):
    frame_signal = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super(CameraThread, self).__init__(parent)
        self.camera_id = 0
        self.is_running = False

    def run(self):
        self.is_running = True
        cap = cv2.VideoCapture(self.camera_id)
        while self.is_running:
            ret, frame = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                image_qt = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.frame_signal.emit(image_qt)

        cap.release()

    def stop(self):
        self.is_running = False
        self.wait()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.second_form = None
        self.setWindowTitle("Пример PyQt5")
        self.setFixedSize(450, 900)
        self.setGeometry(100, 100, 450, 900)

        palette = self.palette()
        pixmap = QPixmap("img_1.png")
        scaled_pixmap = pixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.IgnoreAspectRatio)
        palette.setBrush(QPalette.Background, QBrush(scaled_pixmap))
        self.setPalette(palette)

        self.button = QPushButton(self)
        self.button.setText("")
        self.button.clicked.connect(self.enter)
        self.button.setGeometry(188, 659, 2 * 37, 2 * 37)
        self.button.setStyleSheet(
            f"QPushButton {{ border-radius: {37}px; background-color: white; color: white; font-size: 20px; }}")

    def enter(self):
        self.second_form = SecondForm()
        self.second_form.show()


class SecondForm(QWidget):
    def __init__(self):
        super().__init__()
        self.snapshot = None
        self.initUI()

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("Camera App")
        self.setFixedSize(450, 900)
        self.setGeometry(600, 100, 450, 900)
        self.camera_label = QLabel(self)
        self.camera_label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.camera_label)
        self.setLayout(layout)

        self.camera_thread = CameraThread()
        self.camera_thread.frame_signal.connect(self.update_camera_image)
        self.camera_thread.start()
        self.snapshot = None

        self.button = QPushButton(self)
        self.button.setText("")
        self.button.setGeometry(175, 670, 2 * 52, 2 * 52)
        self.button.setStyleSheet(
            f"QPushButton {{ border-radius: {37}px; background-color: white; color: white; font-size: 20px; }}")
        self.button.clicked.connect(self.take_snapshot)
        palette = self.palette()
        pixmap = QPixmap("img_4.png")
        scaled_pixmap = pixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.IgnoreAspectRatio)
        palette.setBrush(QPalette.Background, QBrush(scaled_pixmap))
        self.setPalette(palette)
        self.button1 = QPushButton(self)
        self.button1.setText("Посмотреть историю запросов")
        self.button1.setGeometry(175, 800, 2 * 104, 2 * 26)
        self.button1.clicked.connect(self.enter1)

    def enter1(self):
        self.third_form = ThirdForm()
        self.third_form.show()

    def update_camera_image(self, frame):
        resized_frame = frame.scaled(300, 300, Qt.AspectRatioMode.IgnoreAspectRatio)
        self.camera_label.setPixmap(QPixmap.fromImage(resized_frame))

    def take_snapshot(self):
        frame = self.camera_label.pixmap().toImage()
        if not frame.isNull():
            self.snapshot = QPixmap.fromImage(frame)
            self.save_snapshot()

    def save_snapshot(self):
        global sp
        if self.snapshot is not None:
            directory = "Hackathon"
            project_path = "C:/Users/asus/PycharmProjects/Hackaton"  # Замените на путь к вашему проекту

            # Проверяем, существует ли папка "Hackathon" в проекте
            hackathon_dir = os.path.join(project_path, directory)
            if not os.path.exists(hackathon_dir):
                os.makedirs(hackathon_dir)

            name = f"{''.join(sample(alphabet, 3))}.png"
            # Получаем полный путь и имя файла для сохранения изображения
            file_path = os.path.join(hackathon_dir, name)

            # file_path, _ = QFileDialog.getSaveFileName(self, "Save Snapshot", hackathon_dir, "Images (*.png)")
            self.snapshot.save(file_path)

            decoded_text = decode(Image.open(f"Hackathon/{name}"))
            print(decoded_text)
            try:
                number = str(decoded_text[0]).split(":")[2]
                message = number
                with open('txt.txt', 'w', encoding='utf8') as f:
                    f.write(str(decoder(message)))

                print(decoder(message))

            except IndexError:
                pass

            os.remove(f"Hackathon/{name}")

class ThirdForm(QWidget):
    def __init__(self):
        super().__init__()
        self.snapshot = None
        self.initUI()


    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("Camera App")
        self.setFixedSize(450, 900)
        self.setGeometry(1100, 100, 450, 900)
        palette = self.palette()
        pixmap = QPixmap("img_7.png")
        scaled_pixmap = pixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.IgnoreAspectRatio)
        palette.setBrush(QPalette.Background, QBrush(scaled_pixmap))
        self.setPalette(palette)
        self.label = QLabel()
        f = open('txt.txt', 'r')
        self.label.setText(f.readlines()[0])
        self.label.setGeometry(350, 200, 100, 100)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec())
