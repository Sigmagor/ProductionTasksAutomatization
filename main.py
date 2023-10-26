import os
import socket
from random import sample

import cv2
from PIL import Image
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from pyzbar.pyzbar import decode

from support import *

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


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Camera App")
        self.setFixedSize(300, 300)
        self.camera_label = QLabel(self)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.snapshot_button = QPushButton("Take Snapshot", self)
        self.snapshot_button.clicked.connect(self.take_snapshot)
        layout = QVBoxLayout()
        layout.addWidget(self.camera_label)
        layout.addWidget(self.snapshot_button)
        self.setLayout(layout)
        self.camera_thread = CameraThread()
        self.camera_thread.frame_signal.connect(self.update_camera_image)
        self.snapshot = None
        self.camera_thread.start()

    def update_camera_image(self, image):
        self.camera_label.setPixmap(QPixmap.fromImage(image))

    def take_snapshot(self):
        frame = self.camera_label.pixmap().toImage()
        if not frame.isNull():
            self.snapshot = QPixmap.fromImage(frame)
            self.save_snapshot()

    def save_snapshot(self):
        global sp
        if self.snapshot is not None:
            directory = "Hackathon"
            project_path = "C:/Users/asus/PycharmProjects/Hackaton"
            hackathon_dir = os.path.join(project_path, directory)
            if not os.path.exists(hackathon_dir):
                os.makedirs(hackathon_dir)
            name = f"{''.join(sample(alphabet, 3))}.png"
            file_path = os.path.join(hackathon_dir, name)
            self.snapshot.save(file_path)
            decoded_text = decode(Image.open(f"Hackathon/{name}"))
            print(decoded_text)
            try:
                number = str(decoded_text[0]).split(":")[2]
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                broadcast_address = '<ip_address>'
                port = 4553
                message = number
                print(decoder(message))
                try:
                    sock.sendto(decoder(message), (broadcast_address, port))
                    print("Широковещательный запрос отправлен")
                    while True:
                        data, addr = sock.recvfrom(1024)
                        print(f"Получен ответ от устройства {addr}: {data.decode()}")
                except OSError as e:
                    print(f"Ошибка при отправке запроса: {e}")
                finally:
                    sock.close()
            finally:
                os.remove(f"Hackathon/{name}")

    def closeEvent(self, event):
        self.camera_thread.stop()
        super(MainWindow, self).closeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
