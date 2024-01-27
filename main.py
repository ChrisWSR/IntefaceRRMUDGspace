import sys
import cv2
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication

from Custom_Widgets import *
from detection import Detection
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
        self.detection = Detection()
        # Connect the ImageUpdate signal of the Detection instance to 
        # the process_frame method of this class
        self.detection.ImageUpdate.connect(self.process_frame)


    """
        The main execution method of the thread. Captures video frames, processes them using the Detection instance,
        and emits the processed frames as signals.

        Raises:
            RuntimeError: If there is an error opening the camera.
    """
    def run(self):
        try:
            # Start the thread and set up video capture from the camera(ID 0)
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise RuntimeError("Error opening the camera.")

            while getattr(self, "thread", True):
                # Read a frame from the camera
                ret, frame = cap.read()
                if ret:
                    # Process the frame using the Detection instance
                    self.detection.process_frame(frame)
            cap.release()
        except Exception as e:
            print(f"An error occurred: {e}")


    """
        Processes a video frame by converting it to RGB, performing horizontal flipping, adjusting its size,
        and emitting the processed frame as a QImage signal.

        Args:
            frame: Input video frame to be processed.
    """
    def process_frame(self, frame):
        # Convert the BGR frame to RGB and perform horizontal flipping
        Image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        flipped_image = cv2.flip(Image_rgb, 1)

        # Adjust the size of the image based on the dimensions of the container
        qt_image = QImage(flipped_image.data, flipped_image.shape[1], flipped_image.shape[0], QImage.Format_RGB888)
        scaled_image = qt_image.scaled(self.container_size, Qt.IgnoreAspectRatio)
        self.ImageUpdated.emit(scaled_image)


    """
        Sets the size of the container where the processed frame will be displayed.

        Args:
            size: QSize object representing the size of the container.
    """
    def set_container_size(self, size):
        self.container_size = size






########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("interface.ui",self)
        # Apply the file style.json
        loadJsonStyle(self, self.ui)    


        self.detection = Detection()
        self.cameraThread = CameraThread(self.detection)

        self.turnOnCamera.clicked.connect(self.start_video)

    

    def start_video(self):
        self.detection.start()
        self.cameraThread.set_container_size(self.cameraFramePage.size())
        self.cameraThread.start()
        self.cameraThread.ImageUpdated.connect(self.displayImage)



    """
        Displays the provided QImage in a QLabel (cameraFramePage) by calculating the scaling factor
        to maintain the aspect ratio, scaling the image accordingly, and centering it within the QLabel.

        Args:
            Image: QImage to be displayed.
    """
    def displayImage(self, Image):
        label_size = self.cameraFramePage.size()
    
        # Get the dimensions of the image and the container
        image_size = Image.size()
        container_width, container_height = label_size.width(), label_size.height()
    
        # Calculate the scale to maintain the aspect ratio
        width_ratio = container_width / image_size.width()
        height_ratio = container_height / image_size.height()
        scale_factor = min(width_ratio, height_ratio)
    
        # Scale the image proportionally
        scaled_image = Image.scaled(image_size * scale_factor, Qt.KeepAspectRatio)
        
        # Calculate the area to center the image in the container
        x_offset = (container_width - scaled_image.width()) / 2
        y_offset = (container_height - scaled_image.height()) / 2
    
        # Create a pixmap and display it in the QLabel
        pixmap = QPixmap.fromImage(scaled_image)
        self.cameraFramePage.setPixmap(pixmap)
        self.cameraFramePage.setAlignment(Qt.AlignCenter)

    
    def closeEvent(self, event):
        self.detection.terminate()
        self.cameraThread.terminate()
        event.accept()
    



########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
