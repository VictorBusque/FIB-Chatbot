#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
from random import randint
import json
import datetime


class Exam(object):
    """ Helper class for actions

        Parameters:
            data(:obj:`dict`): Information of a lecture. Example:
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


    def get_dates(self, exam):
        avis_date = avis['inici']
        avis_date_day, avis_date_hour = avis_date.split('T')
        year, month, day = avis_date_day.split('-')
        hour, minute, second = avis_date_hour.split(':')
        return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
