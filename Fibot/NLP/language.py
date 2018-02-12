#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
import re
import requests

class Translator(object):

    """Helper class that enables the bot to speak several languages

        Attributes:
            languages (:obj:`dict`): helper to indicate different languages
    """
    def __init__(self):
        self.base_url = "http://translate.google.com/m"
        self.languages =  {'Catalan': 'ca', 'Spanish': 'es', 'English': 'en'}

    """
        Parameters:
            text (:obj:`str`): text to translate
            from (:obj:`str`): language to translate from [OPTIONAL]
            to (:obj:`str`): language to translate to

        This function translates the text to the language selected.
        It is optional to include the language in which the text was written.
    """
    def translate(self, text, to, _from = 'English'):
        if to == _from: return text
        print("Translating: \t\t '{}' \t{} \t -> \t{}".format(text, _from, to))
        params = {
            'sl': self.languages[_from],
            'hl': self.languages[to],
            'q': text
        }
        response = requests.get(self.base_url, params = params)
        if response.status_code == 200:
            html_code = response.content.decode('ISO-8859-1')
            start = 'class="t0">(.*?)<'
            end = '</div>'
            results = re.findall('%s(.*)%s' % (start, end), str(html_code))
            print("{}  ->  {}".format(text, results[0][0]))
            return results[0][0]
