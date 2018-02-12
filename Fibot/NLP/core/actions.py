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
#from Fibot.api_raco import API_raco


class teacher_db:
    def search_mail(self, info):
        return 'bejar@cs.upc.edu'

    def search_desk(self, info):
        return 'Omega, 204'


class action_show_teacher_mail(Action):

    def name(self):
        return 'action_show_teacher_mail'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("looking for the teachers mails")
        teacher_name = tracker.get_slot("teacher_name")
        teacher_surname = tracker.get_slot("teacher_surname")
        teacherdb = teacher_db()
        mail = teacherdb.search_mail({
            'teacher_name': teacher_name,
            'teacher_surname': teacher_surname
        })
        dispatcher.utter_message({}.format(mail))


class action_show_teacher_desk(Action):

    def name(self):
        return 'action_show_teacher_desk'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("looking for the teachers desks")
        teacher_name = tracker.get_slot("teacher_name")
        teacher_surname = tracker.get_slot("teacher_surname")
        teacherdb = teacher_db()
        desk = teacherdb.search_desk({
            'teacher_name': teacher_name,
            'teacher_surname': teacher_surname
        })
        dispatcher.utter_message({}.format(desk))


class action_show_subject_free_spots(Action):

    def name(self):
        return 'action_show_subject_free_spots'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("looking for free spots")
        subject_acro = tracker.get_slot("subject_acronym")
        subject_name = tracker.get_slot("subject_name")
        #raco_api = API_raco()
        #query = {'places-matricula': { 'field': 'assig', 'value': subject_acro } }
        #response = raco_api.get_main(query, public=True)
        #lliures = response['places_lliures']
        #totals = response['places_totals']
        dispatcher.utter_message("{}/{}".format(22, 22))


class priv_raco_api:
    def search_classroom(self, info):
        return 'A5001'

    def search_schedule(self, info):
        return 'Wednesday, 10:00'


class action_show_subject_classroom(Action):
    def name(self):
        return 'action_show_subject_classroom'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("looking for clasroom")
        subject_acro = tracker.get_slot("subject_acronym")
        subject_name = tracker.get_slot("subject_name")
        #raco_api = API_raco()
        #query = {'horari': {'field': 'codi_assig' , 'value': subject}}
        #response = raco_api.get_main(query, chat_id, public = False)
        priv_raco_api = priv_raco_api()
        response = priv_raco_api.search_classroom(subject_acro)
        dispatcher.utter_message("{}".format(response))


class action_show_subject_schedule(Action):
    def name(self):
        return 'action_show_subject_schedule'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("looking for clasroom")
        subject_acro = tracker.get_slot("subject_acronym")
        subject_name = tracker.get_slot("subject_name")
        #raco_api = API_raco()
        #query = {'horari': {'field': 'codi_assig' , 'value': subject}}
        #response = raco_api.get_main(query, chat_id, public = False)
        priv_raco_api = priv_raco_api()
        response = priv_raco_api.search_schedule(subject_acro)
        dispatcher.utter_message("{}".format(response))
