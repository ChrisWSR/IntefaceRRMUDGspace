from ultralytics import YOLO
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
from openvino.inference_engine import IECore


class Detection(QThread):
    ImageUpdate = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        # Inicializar el runtime de inferencia de OpenVINO
        self.ie = IECore()
        
        # Cargar el modelo de detección de rocas
        self.rock_detection_model = self.ie.read_network(model="weights/its.xml", weights="weights/its.bin")
        self.rock_detection_exec_model = self.ie.load_network(network=self.rock_detection_model, device_name="CPU", num_requests=1)
        
        # Cargar el modelo de clasificación de rocas
        self.rock_classification_model = self.ie.read_network(model="weights/kind.xml", weights="weights/kind.bin")
        self.rock_classification_exec_model = self.ie.load_network(network=self.rock_classification_model, device_name="CPU", num_requests=1)

        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(3, 640)
        self.video_capture.set(4, 640)

    def run(self):
        while True:
            ret, frame = self.video_capture.read()
            if ret:
                self.process_frame(frame)

    def process_frame(self, frame):
        # Realiza la detección de rocas
        # Necesitarás adaptar este código para trabajar con tu modelo específico y formato de datos
        input_blob = next(iter(self.rock_detection_exec_model.input_info))
        output_blob = next(iter(self.rock_detection_exec_model.outputs))
        n, c, h, w = self.rock_detection_exec_model.input_info[input_blob].tensor_desc.dims
        
        # Preparar el frame
        frame_processed = cv2.resize(frame, (w, h))
        frame_processed = frame_processed.transpose((2, 0, 1))  # Cambiar de HWC a CHW
        frame_processed = np.expand_dims(frame_processed, axis=0)
        
        # Inferencia
        detection_results = self.rock_detection_exec_model.infer({input_blob: frame_processed})
        
        # Procesar los resultados de detección...
        # Asumiendo que tienes los resultados, recorta las rocas detectadas
        
        for rock in detected_rocks:  # Aquí necesitas iterar sobre tus rocas detectadas
            # Preparar el recorte de la roca para clasificación
            rock_crop = # Código para recortar la roca basado en detecciones
            
            # Clasificación de la roca
            classification_input_blob = next(iter(self.rock_classification_exec_model.input_info))
            rock_crop_processed = # Código para preparar el recorte para clasificación
            
            classification_results = self.rock_classification_exec_model.infer({classification_input_blob: rock_crop_processed})
            
            # Procesar los resultados de clasificación...
        
        # Actualizar UI con los resultados
        # self.ImageUpdate.emit(annotated_image con clasificaciones)
