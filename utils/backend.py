import requests
from datetime import datetime
from threading import Thread
from requests.exceptions import HTTPError
import json

from .send_telegram import send_telegram_mesg
from features.lifx import LIFX

def dict_to_list(data):
    return [val for (i, (key, val)) in enumerate(data.items())]

class Backend:
    def __init__(self, elapsed_time=10):
        self.tracker = {'angry' : 0, 'disgust' : 0, 'scared' : 0, 'happy' : 0,
            'sad' : 0, 'surprised' : 0, 'neutral' : 0}
        self.start_time = datetime.now()
        self.elapsed_time = 10 # Set elapsed time to 10s by default
        self.time_str = ''
        self.url = r'https://maker.ifttt.com/trigger/webhook_send_email/with/key/bnFflh0L430uryyw5YyEDx'
        self.chat_id = 0
        self.summary = [0]*len(self.tracker)
        self.send_data_flag = False
        self.threads = []

        try:
            self.lifx = LIFX(duration_secs=1) # Will produce error if no LIFX connected
        except ValueError:
            self.lifx = None


    def update_summary(self, top_emtn):
        temp = list(self.tracker).index(top_emtn)
        self.summary[temp] += 1
        return self.summary


    def get_elapsed_time(self):
        time = int(''.join(x for x in self.time_str if x.isdigit()))
        if "min" in self.time_str: # Only true if minutes
            time *= 60

        return time


    def record_label(self, label, app):
        # Update elapsed_time from time_str
        self.elapsed_time = self.get_elapsed_time()

        time_sec = (datetime.now() - self.start_time).total_seconds()
        if label == []: return self.summary #if no label, return the same value

        if(time_sec >= self.elapsed_time):
            self.start_time = datetime.now()
            self.send_data_flag = True
            self.lifx.change_colors(sleep_secs=1, smooth=True, seq='one',
                                    color_index=label[1])
            return self.check_and_send(app, time_sec)
        else:
            # Track predicted emotions
            self.tracker[label[0]] += 1
            return self.summary


    def check_and_send(self, app, time_sec):
        print("Period(s): {}".format(time_sec))
        TOP_EMOTION = max(self.tracker, key=self.tracker.get)
        self.tracker = {key:0 for key in self.tracker} #Reset tracker
        if app['table_lamp'] == True:
            t = Thread(target=self.activate_apps_thread, args=[app['table_lamp'], TOP_EMOTION, time_sec])
            t.start()
            self.threads.append(t)
        return self.update_summary(TOP_EMOTION)


    def activate_apps_thread(self, app, TOP_EMOTION, time_sec):
        self.process_ifttt(emotion=TOP_EMOTION)
        if self.chat_id is not 0:
            send_telegram_mesg(TOP_EMOTION, self.chat_id)


    def process_ifttt(self, emotion):
        print('To IFTTT data: {}'.format(emotion))
        try :
            response = requests.post(self.url, data={'value1':emotion})
            if response.status_code == 200: print("To IFTTT status: Success")
        except Exception as e:
            print('Send to IFTTT error: Are you connected to Internet?')
