#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
from threading import Thread, Timer
import datetime


class Notification_thread(object):

    def __init__(self, chats, api, delay):
        self.delay = delay
        self.api = api
        self.chats = chats
        self.thread = None
        self.polling = True
        self.last_check = None

    def run(self):
        if self.polling:
            self.thread = Timer(self.delay, self.poll, args = [self.chats, self.api])
            self.thread.start()


    def poll(self, chats, api):
        print("Last check was done: {}".format(self.last_check))
        for student_id in chats.chats.keys():
            student = chats.get_chat(student_id)
            print("Checking chat_id {}".format(student_id))
            if student['notifications']:
                print("This student has notifications activated")
                access_token = student['access_token']
                avisos = api.get_avisos(access_token)
                print("Got avisos")
                avisos = self.filter(avisos)
                print("Filtered avisos")
                print (list(avisos))
                self.last_check = datetime.datetime.now()
        self.run()


    def filter(self, avisos):
        for avis in avisos:
            avis_date = self.get_date(avis)
            if not self.last_check: yield avis
            elif avis_date > self.last_check: yield avis
            else: print("Pues te jodes")

    """
        2018-03-01T00:00:00 -> datetime(year, month, day, hour, minute, second)
    """
    def get_date(self, avis):
        avis_date = avis['data_modificacio']
        avis_date_day, avis_date_hour = avis_date.split('T')
        year, month, day = avis_date_day.split('-')
        hour, minute, second = avis_date_hour.split(':')
        return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))


    def datetime_2_json(self, date):
    	return {'day': date.day,
							'month': date.month,
							'year': date.year,
							'hour': date.hour,
							'minute': date.minute,
							'second': date.second}

    def stop_polling(self):
        self.polling = False

    def start_polling(self):
        self.polling = True
