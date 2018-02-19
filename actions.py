#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#

#-- 3rd party imports --#
from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

#-- Local imports --#
from Fibot.api.api_raco import API_raco
from Fibot.chats import Chats
from Fibot.api.data_types.lecture import Lecture
from Fibot.api.data_types.subject_spots import Subject_spots


class teacher_db:
    def search_mail(self, info):
        return 'bejar@cs.upc.edu'

    def search_desk(self, info):
        return 'Omega, 204'

"""
    Could be improved by checking the slots given
    or by doing the query search to the db and see if there
    are several matches.
"""
class action_show_teacher_mail(Action):

    def name(self):
        return 'action_show_teacher_mail'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        teacher_name = tracker.get_slot("teacher_name")
        teacher_surname = tracker.get_slot("teacher_surname")
        teacherdb = teacher_db()
        mail = teacherdb.search_mail({
            'teacher_name': teacher_name,
            'teacher_surname': teacher_surname
        })
        print(mail)
        dispatcher.utter_message("{}".format(mail))
        return []


class action_show_teacher_office(Action):

    def name(self):
        return 'action_show_teacher_office'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        teacher_name = tracker.get_slot("teacher_name")
        teacher_surname = tracker.get_slot("teacher_surname")
        teacherdb = teacher_db()
        desk = teacherdb.search_desk({
            'teacher_name': teacher_name,
            'teacher_surname': teacher_surname
        })
        print(desk)
        dispatcher.utter_message("{}".format(desk))
        return []


class action_show_subject_free_spots(Action):

    def name(self):
        return 'action_show_subject_free_spots'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym").upper()
        raco_api = API_raco()
        query = {'places-matricula': { 'field': 'assig', 'value': subject_acro }}
        response = raco_api.get_main(query)
        s_s = Subject_spots(response)
        for group in s_s.group_info.keys():
            dispatcher.utter_message("{}".format(s_s.get_group_spots(group)))
        return []


class action_show_subject_classroom(Action):
    def name(self):
        return 'action_show_subject_classroom'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym")
        chat_id = tracker.sender_id
        c = Chats()
        access_token = c.get_chat_lite(chat_id)['access_token']
        print("el access token de {} es {}".format(chat_id, access_token))
        if subject_acro:
            raco_api = API_raco()
            query = {'horari': {'field': 'codi_assig' , 'value': subject_acro}}
            response = raco_api.get_main(query, public = False, access_token = access_token)
            for data in response:
                lecture = Lecture(data)
                dispatcher.utter_message("{}".format(lecture))
        return []


class action_show_subject_schedule(Action):
    def name(self):
        return 'action_show_subject_schedule'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym")
        chat_id = tracker.sender_id
        c = Chats()
        c = Chats()
        access_token = c.get_chat_lite(chat_id)['access_token']
        print("el access token de {} es {}".format(chat_id, access_token))
        if subject_acro:
            raco_api = API_raco()
            query = {'horari': {'field': 'codi_assig' , 'value': subject_acro}}
            response = raco_api.get_main(query, public = False, access_token = access_token)
            for data in response:
                lecture = Lecture(data)
                dispatcher.utter_message("{}".format(lecture))
        return []
