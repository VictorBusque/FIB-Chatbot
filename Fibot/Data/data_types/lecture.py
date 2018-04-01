#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
from random import randint
import json


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
