#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Teacher(object):

    """ Helper class for actions

        Parameters:
            data(:obj:`dict`): Information of a teacher. Example:
                {
                    "name": "Javier Bejar Alonso"
                    "mail": "bejar@cs.upc.edu",
                    "office": "Building Omega Office 204"
                }
    """
    def __init__(self, data):
        self.name = data['name']
        self.mail = data['mail']
        if data['office']: self.office = data['office']
        else: self.office = None

    def get_mail(self):
        return "{}'s mail is {}".format(
            self.name,
            self.mail
        )

    def get_office(self):
        return "{}'s office is {}".format(
            self.name,
            self.office
        )
