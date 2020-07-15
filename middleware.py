import cv2
from features import Emotions
from utils import Backend

def manage_features(data, job):

    if job == 'init_emotions':
        return Emotions(data['cap'])

    elif job == 'init_camera':
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, data['fps'])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, data['width'])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, data['height'])
        return cap

    elif job == 'init_backend':
        return Backend(data['time'])

    elif job == 'detect_emotion':
        label = ''
        frame, preds, label = data['system'].run_window()
        data['backend'].time_str = data['time'] # Update new elapsed_time
        emotn_summary = data['backend'].record_label(label, data['app'])
        return frame, preds, emotn_summary
