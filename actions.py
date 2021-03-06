#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
from random import randint
from pprint import pprint
from termcolor import colored
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

def color_print_slots(tracker):
    slots_dict = tracker.slots
    for slot in slots_dict.keys():
        if not 'None' in str(slots_dict[slot]):
            data = str(slots_dict[slot])
            data = data.split(':')[1].split(')')[0]
            print('\t'+slot+': '+colored(data, 'green'))
        else: print('\t'+slot+': '+colored('None', 'red'))

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
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Reseteando todos los slots...\n")
        return[AllSlotsReset()]


class Action_check_subject_existance(Action):

    def name(self):
        return 'Action_check_subject_existance'

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        subject_acro = tracker.get_slot("subject_acronym")
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        if subject_acro:
            subject_acro = subject_acro.upper()
            if not API_raco().subject_exists(subject_acro):
                dispatcher.utter_message(str(Not_understood(user_lang, 'wrong_subject')))
            else:
                print(colored("Asignatura existe", 'green'))
                return [SlotSet("subject_existance", True)]
        else:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_understand')))
        print(colored("Asignatura NO existe", 'red'))
        return [SlotSet("subject_existance", False)]


class Action_check_subject_enrollment(Action):
    def name(self):
        return 'Action_check_subject_enrollment'

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        subject_acro = tracker.get_slot("subject_acronym").upper()
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        if not API_raco().user_enrolled_subject(subject_acro, access_token, user_lang):
            response = str(Not_understood(user_lang, 'not_enrolled'))
            if '{}' in response:
                dispatcher.utter_message(response.format(subject_acro))
            else: dispatcher.utter_message(response)
            print(colored("El usuario NO está matriculado", 'red'))
            return [SlotSet("subject_enrollment", False)]
        else:
            print(colored("El usuario está matriculado", 'green'))
            return [SlotSet("subject_enrollment", True)]


class Action_check_user_logged(Action):

    def name(self):
        return 'Action_check_user_logged'

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        if not access_token:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_logged')))
            print(colored("El usuario NO está identificado en el Racó", 'red'))
            return [SlotSet('user_logged', False)]
        else:
            print(colored("El usuario está identificado en el Racó", 'green'))
            return [SlotSet('user_logged', True)]


class Action_show_teacher_mail(Action):

    def name(self):
        return 'Action_show_teacher_mail'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
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
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
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
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
        subject_acro = tracker.get_slot("subject_acronym").upper()
        group = tracker.get_slot("group")
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        response = list(API_raco().get_free_spots(subject_acro, user_lang))
        if not response:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_enrollment_possible')).format(subject_acro))
            return []
        s_s = Subject_spots(response, user_lang)
        if group:
            dispatcher.utter_message("{}".format(s_s.get_group_spots(group)))
        else:
            for group in s_s.group_info.keys():
                dispatcher.utter_message("{}".format(s_s.get_group_spots(group)))
        return []


class Action_show_subject_classroom(Action):
    def name(self):
        return 'Action_show_subject_classroom'

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
        subject_acro = tracker.get_slot("subject_acronym").upper()
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        response = API_raco().get_schedule(access_token, user_lang, subject_acro)
        for data in response:
            lecture = Lecture(data, user_lang)
            dispatcher.utter_message("{}".format(lecture))
        return []


class Action_show_subject_schedule(Action):
    def name(self):
        return 'Action_show_subject_schedule'

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
        subject_acro = tracker.get_slot("subject_acronym").upper()
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        response = API_raco().get_schedule(access_token, user_lang, subject_acro)
        for data in response:
            lecture = Lecture(data, user_lang)
            dispatcher.utter_message("{}".format(lecture))
        return []


class Action_show_subject_teachers_mails(Action):

    def name(self):
        return 'Action_show_subject_teachers_mails'

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
        subject_acro = tracker.get_slot("subject_acronym").upper()
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        teachers_info = API_raco().get_subject_teachers(acronym = subject_acro, language = user_lang)
        teachers_info = Subject_teachers(subject_acro, teachers_info, user_lang)
        if teachers_info.amount <= 4:
            for response in teachers_info.get_mails():
                dispatcher.utter_message("{}".format(response))
        else:
            answers = {'ca': "Aquests són els professors de {}. Qui t'interessa?!\n",
                'es': 'Éstos son los profesores de {}. ¿Quién te interesa?\n',
                'en': "These are {}'s teachers. Who are you interested in?\n"}
            answer = answers[user_lang].format(subject_acro)
            for teacher in teachers_info.get_names(): answer = answer + teacher + '\n'
            dispatcher.utter_message("{}".format(answer))
            return [SlotSet("matches", True)]
        return [SlotSet("matches", False)]


class Action_show_subject_teachers_offices(Action):

    def name(self):
        return 'Action_show_subject_teachers_offices'

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
        subject_acro = tracker.get_slot("subject_acronym").upper()
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        teachers_info = API_raco().get_subject_teachers(acronym = subject_acro, language = user_lang)
        teachers_info = Subject_teachers(subject_acro, teachers_info, user_lang)
        if teachers_info.amount <= 4:
            for response in teachers_info.get_offices():
                dispatcher.utter_message("{}".format(response))
        else:
            answers = {'ca': "Aquests són els professors de {}. Qui t'interessa?!\n",
                'es': 'Éstos son los profesores de {}. ¿Quién te interesa?\n',
                'en': "These are {}'s teachers. Who are you interested in?\n"}
            answer = answers[user_lang].format(subject_acro)
            for teacher in teachers_info.get_names(): answer = answer + teacher + '\n'
            dispatcher.utter_message("{}".format(answer))
            return [SlotSet("matches", True)]
        return [SlotSet("matches", False)]


class Action_show_subject_teachers_names(Action):

    def name(self):
        return 'Action_show_subject_teachers_names'

    def resets_topic(self):
        return True

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
        subject_acro = tracker.get_slot("subject_acronym").upper()
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        teachers_info = API_raco().get_subject_teachers(acronym = subject_acro, language = user_lang)
        teachers_info = Subject_teachers(subject_acro, teachers_info, user_lang)
        answers = {'ca': "Aquests són els professors de {}:\n",
            'es': 'Éstos son los profesores de {}:\n',
            'en': "These are {}'s teachers:\n"}
        answer = answers[user_lang].format(subject_acro)
        for teacher in teachers_info.get_names(): answer = answer + teacher + '\n'
        dispatcher.utter_message("{}".format(answer))
        return []


class Action_show_next_class(Action):

    def name(self):
        return 'Action_show_next_class'

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        schedule = API_raco().get_schedule(access_token = access_token, language = user_lang)
        schedule = Schedule(schedule, user_lang)
        answer = schedule.get_response()
        if isinstance(answer, list): dispatcher.utter_message("{}".format(answer[0]))
        else: dispatcher.utter_message("{}".format(answer))
        return []


class Action_show_next_exams(Action):

    def name(self):
        return 'Action_show_next_exams'

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
        chat_id = tracker.sender_id
        subject_acro = tracker.get_slot("subject_acronym")
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        if subject_acro: acro_filter = subject_acro.upper()
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
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
        chat_id = tracker.sender_id
        subject_acro = tracker.get_slot("subject_acronym")
        user_lang = Chats().get_chat_lite(chat_id)['language']
        access_token = Chats().get_chat_lite(chat_id)['access_token']
        if subject_acro: acro_filter = subject_acro
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


class Action_show_teacher_info(Action):

    def name(self):
        return 'Action_show_teacher_info'

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
        teacher_name = tracker.get_slot("teacher_name")
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        if teacher_name:
            teacher, dist = Teachers(language = user_lang).get_closer_teacher(teacher_name)
            if dist <= 5:
                dispatcher.utter_message("{}".format(teacher))
            else:
                dispatcher.utter_message("{}".format(Not_understood(user_lang, 'wrong_teacher')))
        else:
            dispatcher.utter_message("{}".format(Not_understood(user_lang, 'not_understand')))
        return []


class Action_greet(Action):

    def name(self):
        return 'Action_greet'

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        responses = []
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            responses = data['greet_back']
        chosen_response = randint(0, len(responses[user_lang])-1)
        final_response = responses[user_lang][chosen_response]
        dispatcher.utter_message("{}".format(final_response))
        return []


class Action_no_problem(Action):

    def name(self):
        return 'Action_no_problem'

    def run(self, dispatcher, tracker, domain):
        print("\nEjecutando acción:\t{}".format(colored(self.name(), 'yellow', attrs=['bold'])))
        print("Representación de los slots:")
        color_print_slots(tracker)
        chat_id = tracker.sender_id
        user_lang = Chats().get_chat_lite(chat_id)['language']
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            responses = data['thank']
        chosen_response = randint(0, len(responses[user_lang])-1)
        final_response = responses[user_lang][chosen_response]
        dispatcher.utter_message("{}".format(final_response))
        return []
