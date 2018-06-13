#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
from random import randint
import json
import datetime


class Schedule(object):

    def __init__(self, data, language):
        self.lectures = []
        self.language = language
        for lecture in data:
            self.lectures.append(Lecture(lecture, self.language))
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            self.responses = data['ask_next_class']
        return


    def get_next_class(self):
        now = datetime.date.today().isoweekday()
        hour = datetime.datetime.now().hour
        checker = [now, hour]
        ok = []
        for lecture in self.lectures:
            if lecture.day_schedule > checker: ok.append(lecture)
        if not ok: return []
        else: return min(ok)

    def get_response(self):
        now = datetime.date.today().isoweekday()
        hour = datetime.datetime.now().hour
        next = self.get_next_class()
        if not next: return self.responses[self.language]["other_day_other_week"]
        else:
            schedule = next.day_schedule
            if now == schedule[0]:
                chosen_response = randint(0, len(self.responses[self.language]['same_day'])-1)
                final_response = self.responses[self.language]['same_day'][chosen_response]
                return final_response.format(next.assig, schedule[1], next.classroom)
            else:
                chosen_response = randint(0, len(self.responses[self.language]['other_day_week'])-1)
                final_response = self.responses[self.language]['other_day_week'][chosen_response]
                if schedule[0]-now == 1: return final_response.format(self.get_tomorrow(), next.assig, schedule[1], next.classroom)
                else:
                    return final_response.format(self.get_following_days().format(schedule[0]-now), next.assig, schedule[1], next.classroom)

    def get_tomorrow(self):
        if self.language == 'ca': return 'demà'
        elif self.language == 'es': return 'mañana'
        else: return 'tomorrow'

    def get_following_days(self):
        if self.language == 'ca': return "d'aquí {} dies"
        elif self.language == 'es': return 'dentro de {} días'
        else: return 'in {} days'



class Lecture(object):

    """ Helper class for actions

        Parameters:
            data(:obj:`dict`): Information of a lecture. Example:
                {
                    "codi_assig": "WSE",
                    "grup": "10",
                    "dia_setmana": 2,
                    "inici": "12:00",
                    "durada": 2,
                    "tipus": "T",
                    "aules": "A5201"
                }
            language(:obj:`str`): Language in which the output has to be
    """
    def __init__(self, data, language):
        days = {
            'ca': {
                1: 'Dilluns',
                2: 'Dimarts',
                3: 'Dimecres',
                4: 'Dijous',
                5: 'Divendres'
            },
            'es': {
                1: 'Lunes',
                2: 'Martes',
                3: 'Miércoles',
                4: 'Jueves',
                5: 'Viernes'
            },
            'en': {
                1: 'Monday',
                2: 'Tuesday',
                3: 'Wednesday',
                4: 'Thursday',
                5: 'Friday'
            }
        }
        types = {
            'ca': {
                'T': 'teoria',
                'L': 'laboratori',
                'P': 'problemes',
            },
            'es': {
                'T': 'teoría',
                'L': 'laboratorio',
                'P': 'problemas',
            },
            'en': {
                'T': 'theory',
                'L': 'laboratory',
                'P': 'problems',
            }
        }
        self.day_schedule = [data['dia_setmana'], self.format_hour(data['inici'])]
        self.language = language
        self.assig = data['codi_assig']
        self.group = data['grup']
        self.day = days[self.language][data['dia_setmana']]
        self.begin_hour = data['inici']
        aux_hour =  self.begin_hour.split(':')
        self.end_hour = "{}:{}".format(
                str(int(aux_hour[0])+data['durada']),
                aux_hour[1] )
        self._type = types[self.language][data['tipus']]
        self.classroom = data['aules']
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            self.responses = data['ask_subject_schedule']
        return


    def __repr__(self):
        chosen_response = randint(0, len(self.responses[self.language])-1)
        final_response = self.responses[self.language][chosen_response]
        return final_response.format(
            self.day,
            self.begin_hour,
            self.end_hour,
            self._type,
            self.classroom
        )

    def format_hour(self, hour):
        return int(hour.split(':')[0])

    def __lt__(self, other):
        return self.day_schedule < other.day_schedule

    def __gt__(self, other):
        return self.day_schedule > other.day_schedule

    def __eq__(self, other):
        return self.day_schedule == other.day_schedule
