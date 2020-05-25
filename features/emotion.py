import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

class Emotions:
    def __init__(self, camera):
        self.camera = camera
        self.face_detection = cv2.CascadeClassifier(
                                'haarcascade_frontalface_default.xml')
        self.emotion_classifier = load_model('_model.68-0.64.hdf5',
                                                compile=False)
        self.EMOTIONS = ["angry", "disgust", "scared", "happy", "sad",
                        "surprised", "neutral"]

    def run_window(self):
        label = []
        faces, gray, frame = self.get_frame_data()
        preds = np.zeros(len(self.EMOTIONS))
        if len(faces) > 0:
            faces = self.sort_faces(faces)
            roi, fX, fY, fW, fH = self.extract_roi(gray, faces[0])
            preds = self.emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = [self.EMOTIONS[preds.argmax()], preds.argmax()]

            cv2.putText(frame, label[0], (fX, fY - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            cv2.rectangle(frame, (fX, fY), (fX + fW, fY + fH),
                          (0, 0, 255), 2)

        # Resize for display
        return cv2.resize(frame, (320, 240)), preds, label

    def sort_faces(self, faces):
        return sorted(faces, reverse=True, key=lambda x:(x[2] - x[0])*(x[3] - x[1]))

    def get_frame_data(self):
        frame = self.camera.read()[1]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.get_face(gray)

        return faces, gray, frame

    def get_face(self, gray):
        return self.face_detection.detectMultiScale(gray, scaleFactor=1.1,
                    minNeighbors=5, minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE)

    def extract_roi(self, gray, face):
        """
        Extract the ROI of the face from the grayscale image,
        resize it to a fixed 48x48 pixels, and then prepare
        the ROI for classification via the CNN
        """
        (fX, fY, fW, fH) = face
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (48, 48)) # Resize to fit Model input size
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        return roi, fX, fY, fW, fH
