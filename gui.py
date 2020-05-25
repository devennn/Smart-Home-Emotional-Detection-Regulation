import cv2
import numpy as np
import random
from datetime import datetime
from utils import Plot_Graph

from gui_window import setup_window
from middleware import manage_features

import PySimpleGUI as sg
sg.theme('Material2')
sg.change_look_and_feel('Dark Blue 3')

start_time = datetime.now() # Indicating program start for summary update

# Scale to value between 0-500
def scale(preds):
    return np.interp(preds, (preds.min(), preds.max()), (0, 500))

def frame_to_bytes(frame):
    return cv2.imencode('.png', frame)[1].tobytes()

def wait_thread(threads):
    for t in threads: t.join()

def stop_task(data, window):
    print("App LIFX: Reset original color")
    data["backend"].lifx.reset_original()
    # Reset all threads
    wait_thread(data['backend'].threads)
    data['backend'].threads = []
    # Create White image and update window
    window['image'].update(data=frame_to_bytes(np.full((240, 320), 0)))

def main():
    g = Plot_Graph()
    graph = g.graph()

    data = {}

    # Init camera
    data['fps'] = 5
    data['width'] = 320
    data['height'] = 240
    data['cap'] = manage_features(data, 'init_camera')

    # Init emotion recognition
    data['system'] = manage_features(data, 'init_emotions')
    EMOTIONS = data['system'].EMOTIONS
    emotion_class_len = len(EMOTIONS)

    # Init backend
    data['time'] = 60
    data['backend'] = manage_features(data, job='init_backend')

    # Setup required variable
    app = {'table_lamp':False, 'bed_light':False, 'tv':False, 'front_door':False,
            'garage':False, 'fridge':False}
    data['app'] = app
    data['time'] = 0
    running = False
    view_data = 'Real-Time'
    last_vals = np.zeros(emotion_class_len)
    emotn_summary = [0]*emotion_class_len

    # Start GUI
    window = setup_window(graph)

    # Main loop
    while True:
        event, values = window.read(timeout=20)
        # Button state checker
        if event == 'Exit' or event is None:
            data["backend"].lifx.reset_original()
            wait_thread(data['backend'].threads)
            data['cap'].release()
            cv2.destroyAllWindows()
            return
        elif event == 'Start':
            running = True
        elif event == 'Stop':
            running = False
            stop_task(data, window)
        elif event == 'Real-Time':
            view_data = 'Real-Time'
        elif event == 'Summary':
            view_data = 'Summary'
        elif event == 'Connect':
            if values['chat_id']:
                data['backend'].chat_id = values['chat_id']
                print("Connected to Telegram: ID: {}".format(data['backend'].chat_id))
            else:
                print("No chat id")

        # Check and change app state
        if values['table_lamp']:
            if app['table_lamp'] is False: print("Connected: Table Lamp") # Print once
            app['table_lamp'] = True
        elif values['table_lamp'] == False:
            if app['table_lamp'] is True: print("Disconnected: Table Lamp") # Print once
            app['table_lamp'] = False

        # Run if running button is pressed
        if running:
            data['time'] = values['time']
            frame, preds, emotn_summary = manage_features(data, job='detect_emotion')
            window['image'].update(data=frame_to_bytes(frame))

            graph.erase()
            if view_data == 'Real-Time':
                to_plot = scale(preds)
                if sum(to_plot) == emotion_class_len*500:
                    to_plot = last_vals
                else:
                    last_vals = to_plot
            elif view_data == 'Summary':
                if sum(emotn_summary) == 0:
                    to_plot = emotn_summary
                else:
                    to_plot = scale(np.array(emotn_summary))

            for i in range(emotion_class_len):
                graph = g.update_value(graph, to_plot[i], i, EMOTIONS[i])

if __name__ == '__main__':
    main()
