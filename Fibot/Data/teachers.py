#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
import json
from itertools import combinations

#-- 3rd party imports --#
from nltk import edit_distance



class Teachers(object):

    def __init__(self):
        with open('./Data/urls_upc.json', 'r') as fp:
        	self.departments = json.load(fp).keys()
        self.data = {}
        for department in self.departments:
            with open('./Data/teachers/{}.json'.format(department), 'r') as fp:
            	self.data[department] = json.load(fp)
        print("Loaded teachers data for departments {}".format(self.departments))


    def get_closer_teacher(self, teacher_name, num_matches = 1):
        teacher_name = teacher_name.lower()
        min_values = (None, float("inf"))
        ret_list = {}
        for department in self.departments:
            for teacher in self.data[department].keys():
                teacher = teacher.lower()
                curr_dist = self.distance(teacher_name, teacher)
                if curr_dist < min_values[1]:
                    if len(ret_list.keys()) >= num_matches: ret_list.pop(min_values[0])
                    ret_list[teacher] = curr_dist
                    min_values = self.get_min_values(ret_list)
        return list(ret_list.items())


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


    def get_min_values(self, dict_ret):
        min_values = (None, -(float("inf")))
        for item, value in dict_ret.items():
            if value > min_values[1]:
                min_values = (item, value)
        return min_values
