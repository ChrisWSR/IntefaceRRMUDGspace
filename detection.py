from ultralytics import YOLO
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np


"""
    A class for performing real-time object detection using YOLO model.

    Inherits:
        QThread: Allows the class to run in a separate thread.

    Signals:
        ImageUpdate: Signal emitted when a new annotated image is available for display.

    Attributes:
        ImageUpdate (pyqtSignal): Signal to update the UI with annotated images.
"""
class Detection(QThread):
    ImageUpdate = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.yolo_model = YOLO("weights/its.pt")
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(3, 640)
        self.video_capture.set(4, 640)

    def run(self):
        while True:
            ret, frame = self.video_capture.read()
            if ret:
                self._process_frame(frame)


    def process_frame(self, frame):
            detection_results = self.yolo_model.predict(frame, imgsz=640, conf=0.80)
            annotated_image = detection_results[0].plot()

            # Emits the annotated frame to update the UI
            self.ImageUpdate.emit(annotated_image)


         
