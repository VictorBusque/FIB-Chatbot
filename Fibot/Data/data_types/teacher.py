#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
from random import randint
import json

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
                language(:obj:`str`): Language in which the output has to be
    """
    def __init__(self, data, language):
        self.name = data['name']
        self.mail = data['mail']
        self.department = data['department']
        self.office = data['office']
        self.language = language
        if self.office and self.language == 'en':
            self.office = self.office.replace('Edifici', 'Building').replace('Despatx', 'Office').replace('Planta', 'Floor')
        if self.office and self.language == 'es':
            self.office = self.office.replace('Edifici', 'Edificio').replace('Despatx', 'Despacho')
        self.responses = {}
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            self.responses['ask_teacher_mail'] = data['ask_teacher_mail']
            self.responses['ask_teacher_office'] = data['ask_teacher_office']
            self.responses['teacher_info'] = data['teacher_info']
        return

    """
        Returns a string formatted text which explains the mail for the teacher
    """
    def get_mail(self):
        if self.mail:
            chosen_response = randint(0, len(self.responses['ask_teacher_mail'][self.language])-1)
            final_response = self.responses['ask_teacher_mail'][self.language][chosen_response]
            if chosen_response < 2:
                return final_response.format(
                    self.name.split(' ')[0].title(),
                    self.mail
                    )
            else:
                return final_response.format(self.mail)
        else:
            if self.language == 'ca': return "Aquesta persona no té correu..."
            if self.language == 'es': return "Esta persona no tiene correo..."
            if self.language == 'en': return "This person does not have mail..."

    """
        Returns a string formatted text which explains the office of the teacher
    """
    def get_office(self):
        if self.office:
            chosen_response = randint(0, len(self.responses['ask_teacher_office'][self.language])-1)
            final_response = self.responses['ask_teacher_office'][self.language][chosen_response]
            if chosen_response < 1:
                return final_response.format(
                    self.name.split(' ')[0].title(),
                    self.office
                    )
            else:
                return final_response.format(self.office)
        else:
            if self.language == 'ca': return "Aquesta persona no té despatx..."
            if self.language == 'es': return "Esta persona no tiene despacho..."
            if self.language == 'en': return "This person does not have an office..."

    """
        Returns a general description of the teacher
    """
    def __repr__(self):
        chosen_response = randint(0, len(self.responses['teacher_info'][self.language])-1)
        final_response = self.responses['teacher_info'][self.language][chosen_response]
        return final_response.format(self.name.title(), self.department)
