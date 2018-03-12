#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    def __init__(self, data):
        self.subject = data[0]['assig']
        self.group_info = {}
        for item in data:
            self.group_info[item['grup']] = {
                'group': item['grup'],
                'free_spots': item['places_lliures'],
                'total_spots': item['places_totals']
            }

    def get_group_spots(self, group):
        return "There are {}/{} free spots in {}, group {}.".format(
            self.group_info[group]['free_spots'],
            self.group_info[group]['total_spots'],
            self.subject,
            self.group_info[group]['group']
        )
