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


class Teacher_name_classifier(object):

    def __init__(self, path_to_data = './Data/Names/'):
        self.names_data = pd.read_csv(path_to_data+'{}.csv'.format('names'), delimiter=',', header = 0)[['Nombre']]
        self.names_data = list(map(str.lower, self.names_data['Nombre'].values.tolist()))
        self.process()

    def process(self):
        for idx, item in enumerate(self.names_data):
            if '/' in item:
                print(item)
                name1, garbo = item.split('/')
                print("{} - {}".format(name1, garbo))
                name1 = name1.lower()
                self.names_data[idx] = name1



    def is_name(self, word):
        word = word.lower()
        for accent in accents:
            word = word.replace(accent,'�')
        print(word)
        for name in self.names_data:
            name = self.delete_accents(name)
            print("{} - {}".format(word, name))
            if edit_distance(word, name) == 0: return True
        return False


    def get_name(self, word):
        return

    def get_surname(self, word):
        return

    def delete_accents(self, word):
        return ''.join((c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn'))

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
        print("Loaded teachers data for departments {}".format(self.departments))

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
        if debug: print("{} is the distance.".format(lower_dist))
        return Teacher(match, language = self.language)

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

    """
        Helper in order to find list of matches (not used atm)
    """
    def get_min_values(self, dict_ret):
        min_values = (None, -(float("inf")))
        for name, value in dict_ret.items():
            if value > min_values[1]:
                min_values = (name, value)
        return min_values
