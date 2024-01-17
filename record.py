import cv2
import numpy as np
import time
from datetime import datetime

class CCTV:
    def __init__(self, video_source=0):
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise ValueError("Unable to open video source", video_source)
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2()
        self.contour_area_threshold = 10000  # Minimum contour area to detect motion
        self.is_recording = False
        self.out = None
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def get_frame(self):
        ret, frame = self.cap.read()
        return frame

    def detect_motion(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fg_mask = self.background_subtractor.apply(gray)
        _, thresh = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) > self.contour_area_threshold:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                motion_detected = True

        return motion_detected, frame

    def detect_and_save_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face_image = frame[y:y+h, x:x+w]
            timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            cv2.imwrite(f'face_{timestamp_str}.png', face_image)

    def start(self):
        while True:
            frame = self.get_frame()
            motion_detected, annotated_frame = self.detect_motion(frame)

            # Add date and time to the frame
            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(annotated_frame, timestamp_str, (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if motion_detected:
                time.sleep(0.01)  # Delay before starting recording
                if not self.is_recording:
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    self.out = cv2.VideoWriter(f'output_{timestamp_str}.avi', fourcc, 5.0, (640, 480))
                    self.is_recording = True
                self.out.write(frame)
                self.detect_and_save_faces(frame)
            else:
                if self.is_recording:
                    self.out.release()
                    self.is_recording = False

            cv2.imshow('Motion Detection', annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        if self.is_recording:
            self.out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # This code will only run if record.py is run directly
    record = CCTV()
    record.start()