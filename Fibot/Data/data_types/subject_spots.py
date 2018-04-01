#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
from random import randint
import json

class Subject_spots(object):
    """ Helper class for actions

        Parameters:
            data(:obj:`list(:obj:`dict`)): Information of a subjects spots. Example:
                [{
                    "assig": "A",
                    "grup": "11",
                    "places_lliures": 0,
                    "places_totals": 0,
                    "tipus_grup": "N",
                    "tipus_assignatura": "APE",
                    "pla": "GRAU"
                }, ... ]
    """
    def __init__(self, data, language):
        self.subject = data[0]['assig']
        self.group_info = {}
        for item in data:
            self.group_info[item['grup']] = {
                'group': item['grup'],
                'free_spots': item['places_lliures'],
                'total_spots': item['places_totals']
            }
        self.language = language
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            self.responses = data['ask_free_spots']


    def get_group_spots(self, group):
        chosen_response = randint(0, len(self.responses[self.language])-1)
        final_response = self.responses[self.language][chosen_response]
        return final_response.format(
            self.group_info[group]['free_spots'],
            self.group_info[group]['total_spots'],
            self.subject,
            self.group_info[group]['group']
        )
