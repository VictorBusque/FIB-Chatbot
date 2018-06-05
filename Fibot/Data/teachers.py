#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
import json
from itertools import combinations
import pandas as pd
import unicodedata

#-- 3rd party imports --#
from nltk import edit_distance

#-- Local imports --#
from Fibot.Data.data_types.teacher import Teacher


class Teachers(object):

    """This class allows the bot to interact with the teachers information
    as scraped by the scrap_teachers.py script.

    So it allows to find matches from teachers names as inputed by users to real
    teachers in the database (see Data/teachers folder)

    Attributes:
        departments(:obj:`list`): List of the current departments in the database
        data(:obj:`dict`): Dictionary that maps departments to a dictionary of teachers and info
    """
    def __init__(self,  language = 'es'):
        with open('./Data/urls_upc.json', 'r') as fp:
        	self.departments = json.load(fp).keys()
        self.data = {}
        self.language = language
        for department in self.departments:
            with open('./Data/teachers/{}.json'.format(department), 'r') as fp:
            	self.data[department] = json.load(fp)
        print("Cargados en memoria los profesores de los departamentos {}".format(list(self.departments)))
        return

    """
        Parameters:
            teacher_name (:obj:`str`): String of the user's input to find matches of

        This function returns:
            (:class:`Fibot.Data.data_types.teacher`): The instance of the teacher that
            best matches the user query based on the edit distance measure.
    """
    def get_closer_teacher(self, teacher_name, debug=True):
        teacher_name = teacher_name.lower()
        lower_dist = float("inf")
        match_department, match_teacher = None, None
        for department in self.departments:
            for teacher in self.data[department].keys():
                teacher = teacher.lower()
                curr_dist = self.distance(teacher_name, teacher)
                if curr_dist < lower_dist:
                    match_department, match_teacher = department, teacher
                    lower_dist = curr_dist
        match = self.data[match_department][match_teacher]
        match['name'] = match_teacher
        match['department'] = match_department
        if debug: print("Distancia al profesor más cercano: {}\nEl profesor más parecido es: {}.".format(lower_dist, match_teacher))
        return Teacher(match, language = self.language), lower_dist


    """
        Parameters:
            word1 (:obj:`str`): word to compare
            word2 (:obj:`str`): other word to be compared to

        This function computes the edit distance between any possible combination of the word2
        order taking as many words as words in word1.
        And returns the minimum distance found:

        Example:
            distance("Javier Bejar", "Javier Bejar Alonso") = 0
            distance("Roberto Nieuwenhuis", "Robert Lukas Mario Nieuwenhuis") = 1
    """
    def distance(self, word1, word2):
        word2_split = word2.split(' ')
        len1 = len(word1.split(' '))
        len2 = len(word2_split)
        if len1 > len2: return float("inf")
        min_dist = float("inf")
        for word in combinations(word2_split, len1):
            word = ' '.join(word)
            min_dist = min(min_dist, edit_distance(word1, word))
        return min_dist
