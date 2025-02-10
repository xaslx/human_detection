import os
import time
from datetime import datetime

import cv2
import mediapipe as mp

from src.routers.events import add_photo_event
from src.services.photos import BasePhotosService


class HumanDetection:
    def __init__(
        self,
        x_min: int,
        y_min: int,
        x_max: int,
        y_max: int,
        photos_service: BasePhotosService | None = None,
    ):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils

        self.camera = None
        self.pose = None
        self.person_in_frame_time = 0
        self.person_in_frame = False
        
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        
        self.is_running = False
        
        self.photos_service = photos_service

    def start(self):
        if not self.is_running:
            self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
            self.camera = cv2.VideoCapture(0)
            self.is_running = True
            self._detect_person()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.camera.release()

    def _detect_person(self):
        while self.is_running:
            ret, frame = self.camera.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame_rgb)

            if results.pose_landmarks:
                h, w, _ = frame.shape
                x_min = w
                y_min = h
                x_max = y_max = 0

                for lm in results.pose_landmarks.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)
                    x_min = min(x_min, x)
                    y_min = min(y_min, y)
                    x_max = max(x_max, x)
                    y_max = max(y_max, y)

                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 3)
                
                if x_min < w and y_min < h and x_max > 0 and y_max > 0:
                    if not self.person_in_frame:
                        self.person_in_frame = True
                        self.person_in_frame_time = time.time()
                else:
                    self.person_in_frame = False
                    self.person_in_frame_time = 0

                if self.person_in_frame and time.time() - self.person_in_frame_time >= 5:
                    os.makedirs('src/static/photos', exist_ok=True)
                    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    filename = f'photo_{timestamp}.jpg'
                    file_path = os.path.join('src/static/photos', filename)

                    cv2.imwrite(file_path, frame)
                    self.photos_service.save_photo(filename=file_path, timestamp=timestamp)
                    add_photo_event(file_path)

                    self.person_in_frame_time = 0
                    self.person_in_frame = False

            else:
                self.person_in_frame = False
                self.person_in_frame_time = 0

            cv2.waitKey(1)