#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#

#-- 3rd party imports --#
from textblob import TextBlob


class Translator(object):

    """Helper class that enables the bot to speak several languages

        Attributes:
            languages (:obj:`dict`): helper to indicate different languages
    """
    def __init__(self):
        self.languages =  {'Catalan': 'ca', 'Spanish': 'es', 'English': 'en'}

    """
        Parameters:
            text (:obj:`str`): text to translate
            from (:obj:`str`): language to translate from [OPTIONAL]
            to (:obj:`str`): language to translate to

        This function translates the text to the language selected.
        It is optional to include the language in which the text was written.
    """
    def translate(self, text, to, from_lang = None):
        if from_lang:
            return str(TextBlob(text).translate(from_lang = self.languages[from_lang], to = self.languages[to]))
        else:
            return str(TextBlob(text).translate(to = self.languages[to]))

    """
        Parameters:
            text (:obj:`str`): text to guess the language of

        This function returns the language in which a text is written
    """
    def detect_language(self, text):
        return TextBlob(text).detect_language()
