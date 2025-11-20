import sys
import cv2
import numpy as np
import socket
import threading
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer

# ======= Configuración de red =======
PORT = 5001
BUFFER_SIZE = 65535

# ======= Interfaz principal =======
class VideoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Videollamada - Quadtrees & RLE")
        self.setGeometry(100, 100, 800, 600)

        # Elementos de la interfaz
        self.ip_label = QLabel("IP del receptor:")
        self.ip_input = QLineEdit("127.0.0.1")
        self.start_btn = QPushButton("Iniciar transmisión")
        self.stop_btn = QPushButton("Detener transmisión")
        self.video_label = QLabel("Vista previa de video local")
        self.video_label.setFixedSize(640, 480)

        # Layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.ip_label)
        hbox.addWidget(self.ip_input)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.start_btn)
        vbox.addWidget(self.stop_btn)
        vbox.addWidget(self.video_label)
        self.setLayout(vbox)

        # Cámara
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False

        # Conexiones
        self.start_btn.clicked.connect(self.start_stream)
        self.stop_btn.clicked.connect(self.stop_stream)

        # Hilo para recibir video remoto
        threading.Thread(target=self.receive_video, daemon=True).start()

    # ======= Transmisión =======
    def start_stream(self):
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

    def stop_stream(self):
        self.running = False
        self.timer.stop()
        if self.cap:
            self.cap.release()

    def update_frame(self):
        if not self.running or not self.cap:
            return
        ret, frame = self.cap.read()
        if not ret:
            return

        # Compresión (simulada)
        _, encoded = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        self.sock.sendto(encoded, (self.ip_input.text(), PORT))

        # Mostrar video local
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        qt_img = QImage(rgb_image.data, w, h, ch * w, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_img))

    # ======= Recepción =======
    def receive_video(self):
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_sock.bind(("0.0.0.0", PORT))
        print(f"Escuchando video en puerto {PORT}...")
        while True:
            packet, _ = recv_sock.recvfrom(BUFFER_SIZE)
            npdata = np.frombuffer(packet, np.uint8)
            frame = cv2.imdecode(npdata, cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow("Video remoto", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

# ======= MAIN =======
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoApp()
    window.show()
    sys.exit(app.exec())
