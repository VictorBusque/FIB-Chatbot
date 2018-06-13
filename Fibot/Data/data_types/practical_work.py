#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
from random import randint
import json
import datetime


class Practical_schedule(object):

    def __init__(self, pracs_list, language):
        self.pracs = []
        for prac in pracs_list:
            self.pracs.append(Practical_work(prac, language))
        self.pracs = sorted(self.pracs)
        self.language = language


    def get_closest_pracs(self, range = 14, number = None, acro_filter = None):
        if number: return self.pracs[:number]
        else:
            for prac in self.pracs:
                if acro_filter:
                    if acro_filter == prac.subject and self.get_day_difference(prac) <= range: yield prac
                else:
                    if self.get_day_difference(prac) <= range: yield prac


    def get_day_difference(self, prac):
        day_now = datetime.datetime.now()
        day_exam = prac.date
        return (day_exam - day_now).days


class Practical_work(object):
    """ Helper class for actions

        Parameters:
            data(:obj:`dict`): Information of a practical work. Example:
                {
                  'codi_asg': 'WSE',
                  'comentaris': '<p>Please, upload the final version of your 2nd assignment '
                                'here.</p>\r\n'
                                '<p>Antonia Soler</p>',
                  'data_inici': '2018-04-26T12:00:00',
                  'data_limit': '2018-04-27T23:59:00',
                  'data_modificacio': '2018-04-26T13:08:54',
                  'grup': '',
                  'titol': '2nd assignment-Final submission'
                }
            language(:obj:`str`): Language in which the output has to be
    """
    def __init__(self, data, language):
        self.subject = data['codi_asg']
        self.date = self.get_date(data)
        self.title = data['titol']
        self.group = data['grup']
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


    def get_date(self, exam, field = 'data_limit'):
        exam_date = exam[field]
        exam_date_day, exam_date_hour = exam_date.split('T')
        year, month, day = exam_date_day.split('-')
        hour, minute, second = exam_date_hour.split(':')
        return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))


    def __lt__(self, other):
        return self.date < other.date

    def __gt__(self, other):
        return self.date > other.date

    def __eq__(self, other):
        return self.date == other.date

    def __repr__(self):
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            responses = data['ask_next_pracs']
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
        return final_response.format(self.title, self.subject, day, self.months[self.language][self.date.month], hour)
