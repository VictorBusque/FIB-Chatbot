#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
from threading import Timer
import datetime
from pprint import pprint

#-- Local imports --#
from Fibot.Data.data_types.notification import Notification
from Fibot.api.api_raco import API_raco
from Fibot.api.oauth import Oauth
from Fibot.chats import Chats


class Refresh_token_thread(object):

    """This class enables multithreading capabilities by using an extra thread to scan looking for
    chats with expired tokens to refresh.

        Attributes:
            oauth(:class:`Fibot.api.oauth.Oauth`): Object that manages the oauth processes.
            chats(:class:`Fibot.chats.Chats`): Chat records of users.
            delay(:obj:`int`): Amount of seconds between scans.
            queue(:obj:`list`): Lists of chat_id's of the people with tokens to be refreshed.
            thread(:class:`threading.Timer`): Thread that does the scanning.
            polling(:obj:`bool`): Object that indicates if polling has to be done.
    """
    def __init__(self, delay):
        self.oauth = Oauth()
        self.chats = Chats()
        self.delay = delay
        self.queue = []
        self.polling = True
        self.thread = None

    """
        Updates the internal representation of the chats with the last dumped values.
    """
    def update_chats(self):
        self.chats.load()
        self.queue = self.chats.get_expired_chats()

    """
        This function defines the new timer and starts it (effectively allows the scanning)
    """
    def run(self, initial_offset = 0):
        if self.polling:
            self.thread = Timer(self.delay - initial_offset, self.poll)
            self.thread.start()

    """
        Does a scan over all users with expired tokens, and then returns to the activation function
    """
    def poll(self):
        print("Refresh token thread: Refreshing tokens\n")
        self.update_chats()
        for chat in self.queue:
            print("Refresh token thread: Refreshing token for {}\n".format(self.chats.get_chat(chat)['name']))
            refresh_token = self.chats.get_chat(chat)['refresh_token']
            callback = self.oauth.refresh_token(refresh_token)
            if not callback: print ("Something is wrong with this refreshment")
            print("This is the callback from refreshment {}".format(callback))
            if callback: self.chats.update_chat(chat, data = callback, full_data = False)
            if callback: print("Refresh token thread: Refreshed token successfully!\n")
        self.queue = []
        self.run()

    """
        Allows polling
    """
    def stop_polling(self):
        self.polling = False

    """
        Forbids polling
    """
    def start_polling(self):
        self.polling = True
        self.run()


class Notification_thread(object):

    """This class enables multithreading capabilities by using an extra thread to scan looking for
    notifications for users.

        Attributes:
            api(:class:`Fibot.api.api_raco.API_raco`): Object that accesses the info at Raco's API_raco
            message_handler(:class:`Fibot.message_handler.Message_handler`): Object that allows interaction with users
            chats(:class:`Fibot.chats.Chats`): Chat records of users.
            delay(:obj:`int`): Amount of seconds between scans.
            thread(:class:`threading.Timer`): Thread that does the scanning.
            polling(:obj:`bool`): Object that indicates if polling has to be done
            last_check(:class:`datetime.datetime`): datetime of the last check for notifications
    """
    def __init__(self, mh, delay):
        self.api = API_raco()
        self.message_handler = mh
        self.chats = self.message_handler.chats
        self.delay = delay
        self.thread = None
        self.polling = True
        self.last_check = datetime.datetime.now()
        self.retrieve_timestamp()
        print("Loaded timestamp: {}".format(self.last_check))

    """
        Saves the timestamp when the last scan was done
    """
    def dump_timestamp(self):
        to_save = str(self.last_check)
        with open('Data/timestamp.txt', 'w') as file:
            file.write(to_save)

    """
        Retrieves and stores the timestamp when the last scan was done
    """
    def retrieve_timestamp(self):
        with open('Data/timestamp.txt', 'r') as file:
            timestamp = file.readline()
            print("This is the timestamp: {}".format(timestamp))
            date, time = timestamp.split(' ')
            year, month, day = date.split('-')
            hour, minute, second = time.split(':')
            self.last_check = datetime.datetime(int(year),int(month), int(day), int(hour), int(minute), int(second))

    """
        This function defines the new timer and starts it (effectively allows the scanning)
    """
    def run(self):
        if self.polling:
            self.thread = Timer(self.delay, self.poll)
            self.thread.start()

    """
        Does a scan over all users, and then returns to the activation function
    """
    def poll(self):
        self.chats.load()
        print("Notification scanner thread: Last check was done: {}\n".format(datetime.datetime.now()))
        print("Notification scanner thread: Scanning for notifications\n")
        last_avis = self.last_check
        for student_id in self.chats.chats.keys():
            student = self.chats.get_chat(student_id)
            if student['notifications']:
                print("Notification scanner thread: Scanning {}.\n".format(student['name']))
                access_token = student['access_token']
                user_lang = student['language']
                avisos = self.api.get_avisos(access_token)
                if not avisos:
                    print("AVISOS IS NOT OKAY, LETS CHECK SEVERAL THINGS:")
                    print("WADU HEK I AM? {}".format(avisos))
                    print("DO WE HAVE ACCESS TOKEN? {}".format(access_token))
                    print("IS IT EXPIRED? {}".format(student['expire_time_end']))
                    print("IS IT CONSIDERED TO BE EXPIRED? {}".format(self.chats.token_has_expired(student_id)))
                else:
                    print("\n -------------- TOTAL NUMBER OF AVISOS OF USER {}: {} -------------\n".format(student['name'], len(avisos)))
                    filtered = self.filter(avisos)
                    print("\n ----- TOTAL NUMBER OF AVISOS AFTER FILTERING OF USER {}: {} ------\n".format(student['name'], len(filtered)))
                    if filtered: pprint(filtered)
                    for avis in filtered:
                        message = Notification(avis, user_lang).get_notif()
                        self.message_handler.send_message(student_id, message, typing=True)
                        print("Notification was sent!")
                        last_avis = max(last_avis, self.get_date(avis))
        self.last_check = last_avis
        self.dump_timestamp()
        print("Last notification was received {}!".format(self.last_check))
        self.run()

    """
        Parameters:
            avisos(:obj:`list`): List of publications for a user

        This function filters the publications so that they were not sent previously.
    """
    def filter(self, avisos):
        not_new = 0
        result = []
        if not avisos: return []
        for avis in avisos:
            if not self.last_check: result.append(avis)
            elif self.get_date(avis) > self.last_check:
                print("\nThere's a new publication!\t\t {} vs {}\n".format(self.get_date(avis), self.last_check))
                result.append(avis)
            else:
                #print("\nThere's a NOT new publication!\t\t {} vs {}\n".format(self.get_date(avis), self.last_check))
                not_new+=1
        print("Not new avisos: {}".format(not_new))
        return result

    """
        Parameters:
            avis(:obj:`dict`): One publication

        This function returns the date of a publication. It also converts it to datetime.
        so it returns (:class:`datetime.datetime`)

        2018-03-01T00:00:00 -> datetime(year, month, day, hour, minute, second)
    """
    def get_date(self, avis):
        avis_date = avis['data_modificacio']
        avis_date_day, avis_date_hour = avis_date.split('T')
        year, month, day = avis_date_day.split('-')
        hour, minute, second = avis_date_hour.split(':')
        return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    """
        Allows polling
    """
    def stop_polling(self):
        self.polling = False

    """
        Forbids polling
    """
    def start_polling(self):
        self.polling = True
        self.run()
