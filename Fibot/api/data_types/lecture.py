#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    def __init__(self, data):
        days = {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday'
        }
        self.assig = data['codi_assig']
        self.group = data['grup']
        self.day = days[data['dia_setmana']]
        self.begin_hour = data['inici']
        aux_hour =  self.begin_hour.split(':')
        self.end_hour = "{}:{}".format(
                str(int(aux_hour[0])+data['durada']),
                aux_hour[1] )
        if data['tipus'] == 'T': self._type = 'theory'
        elif data['tipus'] == 'L': self._type = 'laboratory'
        else: self._type = 'problems'
        self.classroom = data['aules']

    def __repr__(self):
        return "{} from {} to {} a {} class at classroom {}".format(
            self.day,
            self.begin_hour,
            self.end_hour,
            self._type,
            self.classroom
        )
