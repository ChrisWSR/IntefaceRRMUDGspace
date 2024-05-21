
import sys
import cv2
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
import numpy as np 
from Custom_Widgets import *
from detection-ros import Detection
#from detection4 import Detection
from resources_rc import *



"""
    CameraThread class represents a PyQt QThread responsible for capturing video frames from a camera,
    processing them using a Detection instance, and emitting the processed frames as QImage signals.

    Attributes:
        ImageUpdated (pyqtSignal): PyQt signal emitted when the processed frame is ready for display.
        container_size (QSize): Size of the container where the processed frame will be displayed.
        detection (Detection): An instance of the Detection class responsible for processing video frames.
"""
class CameraThread(QThread):
    ImageUpdated = pyqtSignal(QImage)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.container_size = None
        #self.ThreadActive = True  
        self.detection = Detection()
        # Connect the ImageUpdate signal of the Detection instance to the process_frame method of this class
        #self.detection.ImageUpdate.connect(self.process_frame)
        
        

    """
        The main execution method of the thread. Captures video frames, processes them using the Detection instance,
        and emits the processed frames as signals.

        Raises:
            RuntimeError: If there is an error opening the camera.
    """
    def run(self):
        self.ThreadActive = True
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise RuntimeError("Error opening the camera.")

            while self.ThreadActive:
                ret, frame = cap.read()
                if ret:
                    # Envía el frame capturado a Detection para su procesamiento
                    self.detection.process_frame(frame)
            cap.release()
        except Exception as e:
            print("An error occurred: {}".format(e))



    def stop(self):
        self.ThreadActive = False
        self.detection.stop_camera()
        self.quit()

    def disconnect_image_updated(self):
        self.ImageUpdated.disconnect()


    """
        Processes a video frame by converting it to RGB, performing horizontal flipping, adjusting its size,
        and emitting the processed frame as a QImage signal.

        Args:
            frame: Input video frame to be processed.
    """

    

    """
        Sets the size of the container where the processed frame will be displayed.

        Args:
            size: QSize object representing the size of the container.
    """
    def set_container_size(self, size):
        self.container_size = size



# Inserta esta función antes de la definición de la clase MainWindow
def numpy_to_qimage(image_np):
    if image_np.ndim == 3:
        h, w, ch = image_np.shape
        bytes_per_line = ch * w
        return QImage(image_np.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
    else:
        return None



########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("interface.ui",self)
        # Apply the file style.json
        loadJsonStyle(self, self.ui) 
        self.cameraThread = CameraThread()
        self.cameraThread.detection.ImageUpdate.connect(self.displayImage)
        self.turnOnCamera.clicked.connect(self.start_video)
        self.turnOffCamera.clicked.connect(self.stop_video)

    

    def start_video(self):
        #self.cameraThread.detection.ImageUpdate.connect(self.displayImage)
        self.cameraThread.set_container_size(self.cameraFramePage.size())
        self.cameraThread.start()
        self.cameraThread.detection.start()  # Inicia el hilo de detección


    def stop_video(self):
        self.cameraThread.stop()
        self.cameraThread.detection.stop_camera()  # Detiene el hilo de detección
        self.clearImage()   
    


    """
        Displays the provided QImage in a QLabel (cameraFramePage) by calculating the scaling factor
        to maintain the aspect ratio, scaling the image accordingly, and centering it within the QLabel.

        Args:
            Image: QImage to be displayed.
    """
    
    
    def displayImage(self, Image):
        if isinstance(Image, np.ndarray):  # Verifica si el objeto es un array de NumPy
            qimage = numpy_to_qimage(Image)  # Convierte el array de NumPy a QImage
        elif isinstance(Image, QImage):
            qimage = Image  # No es necesario convertir
        else:
            print("El objeto proporcionado no es una instancia de QImage ni un array de NumPy")
            return
        
        label_size = self.cameraFramePage.size()

        # Obtiene las dimensiones de la imagen y del contenedor
        image_width = qimage.width()
        image_height = qimage.height()
        container_width, container_height = label_size.width(), label_size.height()

        # Calcula el factor de escala para mantener la relación de aspecto
        width_ratio = container_width / image_width
        height_ratio = container_height / image_height
        scale_factor = min(width_ratio, height_ratio)

        # Escala la imagen proporcionalmente
        scaled_image = qimage.scaled(int(image_width * scale_factor), int(image_height * scale_factor), Qt.KeepAspectRatio)
        
        # Crea un pixmap y lo muestra en QLabel
        pixmap = QPixmap.fromImage(scaled_image)
        self.cameraFramePage.setPixmap(pixmap)
        self.cameraFramePage.setAlignment(Qt.AlignCenter)



    def clearImage(self):
        # Set an empty pixmap to clear the image
        self.cameraFramePage.setPixmap(QPixmap())
        QApplication.processEvents()

    



########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
