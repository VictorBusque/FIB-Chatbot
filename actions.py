#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
from random import randint
import json

#-- 3rd party imports --#
from rasa_core.actions.action import Action
from rasa_core.events import AllSlotsReset, SlotSet

#-- Local imports --#
from Fibot.api.api_raco import API_raco
from Fibot.chats import Chats
from Fibot.Data.data_types.lecture import Lecture, Schedule
from Fibot.Data.data_types.subject_spots import Subject_spots
from Fibot.Data.data_types.subject_teachers import Subject_teachers
from Fibot.Data.data_types.practical_work import Practical_schedule
from Fibot.Data.data_types.exam import Exam_schedule
from Fibot.Data.teachers import Teachers


class Not_understood(object):

    def __init__(self, language, type_):
        with open('./Data/error_responses.json', 'rb') as fp:
            self.messages = json.load(fp)
        self.type_ = type_
        self.language = language

    def __repr__(self):
        chosen_response = self.messages[self.type_][self.language][randint(0,len(self.messages[self.type_][self.language])-1)]
        return chosen_response

class Action_slot_reset(Action):
    def name(self):
        return 'Action_slot_reset'
    def run(self, dispatcher, tracker, domain):
        return[AllSlotsReset()]


class Action_show_teacher_mail(Action):

    def name(self):
        return 'Action_show_teacher_mail'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        teacher_name = tracker.get_slot("teacher_name")
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        if teacher_name:
            teacher, dist = Teachers(language = user_lang).get_closer_teacher(teacher_name)
            if dist <= 5:
                mail = teacher.get_mail()
                dispatcher.utter_message("{}".format(mail))
            else:
                dispatcher.utter_message("{}".format(Not_understood(user_lang, 'wrong_teacher')))
        else:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_understand')))
        return []


class Action_show_teacher_office(Action):

    def name(self):
        return 'Action_show_teacher_office'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        teacher_name = tracker.get_slot("teacher_name")
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        if teacher_name:
            teacher, dist = Teachers(language = user_lang).get_closer_teacher(teacher_name)
            if dist <= 5:
                office = teacher.get_office()
                dispatcher.utter_message("{}".format(office))
            else:
                dispatcher.utter_message("{}".format(Not_understood(user_lang, 'wrong_teacher')))
        else:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_understand')))
        return []


class Action_show_subject_free_spots(Action):

    def name(self):
        return 'Action_show_subject_free_spots'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym")
        group = tracker.get_slot("group")
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        if subject_acro:
            subject_acro = subject_acro.upper()
            if API_raco().subject_exists(subject_acro, user_lang):
                response = list(API_raco().get_free_spots(subject_acro, user_lang))
                s_s = Subject_spots(response, user_lang)
                if group:
                    dispatcher.utter_message("{}".format(s_s.get_group_spots(group)))
                else:
                    for group in s_s.group_info.keys():
                        dispatcher.utter_message("{}".format(s_s.get_group_spots(group)))
            else:
                dispatcher.utter_message("{}".format(Not_understood(user_lang, 'wrong_subject')))
        else:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_understand')))
        return []


class Action_show_subject_classroom(Action):
    def name(self):
        return 'Action_show_subject_classroom'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym")
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        if not access_token:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_logged')))
            return []
        if subject_acro:
            subject_acro = subject_acro.upper()
            if API_raco().subject_exists(subject_acro):
                if not API_raco().user_enrolled_subject(subject_acro, access_token, user_lang):
                    response = str(Not_understood(user_lang, 'not_enrolled'))
                    if '{}' in response:
                        dispatcher.utter_message(response.format(subject_acro))
                    else: dispatcher.utter_message(response)
                else:
                    response = API_raco().get_schedule(access_token, user_lang, subject_acro)
                    for data in response:
                        lecture = Lecture(data, user_lang)
                        dispatcher.utter_message("{}".format(lecture))
            else:
                dispatcher.utter_message("{}".format(Not_understood(user_lang, 'wrong_subject')))
        else:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_understand')))
        return []


class Action_show_subject_schedule(Action):
    def name(self):
        return 'Action_show_subject_schedule'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym")
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        if not access_token:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_logged')))
            return []
        if subject_acro:
            subject_acro = subject_acro.upper()
            if API_raco().subject_exists(subject_acro):
                if not API_raco().user_enrolled_subject(subject_acro, access_token, user_lang):
                    response = str(Not_understood(user_lang, 'not_enrolled'))
                    if '{}' in response:
                        dispatcher.utter_message(response.format(subject_acro))
                    else: dispatcher.utter_message(response)
                else:
                    response = API_raco().get_schedule(access_token, user_lang, subject_acro)
                    for data in response:
                        lecture = Lecture(data, user_lang)
                        dispatcher.utter_message("{}".format(lecture))
            else:
                dispatcher.utter_message("{}".format(Not_understood(user_lang, 'wrong_subject')))
        else:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_understand')))
        return []

    def not_logged_message(self, user_lang):
        messages = {
            'ca': "No estàs identificat amb el teu usuari del Racó. No puc accedir a la teva informació.",
            'es': "No estás identifcado con tu usuario del Racó. No puedo acceder a la tu información.",
            'en': "You have not logged in with your Racó account. I cannot see your information."
        }
        return messages[user_lang]


class Action_show_subject_teachers_mails(Action):

    def name(self):
        return 'Action_show_subject_teachers_mails'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym")
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        if subject_acro:
            subject_acro = subject_acro.upper()
            if API_raco().subject_exists(subject_acro):
                teachers_info = API_raco().get_subject_teachers(acronym = subject_acro, language = user_lang)
                teachers_info = Subject_teachers(subject_acro, teachers_info, user_lang)
                if teachers_info.amount <= 4:
                    for response in teachers_info.get_mails():
                        dispatcher.utter_message("{}".format(response))
                else:
                    print("Hay más de 4 profesores")
                    answers = {'ca': "Aquests són els professors de {}, qui t'interessa?!\n",
                        'es': 'Éstos son los profesores de {}. ¿Quién te interesa?\n',
                        'en': "These are {}'s teachers. Who are you interested in?\n"
                    }
                    answer = answers[user_lang].format(subject_acro)
                    for teacher in teachers_info.get_names():
                        print("este es uno {}".format(teacher))
                        answer = answer + teacher + '\n'
                    dispatcher.utter_message("{}".format(answer))
                    print("mensaje mandado, voy a colocar el slotset")
                    print(list(teachers_info.get_names()))
                    return [SlotSet("matches", list(teachers_info.get_names()))]
            else:
                dispatcher.utter_message("{}".format(Not_understood(user_lang, 'wrong_subject')))
        else:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_understand')))
        return []


class Action_show_subject_teachers_offices(Action):

    def name(self):
        return 'Action_show_subject_teachers_offices'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym")
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        if subject_acro:
            subject_acro = subject_acro.upper()
            if API_raco().subject_exists(subject_acro):
                teachers_info = API_raco().get_subject_teachers(acronym = subject_acro, language = user_lang)
                teachers_info = Subject_teachers(subject_acro, teachers_info, user_lang)
                if teachers_info.amount < 4:
                    for response in teachers_info.get_offices():
                        dispatcher.utter_message("{}".format(response))
                else:
                    answers = {'ca': "Aquests són els professors de {}, qui t'interessa?!\n",
                        'es': 'Éstos son los profesores de {}. ¿Quién te interesa?\n',
                        'en': "These are {}'s teachers. Who are you interested in?\n"
                    }
                    answer = answers[user_lang].format(subject_acro)
                    for teacher in teachers_info.get_names():
                        answer = answer + teacher + '\n'
                    dispatcher.utter_message("{}".format(answer))
            else:
                dispatcher.utter_message("{}".format(Not_understood(user_lang, 'wrong_subject')))
        else:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_understand')))
        return []


class Action_show_subject_teachers_names(Action):

    def name(self):
        return 'Action_show_subject_teachers_names'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        subject_acro = tracker.get_slot("subject_acronym")
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        if subject_acro:
            subject_acro = subject_acro.upper()
            if API_raco().subject_exists(subject_acro):
                teachers_info = API_raco().get_subject_teachers(acronym = subject_acro, language = user_lang)
                teachers_info = Subject_teachers(subject_acro, teachers_info, user_lang)
                answers = {'ca': "Aquests són els professors de {}:\n",
                    'es': 'Éstos son los profesores de {}:\n',
                    'en': "These are {}'s teachers:\n"
                }
                answer = answers[user_lang].format(subject_acro)
                for teacher in teachers_info.get_names():
                    answer = answer + teacher + '\n'
                dispatcher.utter_message("{}".format(answer))
            else:
                dispatcher.utter_message("{}".format(Not_understood(user_lang, 'wrong_subject')))
        else:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_understand')))
        return []


class Action_show_next_class(Action):

    def name(self):
        return 'Action_show_next_class'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        if not access_token:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_logged')))
            return []
        schedule = API_raco().get_schedule(access_token = access_token, language = user_lang)
        schedule = Schedule(schedule, user_lang)
        answer = schedule.get_response()
        dispatcher.utter_message("{}".format(answer))
        return []


class Action_show_next_exams(Action):

    def name(self):
        return 'Action_show_next_exams'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        chat_id = tracker.sender_id
        subject_acro = tracker.get_slot("subject_acronym")
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        if not access_token:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_logged')))
            return []
        if subject_acro:
            subject_acro = subject_acro.upper()
            coincidences = ["examen".upper(), "examens".upper(), "exam".upper(), "exams".upper(), "examenes".upper(),
                            "exàmens".upper(), "exámenes".upper(), "exàmen".upper(), "exámen".upper()]
            if subject_acro in coincidences: acro_filter = None
            elif not API_raco().subject_exists(subject_acro, user_lang):
                dispatcher.utter_message("{}".format(Not_understood(user_lang, 'wrong_subject')))
                return []
            elif not API_raco().user_enrolled_subject(subject_acro, access_token, user_lang):
                response = str(Not_understood(user_lang, 'not_enrolled'))
                if '{}' in response: dispatcher.utter_message(response.format(subject_acro))
                else: dispatcher.utter_message(response)
                return []
            else: acro_filter = subject_acro
        else: acro_filter = None
        exams = list(API_raco().get_exams_user(access_token = access_token, language = user_lang))
        e_e = Exam_schedule(exams, user_lang)
        exams = list(e_e.get_closest_exams(range = 62, acro_filter = acro_filter))
        if exams:
            for exam in exams:
                dispatcher.utter_message("{}".format(exam))
            tracker._reset_slots()
            return []
        dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_exams')))
        return []


class Action_show_next_pracs(Action):

    def name(self):
        return 'Action_show_next_pracs'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        print(tracker.slots)
        chat_id = tracker.sender_id
        subject_acro = tracker.get_slot("subject_acronym")
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        if not access_token:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_logged')))
            return []
        if subject_acro:
            subject_acro = subject_acro.upper()
            coincidences = ["practica".upper(), "practiques".upper(), "practical work".upper(), "practical works".upper(),
                            "practicas".upper(), "pràctica".upper(), "pràctiques".upper(), "práctica".upper(), "prácticas".upper()]
            if subject_acro in coincidences:
                print("M'ha preguntat practiques")
                acro_filter = None
            elif not API_raco().subject_exists(subject_acro, user_lang):
                dispatcher.utter_message("{}".format(Not_understood(user_lang, 'wrong_subject')))
                return []
            elif not API_raco().user_enrolled_subject(subject_acro, access_token, user_lang):
                response = str(Not_understood(user_lang, 'not_enrolled'))
                if '{}' in response: dispatcher.utter_message(response.format(subject_acro))
                else: dispatcher.utter_message(response)
                return []
            else: acro_filter = subject_acro
        else: acro_filter = None
        pracs = list(API_raco().get_practiques(access_token = access_token, language = user_lang))
        p_e = Practical_schedule(pracs, user_lang)
        pracs = list(p_e.get_closest_pracs(range = 62, acro_filter = acro_filter))
        if pracs:
            for prac in pracs:
                dispatcher.utter_message("{}".format(prac))
            tracker._reset_slots()
            return []
        dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_pracs')))
        return []
