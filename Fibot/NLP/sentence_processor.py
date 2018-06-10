#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#

#-- 3rd party imports --#
import spacy


class Sentence_processor(object):

    def __init__(self, language):
        if language == 'es':
            self.stop_words = ['la', 'el', 'de', 'decir', 'decirme', 'proporcionar', 'proporcionarme', 'muy', 'que', 'te', 'lo', ',', '!','?', 'es', 'ser',
                'estar', 'poder', 'bot', 'fibot', 'donde', 'cual', 'me', 'saber', 'conocer', 'indicar', 'indicarme', 'haber', 'quedar', 'tener']
        elif language == 'ca':
            self.stop_words = ['la', 'el', 'de', 'decir', 'decirme', 'proporcionar', 'proporcionarme', 'muy', 'que', 'te', 'lo', ',', '!','?', 'es', 'ser',
                'estar', 'poder', 'bot', 'fibot', 'donde', 'cual', 'me', 'saber', 'conocer', 'indicar', 'indicarme', 'haber', 'quedar', 'tener']
        else:
            self.stop_words = ['la', 'el', 'de', 'decir', 'decirme', 'proporcionar', 'proporcionarme', 'muy', 'que', 'te', 'lo', ',', '!','?', 'es', 'ser',
                'estar', 'poder', 'bot', 'fibot', 'donde', 'cual', 'me', 'saber', 'conocer', 'indicar', 'indicarme', 'haber', 'quedar', 'tener']
        if language == 'es' or language == 'ca':
            self.model = spacy.load('es')
        else:
            self.model = spacy.load('en')

    def remove_stop_words_and_lemmatize(self, sentence):
        print("This is the sentence processing {}".format(sentence))
        spacy_sentence = self.model(sentence)
        final_sentence = ""
        for token in spacy_sentence:
            print("analysing {}".format(token))
            if not token.lemma_.lower() in self.stop_words:
                if not final_sentence: final_sentence = str(token).lower()#.lemma_
                else: final_sentence = "{} {}".format(final_sentence, str(token).lower())#.lemma_)
        return final_sentence

    def process_sentence(self, sentence):
        processed_sentence = sentence
        processed_sentence = self.remove_stop_words_and_lemmatize(processed_sentence)
        return processed_sentence
