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

    def run(self):
        if self.polling:
            self.thread = Timer(self.delay, self.poll, args = [self.chats, self.api])
            self.thread.start()


    def poll(self, chats, api):
        for student_id in chats.chats.keys():
            student = chats.get_chat(student_id)
            if student['notifications']:
                access_token = chats.get_chat(student)['access_token']
                avisos = api.get_avisos(access_token)
                print("Got avisos")
                avisos = self.filter(avisos, student['last_notif_polling'])
                print("Filtered avisos")
                print (avisos)
                chats.update_chat(student_id, {'last_notif_polling': datetime.now()}, compulsory = True, full_data = False)
        self.run()


    def filter(self, avisos, date):
        for avis in avisos:
            avis_date = self.get_date(avis)
            if not date: yield avis
            elif avis_date > date: yield avis
            else: print("Pues te jodes")

    """
        2018-03-01T00:00:00 -> datetime(year, month, day, hour, minute, second)
    """
    def get_date(self, avis):
        avis_date = avis['data_modificacio']
        avis_date_day, avis_date_hour = avis_date.split('T')
        year, month, day = avis_date_day.split('-')
        hour, minute, second = avis_date_hour.split(':')
        return datetime.datetime(year, month, day, hour, minute, second)




    def stop_polling(self):
        self.polling = False

    def start_polling(self):
        self.polling = True

"""
threads = []
def thread_func(seconds, chat_id):
	sleep(seconds)
	refresh_token(chat_id)
def schedule_refreshment(chat_id):
	expire_time_end = db_module.get_chat(chat_id)['expire_time_end']
	expire_time_end = datetime.datetime(expire_time_end['year'],
										expire_time_end['month'],
										expire_time_end['day'],
										expire_time_end['hour'],
										expire_time_end['minute'],
										expire_time_end['second'])
	actual_time = datetime.datetime.now()
	delay = (expire_time_end-actual_time).total_seconds()
	print("delay is %s"%str(delay))
	thread = Thread(target = thread_func, args = [delay, chat_id])
	thread.start()
	threads.append(thread)
"""
