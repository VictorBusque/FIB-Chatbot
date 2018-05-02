#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
from random import randint
import json
import datetime


class Exam_schedule(object):

    def __init__(self, exam_list, language):
        self.exams = []
        for subject in exam_list:
            for exam in subject:
                self.exams.append(Exam(exam, language))
        self.exams = sorted(self.exams)
        self.language = language


    def get_closest_exams(self, range = 14, number = None, acro_filter = None):
        if number: return self.exams[:number]
        else:
            for exam in self.exams:
                print(exam.subject)
                if acro_filter:
                    print("Tinc un filtrat per {}".format(acro_filter))
                    if acro_filter == exam.subject and  self.get_day_difference(exam) <= range: yield exam
                else:
                    print("No tinc cap filtrat, perque acro_filter = {}".format(acro_filter))
                    if self.get_day_difference(exam) <= range: yield exam


    def get_day_difference(self, exam):
        day_now = datetime.datetime.now()
        day_exam = exam.date
        return (day_exam - day_now).days


class Exam(object):
    """ Helper class for actions

        Parameters:
            data(:obj:`dict`): Information of an exam. Example:
                {
                    "id": 11438,
                    "assig": "IC",
                    "aules": "A5002, A6002, A5102",
                    "inici": "2018-03-05T13:00:00",
                    "fi": "2018-03-05T14:45:00",
                    "quatr": 2,
                    "curs": 2017,
                    "pla": "GRAU",
                    "tipus": "P"
                }
            language(:obj:`str`): Language in which the output has to be
    """
    def __init__(self, data, language):
        self.subject = data['assig']
        self.date = self.get_date(data)
        self.classrooms = data['aules'].split(', ')
        self.type_ = data['tipus']
        self.duration = self.get_duration(data)
        self.language = language
        self.months = {
            'ca': {
            1: 'Gener',
            2: 'Febrer',
            3: 'Març',
            4: 'Abril',
            5: 'Maig',
            6: 'Juny',
            7: 'Juliol',
            8: 'Agost',
            9: 'Setembre',
            10: 'Octubre',
            11: 'Novembre',
            12: 'Desembre'
            },
            'es': {
            1: 'Enero',
            2: 'Febrero',
            3: 'Marzo',
            4: 'Abril',
            5: 'Mayo',
            6: 'Junio',
            7: 'Julio',
            8: 'Agosto',
            9: 'Septembre',
            10: 'Octubre',
            11: 'Noviembre',
            12: 'Diciembre'
            },
            'en': {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
            }
        }


    def get_date(self, exam, field = 'inici'):
        exam_date = exam[field]
        exam_date_day, exam_date_hour = exam_date.split('T')
        year, month, day = exam_date_day.split('-')
        hour, minute, second = exam_date_hour.split(':')
        return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    def get_duration(self, exam):
        exam_start = self.get_date(exam, 'inici')
        exam_end = self.get_date(exam, 'fi')
        dif = (exam_end-exam_start).seconds
        hours = int(dif/3600)
        minutes = (dif%3600)/60
        return [hours, minutes]

    def __lt__(self, other):
        return self.date < other.date

    def __gt__(self, other):
        return self.date > other.date

    def __eq__(self, other):
        return self.date == other.date

    def __repr__(self):
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            responses = data['ask_next_exams']
        chosen_response = randint(0, len(responses[self.language])-1)
        final_response = responses[self.language][chosen_response]
        day = str(self.date.day)
        if self.language == 'en':
            if day[len(day)-1] == '1': day = "{}st".format(day)
            elif day[len(day)-1] == '2': day = "{}nd".format(day)
            elif day[len(day)-1] == '3': day = "{}rd".format(day)
            else: day = "{}th".format(day)
        if self.date.minute == 0: hour = self.date.hour
        elif self.date.minute >= 10: hour = "{}:{}".format(self.date.hour, self.date.minute)
        else: hour = "{}:0{}".format(self.date.hour, self.date.minute)
        return final_response.format(self.subject, day, self.months[self.language][self.date.month], hour)
