#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
from random import randint
import json

#-- Local imports --#
from Fibot.Data.teachers import Teachers

class Subject_teachers(object):

    """ Helper class for actions

        Parameters:
            subject(:obj:`str`): contains the acronym of the subject in matter.
            data(:obj:`list`): list of dictionaries with info like:
				[
					{
						"nom": "Jorge Castro Rabal",
						"email": "castro@cs.upc.edu",
						"is_responsable": false
					},
					...
				]
            language(:obj:`str`): Language in which the output has to be
    """
    def __init__(self, subject, data, language):
        self.subject = subject
        self.data = data
        self.language = language
        self.amount = len(self.data)
        self.responses = {}
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            self.responses['ask_subject_teacher_mail'] = data['ask_subject_teacher_mail']
            self.responses['ask_subject_teacher_office'] = data['ask_subject_teacher_office']
            self.responses['ask_subject_teacher_name'] = data['ask_subject_teacher_name']
        return


    """
        Function that returns str formatted response to a subject teacher mail question
    """
    def get_mails(self):
        for teacher in self.data:
            chosen_response = randint(0, len(self.responses['ask_subject_teacher_mail'][self.language])-1)
            final_response = self.responses['ask_subject_teacher_mail'][self.language][chosen_response]
            yield final_response.format(
                teacher['nom'].title(),
                teacher['email']
            )

    """
        Function that returns str formatted response to a subject teacher office question
    """
    def get_offices(self):
        for teacher in self.data:
            print("Getting office for teacher: {}".format(teacher['nom']))
            chosen_response = randint(0, len(self.responses['ask_subject_teacher_office'][self.language])-1)
            final_response = self.responses['ask_subject_teacher_office'][self.language][chosen_response]
            teacher_data, distance = Teachers(language = self.language).get_closer_teacher(teacher['nom'])
            office = teacher_data.office
            yield final_response.format(
                teacher['nom'].title(),
                office
            )

    """
        Function that returns str formatted response to a subject teacher name question
    """
    def get_names(self):
        for teacher in self.data:
            chosen_response = randint(0, len(self.responses['ask_subject_teacher_name'][self.language])-1)
            final_response = self.responses['ask_subject_teacher_name'][self.language][chosen_response]
            yield final_response.format(
                teacher['nom'].title()
            )
