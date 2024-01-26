import sys
import cv2
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication

from Custom_Widgets import *
from detection import Detection
from resources_rc import *



class Work(QThread):
    Imageupd = pyqtSignal(QImage)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.container_size = None
        self.detection_instance = Detection()
        self.detection_instance.ImageUpdate.connect(self.process_frame)

    def run(self):
        self.thread = True
        cap = cv2.VideoCapture(0)
        while self.thread:
            ret, frame = cap.read()
            if ret:

                self.detection_instance.process_frame(frame)


               # Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
               # flip = cv2.flip(Image, 1)
                
                # Ajusta el tamaño de la imagen según las dimensiones del contenedor
               # convert_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format_RGB888)
               # pic = convert_QT.scaled(self.container_size, Qt.IgnoreAspectRatio)
               # self.Imageupd.emit(pic)
    

    def process_frame(self, frame):
        Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        flip = cv2.flip(Image, 1)

        # Ajusta el tamaño de la imagen según las dimensiones del contenedor
        convert_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format_RGB888)
        pic = convert_QT.scaled(self.container_size, Qt.IgnoreAspectRatio)
        self.Imageupd.emit(pic)


    def set_container_size(self, size):
        self.container_size = size




########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("interface.ui",self)

        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################

        loadJsonStyle(self, self.ui)    
        ########################################################################

        self.detection_instance = Detection()
        self.Work = Work(self.detection_instance)

        #detection.ImageUpdate.connect(self.show_image)
        self.turnOnCamera.clicked.connect(self.start_video)
        #self.cameraFramePage.show.(Work)
        

        ########################################################################
    def start_video(self):
        self.detection_instance.start()
        self.Work.set_container_size(self.cameraFramePage.size())
        self.Work.start()
        

       # self.Work.start()
        self.Work.Imageupd.connect(self.Imageupd_slot)

    def Imageupd_slot(self, Image):
        label_size = self.cameraFramePage.size()
    
        # Obtiene las dimensiones de la imagen y el contenedor
        image_size = Image.size()
        container_width, container_height = label_size.width(), label_size.height()
    
        # Calcula la escala para mantener la relación de aspecto
        width_ratio = container_width / image_size.width()
        height_ratio = container_height / image_size.height()
        scale_factor = min(width_ratio, height_ratio)
    
        # Escala la imagen proporcionalmente
        scaled_image = Image.scaled(image_size * scale_factor, Qt.KeepAspectRatio)
        
        # Calcula el área para centrar la imagen en el contenedor
        x_offset = (container_width - scaled_image.width()) / 2
        y_offset = (container_height - scaled_image.height()) / 2
    
        # Crea un pixmap y lo muestra en el QLabel
        pixmap = QPixmap.fromImage(scaled_image)
        self.cameraFramePage.setPixmap(pixmap)
        self.cameraFramePage.setAlignment(Qt.AlignCenter)
    
    def closeEvent(self, event):
        self.detection.terminate()
        self.Wor.terminate()
        event.accept()
    


########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    window = MainWindow()
 #   window.show()
 #   sys.exit(app.exec_())
    
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

########################################################################
## END===>
########################################################################  
