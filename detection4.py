from ultralytics import YOLO
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
import torch


class Detection(QThread):
    ImageUpdate = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.yolo_model = YOLO("best.pt")
        # Carga aquí el segundo modelo
        self.second_model = YOLO("kind.pt")
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(3, 640)
        self.video_capture.set(4, 480)
        self.stopped = False
        self.frame_counter = 0
        self.skip_frames = 5  # Procesa el frame cada 5 frame
        self.last_detections = []  # Almacena las últimas detecciones
        self.detection_lifetime = 4  # Detecciones permanecen visibles por este número de frames

    def run(self):
        while not self.stopped:
            ret, frame = self.video_capture.read()
            if ret:
                self.frame_counter += 1
                if self.frame_counter % self.skip_frames == 0:
                    self.process_frame(frame, new_detection=True)
                else:
                    self.process_frame(frame, new_detection=False)
        self.video_capture.release()

    def process_frame(self, frame, new_detection=True):
        if new_detection:
            detection_results = self.yolo_model.predict(frame, imgsz=640, conf=0.5)
            self.last_detections = [(detection, self.detection_lifetime) for detection in detection_results]
        else:
            self.last_detections = [(detection, life-1) for detection, life in self.last_detections if life > 0]

        for detection_obj, life in self.last_detections:
            for box in detection_obj.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                label_index = int(box.cls.item())
                label = detection_obj.names[label_index]
                confidence = box.conf.item() if isinstance(box.conf, torch.Tensor) else box.conf
                
                # Si detectamos una roca, usamos el segundo modelo para clasificar el tipo de roca
                if label.lower() == 'rock':
                    rock_image = frame[int(y1):int(y2), int(x1):int(x2)]
                    # Asume que tienes una función para clasificar el tipo de roca con el segundo modelo
                    rock_type = self.classify_rock_type(rock_image)
                    label = rock_type  # Actualiza la etiqueta con el tipo específico de roca

                text = f"{label}: {confidence:.2f}"
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                text_x = int(x1)
                text_y = int(y1) - 10 if int(y1) - 10 > 10 else int(y1) + 10
                cv2.rectangle(frame, (text_x, text_y - text_size[1] - 2), (text_x + text_size[0], text_y + 2), (0, 255, 0), -1)
                cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        self.ImageUpdate.emit(frame)


    def classify_rock_type(self, rock_image):
        # Convertir la imagen de BGR a RGB
        rgb_image = cv2.cvtColor(rock_image, cv2.COLOR_BGR2RGB)
        # Asegurarse de que la imagen está en el formato de 8 bits
        rgb_image = convert_to_8bit(rgb_image)

        # Redimensiona la imagen al tamaño esperado por el modelo
        resized_image = cv2.resize(rgb_image, (640, 640))

        # Realiza la inferencia utilizando el modelo ultralytics, asegurando que las entradas son correctas
        results_list = self.second_model(resized_image)
        if not results_list:
            return "Unknown"

        results = results_list[0]
        rock_type_index = results.probs.top1
        rock_type = results.names[rock_type_index]
        rock_type_confidence = results.probs.top1conf.item() if isinstance(results.probs.top1conf, torch.Tensor) else results.probs.top1conf

        return f"{rock_type}: {rock_type_confidence:.2f}"
    
    def stop_camera(self):
        self.stopped = True
        self.wait()

def preprocess_image(image):
    # Asumiendo que 'image' es un array de NumPy en formato BGR
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convertir BGR a RGB
    image = cv2.resize(image, (640, 640))  # Redimensionar imagen
    image = image / 255.0  # Normalizar si es necesario
    return image

def convert_to_8bit(image):
    # Convierte la imagen a 8 bits por canal
    if image.dtype == np.float64:  # CV_64F corresponde a numpy.float64
        # Escala los valores a 0-255 y convierte a uint8
        image = np.clip(image * 255.0, 0, 255).astype(np.uint8)
    return image




