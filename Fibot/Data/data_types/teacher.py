#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Teacher(object):

    """ Helper class for actions

        Parameters:
            data(:obj:`dict`): Information of a teacher. Example:
                {
                    "name": "Javier Bejar Alonso"
                    "mail": "bejar@cs.upc.edu",
                    "office": "Building Omega Office 204",
                    "department": "cs"
                }
    """
    def __init__(self, data):
        self.name = data['name']
        self.mail = data['mail']
        self.department = data['department']
        self.office = data['office']
        
    """
        Returns a string formatted text which explains the mail for the teacher
    """
    def get_mail(self):
        return "{}'s mail is:\n {}".format(
            self.name.title(),
            self.mail
        )

    """
        Returns a string formatted text which explains the office of the teacher
    """
    def get_office(self):
        return "{}'s office is:\n {}".format(
            self.name.title(),
            self.office.title()
        )

    """
        Returns a general description of the teacher
    """
    def __repr__(self):
        return "{} is a teacher from {}'s department".format(self.name.title(), self.department)
