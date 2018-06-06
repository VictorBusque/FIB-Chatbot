#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#

#-- 3rd party imports --#
import spacy

class Sentence_processor(object):

    def __init__(self, language):
        if language == 'es' or language == 'ca':
            self.model = spacy.load('es_core_news_sd')
        else:
            self.model = spacy.load('en_core_web_sg')

    def remove_stop_words_and_lemmatize(self, sentence):
        spacy_sentence = self.model(sentence)
        final_sentence = ""
        for token in spacy_sentence:
            if not token.is_stop:
                if not final_sentence: final_sentence = tokrn.lemma_
                else: final_sentence = "{} {}".format(final_sentence, token.lemma_)
        return final_sentence

    def process_sentence(self, sentence):
        processed_sentence = sentence
        processed_sentence = self.remove_stop_words_and_lemmatize(processed_sentence)
        return processed_sentence
