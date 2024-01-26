from ultralytics import YOLO
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np

class Detection(QThread):
    ImageUpdate = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.model = YOLO("best.pt")
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 640)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            self.process_frame(frame)


    def process_frame(self, frame):
            resultados = self.model.predict(frame, imgsz=640, conf=0.25)
            anotaciones = resultados[0].plot()

            # Emite la señal para mostrar la imagen en la interfaz
            self.ImageUpdate.emit(anotaciones)
