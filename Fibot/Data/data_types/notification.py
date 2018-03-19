#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
    def __init__(self, data):
        self.titol = data['titol']
        self.subject = data['codi_assig']
        self.is_from_subject = self.subject[0] != "#"
        self.text = data['text']
        self.attachments = []
        if 'adjunts' in data.keys():
            for att_file in data['adjunts']:
                self.attachments.append({
                        'name': att_file['nom'],
                        'url': att_file['url']
                })

    """
        Returns an array of messages to be sent for this particular notification.
    """
    def get_notif(self):
        val = ["New publication of {} with title:\n {}.".format(self.subject, self.titol)]
        if self.attachments:
            val.append("It has {} attachments.".format(len(self.attachments)))
            for att_file in self.attachments:
                val.append("Attachment with title {} can be found here: {}.".format(att_file['name'], att_file['url']))
        return val
