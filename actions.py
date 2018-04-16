#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#

#-- 3rd party imports --#
from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

#-- Local imports --#
from Fibot.api.api_raco import API_raco
#from Fibot.Data.teachers import Teachers
from Fibot.chats import Chats
from Fibot.Data.data_types.lecture import Lecture, Schedule
from Fibot.Data.data_types.subject_spots import Subject_spots
from Fibot.Data.data_types.subject_teachers import Subject_teachers
from Fibot.Data.teachers import Teachers


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
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        mail = Teachers(language = user_lang).get_closer_teacher(teacher_name).get_mail()
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
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        office = Teachers(language = user_lang).get_closer_teacher(teacher_name).get_office()
        dispatcher.utter_message("{}".format(office))
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
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        query = {'places-matricula': { 'field': 'assig', 'value': subject_acro }}
        response = API_raco().get_main(query)
        s_s = Subject_spots(response, user_lang)
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
        subject_acro = tracker.get_slot("subject_acronym").upper()
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        if not access_token: dispatcher.utter_message("{}".format(self.not_logged_message(user_lang)))
        print("el access token de {} es {}".format(chat_id, access_token))
        if subject_acro:
            query = {'horari': {'field': 'codi_assig' , 'value': subject_acro}}
            response = API_raco().get_main(query, public = False, access_token = access_token)
            for data in response:
                lecture = Lecture(data, user_lang)
                dispatcher.utter_message("{}".format(lecture))
        return []

    def not_logged_message(self, user_lang):
        messages = {
            'ca': "No estàs identificat amb el teu usuari del Racó. No puc accedir a la teva informació.",
            'es': "No estás identifcado con tu usuario del Racó. No puedo acceder a la tu información.",
            'en': "You have not logged in with your Racó account. I cannot see your information"
        }
        return messages[user_lang]


class action_show_subject_schedule(Action):
    def name(self):
        return 'action_show_subject_schedule'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym").upper()
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        if not access_token: dispatcher.utter_message("{}".format(self.not_logged_message(user_lang)))
        print("el access token de {} es {}".format(chat_id, access_token))
        if subject_acro:
            query = {'horari': {'field': 'codi_assig' , 'value': subject_acro}}
            response = API_raco().get_main(query, public = False, access_token = access_token)
            print(response)
            for data in response:
                lecture = Lecture(data, user_lang)
                dispatcher.utter_message("{}".format(lecture))
        return []

    def not_logged_message(self, user_lang):
        messages = {
            'ca': "No estàs identificat amb el teu usuari del Racó. No puc accedir a la teva informació.",
            'es': "No estás identifcado con tu usuario del Racó. No puedo acceder a la tu información.",
            'en': "You have not logged in with your Racó account. I cannot see your information."
        }
        return messages[user_lang]

class action_show_subject_teachers_mails(Action):

    def name(self):
        return 'action_show_subject_teachers_mails'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym").upper()
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        teachers_info = API_raco().get_subject_teachers(acronym = subject_acro, language = user_lang)
        teachers_info = Subject_teachers(subject_acro, teachers_info, user_lang)
        print("This are the teachers: {}".format(list(teachers_info.get_names())))
        if teachers_info.amount < 4:
            for response in teachers_info.get_mails():
                dispatcher.utter_message("{}".format(response))
        else:
            answers = {'ca': "Quin d'aquests professors t'interessa?\n",
                'es': '¿Quién de estos te interesa?\n',
                'en': 'Who out of this teachers are you interested in?\n'
            }
            answer = answers[user_lang]
            for teacher in teachers_info.get_names():
                answer = answer + teacher + '\n'
            dispatcher.utter_message("{}".format(answer))
        return []


class action_show_subject_teachers_offices(Action):

    def name(self):
        return 'action_show_subject_teachers_offices'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym").upper()
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        teachers_info = API_raco().get_subject_teachers(acronym = subject_acro, language = user_lang)
        teachers_info = Subject_teachers(subject_acro, teachers_info, user_lang)
        print("This are the teachers: {}".format(list(teachers_info.get_names())))
        if teachers_info.amount < 4:
            for response in teachers_info.get_offices():
                dispatcher.utter_message("{}".format(response))
        else:
            answers = {'ca': "Quin d'aquests professors t'interessa?\n",
                'es': '¿Quién de estos te interesa?\n',
                'en': 'Who out of this teachers are you interested in?\n'
            }
            answer = answers[user_lang]
            for teacher in teachers_info.get_names():
                answer = answer + teacher + '\n'
            dispatcher.utter_message("{}".format(answer))
        return []#[SlotSet("matches", teachers_info.get_names())]

class action_show_subject_teachers_names(Action):

    def name(self):
        return 'action_show_subject_teachers_names'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym").upper()
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        teachers_info = API_raco().get_subject_teachers(acronym = subject_acro, language = user_lang)
        teachers_info = Subject_teachers(subject_acro, teachers_info, user_lang)
        print("This are the teachers: {}".format(list(teachers_info.get_names())))
        answers = {'ca': "Aquests són els professors de {}\n",
            'es': 'Éstos son los profesores de {}\n',
            'en': "These are {}'s teachers\n"
        }
        answer = answers[user_lang].format(subject_acro)
        for teacher in teachers_info.get_names():
            answer = answer + teacher + '\n'
        dispatcher.utter_message("{}".format(answer))
        return []

class action_show_next_class(Action):

    def name(self):
        return 'action_show_next_class'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        schedule = API_raco().get_schedule(access_token, user_lang)
        schedule = Schedule(schedule, user_lang)
        answer = schedule.get_response()
        dispatcher.utter_message("{}".format(answer))
        return []
