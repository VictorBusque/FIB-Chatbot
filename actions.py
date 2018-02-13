#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#-- 3rd party imports --#
from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

#-- Local imports --#
from Fibot.api_raco import API_raco


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


class action_show_teacher_desk(Action):

    def name(self):
        return 'action_show_teacher_desk'

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

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym")
        #subject_name = tracker.get_slot("subject_name")
        raco_api = API_raco()
        query = {'places-matricula': { 'field': 'assig', 'value': subject_acro }}
        print(query)
        response = raco_api.get_main(query)
        free = []
        total = []
        for item in list(response):
            dispatcher.utter_message("There are {}/{} free spots in {}, group {}.".format(
                            item['places_lliures'],
                            item['places_totals'],
                            subject_acro,
                            item['grup']))
        return []

class priv_raco_api:
    def search_classroom(self, info):
        return 'A5001'

    def search_schedule(self, info):
        return 'Wednesday, 10:00'


class action_show_subject_classroom(Action):
    def name(self):
        return 'action_show_subject_classroom'

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym")
        raco_api = API_raco()
        query = {'horari': {'field': 'codi_assig' , 'value': subject_acro}}
        response = raco_api.get_main(query, chat_id, public = False)
        dispatcher.utter_message("{}".format(response))
        return []


class action_show_subject_schedule(Action):
    def name(self):
        return 'action_show_subject_schedule'

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym")
        raco_api = API_raco()
        query = {'horari': {'field': 'codi_assig' , 'value': subject_acro}}
        response = raco_api.get_main(query, chat_id, public = False)
        dispatcher.utter_message("{}".format(response))
        return []
