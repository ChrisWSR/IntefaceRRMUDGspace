from ultralytics import YOLO
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
from cv_bridge import CvBridge
import rospy
from sensor_msgs.msg import Image

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
        self.yolo_model = YOLO("hammer_bottle.pt")
        self.bridge = CvBridge()
        self.stopped = False
        rospy.init_node('nodo_suscriptor', anonymous=True)
        rospy.Subscriber("/zed2i/zed_node/rgb/image_rect_color", Image, self.callback_imagen)

    def callback_imagen(self, msg):
        if not self.stopped:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            frame = cv2.resize(frame, (640, 640))  # Resize the frame if necessary
            self.process_frame(frame)

    def run(self):
        rospy.spin()  # Keeps the node running

    def process_frame(self, frame):
        detection_results = self.yolo_model.predict(frame, imgsz=640, conf=0.25)
        annotated_image = detection_results[0].plot()

        # Emits the annotated frame to update the UI
        self.ImageUpdate.emit(annotated_image)
    
    def stop_camera(self):
        self.stopped = True
        self.quit()
        self.wait()

if __name__ == '__main__':
    detection = Detection()
    detection.start()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        detection.stop_camera()
        cv2.destroyAllWindows()
