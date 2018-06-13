#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
from random import randint
import json


class Notification(object):

    """This is a helper class to send messages from publications

        Parameters:
            data(:obj:`dict`): Dict with the following format:
            {
                "titol": "1st assignment",
                "codi_assig": "WSE",
                "text": "<p>Dear students,</p>\r\n<p>Please, find your 1st assignment attached to this post, and read the document carefully. We&#39;ll discuss any details in class tomorrow.</p>\r\n<p>Of course, bring any questions you may have.</p>\r\n<p>Regards,</p>\r\n<p>Antonia Soler</p>",
                "data_insercio": "2018-03-05T00:00:00",
                "data_modificacio": "2018-03-05T13:35:28",
                "data_caducitat": "2018-03-16T00:00:00",
                "adjunts": [
                    {
                        "tipus_mime": "application/msword",
                        "nom": "1st_assignmentWSE_Q2.doc",
                        "url": "https://api.fib.upc.edu/v2/jo/avisos/adjunt/70401",
                        "data_modificacio": "2018-03-05T06:23:48",
                        "mida": 31232
                    }
                ]
            }
    """
    def __init__(self, data, language):
        self.titol = data['titol']
        self.subject = data['codi_assig']
        self.is_from_subject = self.subject[0] != "#"
        self.text = data['text']
        self.attachments = []
        self.language = language
        if 'adjunts' in data.keys():
            for att_file in data['adjunts']:
                self.attachments.append({
                        'name': att_file['nom'],
                        'url': att_file['url']
                })
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            self.responses = data['notification']
        return


    """
        Returns an array of messages to be sent for this particular notification.
    """
    def get_notif(self):
        chosen_response = randint(0, len(self.responses[self.language]['intro'])-1)
        final_response = self.responses[self.language]['intro'][chosen_response]
        type = len(final_response.split('{}'))==2
        if type:
            val = [final_response.format(self.subject)]
        else:
            val = [final_response.format(self.subject, self.titol)]
        if self.attachments:
            for attachment in self.attachments:
                chosen_response = randint(0, len(self.responses[self.language]['attachment'])-1)
                final_response = self.responses[self.language]['attachment'][chosen_response]
                val.append(final_response.format(attachment['name'], attachment['url']))
        return val
