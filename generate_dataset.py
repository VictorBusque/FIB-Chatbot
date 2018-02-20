#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- general imports --#
import json
import random


class Item_generator(object):

	def __init__(self, data, num_items = 9999):
		if isinstance(data, list):
			d_size = len(data)
			self.num_items = min(num_items, d_size)
			self.items = data[:self.num_items]
		else:
			d_size = len(open(data,'r').readlines())
			self.num_items = min(num_items, d_size)
			self.items = open(data,'r').readlines()[:self.num_items]

	def get_random(self):
		i_idx = random.randint(0, self.num_items-1)
		return self.items[i_idx]


class Data_generator(object):

	def __init__(self, i_g, s_g, type_, intent):
		self.i_g = i_g
		self.s_g = s_g
		self.type = type_
		self.intent = intent

	def get_examples(self, num_examples):
		examples = []
		for i in range(num_examples):
			examples.append(self.get_random_element())
		return examples


	def get_random_element(self):
		entity = self.i_g.get_random().lower().rstrip()
		sentence = self.s_g.get_random()
		offset_ini = 0
		for char in sentence:
			if char != "{":
				offset_ini += 1
			else: break
		offset_fi = offset_ini + len(entity)
		if self.type == 'teacher': entity_type = 'teacher_name'
		if self.type == 'subject': entity_type = 'subject_acronym'
		return {
			"text": sentence.format(entity),
			"intent": self.intent,
			"entities": [
				{
					'start': offset_ini,
					'end': offset_fi,
					'value': entity,
					'entity': entity_type,
				}
			]
		}


def main(amount = 250):

	intros_teacher_mail = ["{}'s mail", "what is {}'s mail", "what is {}'s mail?"]
	intros_teacher_desk = ["what's {}'s office?", "what's {}'s office", "{}'s office"]


	intros_subject_free_spots = ['free spots in {}', 'how many free spots are in {}?',
			'how many free spots are in {}', 'spots left in {}']
	intros_subject_schedule = ['schedule of {}', "what's {}'s schedule?",
			"what's {}'s schedule", 'when do i have {}']
	intros_subject_clasroom = ['in which class do i have {}?',
			'in which class do i have {}', "{}'s classroom", 'where do i have {}']
	intros_inform_teacher = ['the teacher is {}', '{}']
	intros_inform_subject = ['the subject is ', '{}']

	regex_features = []
	entity_synonyms = []
	common_examples = []

	teacher_gen = Item_generator(data = "./Data/Professors.txt")
	subject_gen = Item_generator(data = "./Data/Subjects.txt")

	intro_mail_gen = Item_generator(data = intros_teacher_mail)
	intro_desk_gen = Item_generator(data = intros_teacher_desk)
	intro_spots_gen = Item_generator(data = intros_subject_free_spots)
	intro_schedule_gen = Item_generator(data = intros_subject_schedule)
	intro_classroom_gen = Item_generator(data = intros_subject_clasroom)
	intro_inform_teacher_gen = Item_generator(data = intros_inform_teacher)
	intro_inform_subject_gen = Item_generator(data = intros_inform_subject)

	teacher_mail_gen = Data_generator(teacher_gen, intro_mail_gen, type_="teacher", intent="ask_teacher_mail")
	teacher_desk_gen = Data_generator(teacher_gen, intro_desk_gen, type_="teacher", intent="ask_teacher_office")
	subject_spots_gen = Data_generator(subject_gen, intro_spots_gen, type_="subject", intent="ask_free_spots")
	subject_schedule_gen = Data_generator(subject_gen, intro_schedule_gen, type_="subject", intent="ask_subject_schedule")
	subject_classroom_gen = Data_generator(subject_gen, intro_classroom_gen, type_="subject", intent="ask_subject_classroom")
	inform_teacher_gen = Data_generator(teacher_gen, intro_inform_teacher_gen, type_="teacher", intent="inform")
	inform_subject_gen = Data_generator(subject_gen, intro_inform_subject_gen, type_="subject", intent="inform")

	common_examples.extend( teacher_mail_gen.get_examples(amount) )
	common_examples.extend( teacher_desk_gen.get_examples(amount) )
	common_examples.extend( subject_spots_gen.get_examples(amount) )
	common_examples.extend( subject_schedule_gen.get_examples(amount) )
	common_examples.extend( subject_classroom_gen.get_examples(amount) )
	#common_examples.extend( inform_teacher_gen.get_examples(amount) )
	#common_examples.extend( inform_subject_gen.get_examples(amount) )

	result = {"rasa_nlu_data": {
					"regex_features": regex_features,
					"entity_synonyms": entity_synonyms,
					"common_examples": common_examples}
			 }
	print ( "Size of the dataset: {}".format(len(common_examples)))
	json_ = str(json.dumps(result, indent=2))
	file = open("./Data/Dataset.json","w")
	file.write(json_)
	file.close()


if __name__ == "__main__":
	amount = input("How many examples for each type? ")
	if amount: main(int(amount))
	else: main()
