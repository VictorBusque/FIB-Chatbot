#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Teacher(object):

    """ Helper class for actions

        Parameters:
            data(:obj:`dict`): Information of a teacher. Example:
                {
                    "name": "Javier",
                    "last_name": ["Bejar", "Alonso"],
                    "mail": "bejar@cs.upc.edu",
                    "office": "Omega, 204"
                }
    """
    def __init__(self, data):
        self.name = data['name']
        self.last_name = ['last_name']
        self.mail = data['mail']
        self.office = data['office']

    def get_mail(self):
        return "{}'s mail is {}".format(
            self.name,
            self.mail
        )

    def get_office(self):
        return "{}'s office is {}".format(
            self.name,
            self.mail
        )
