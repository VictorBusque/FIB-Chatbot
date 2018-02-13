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
		entity = self.i_g.get_random().rstrip()
		sentence = self.s_g.get_random()
		if self.type == 'teacher':
			name, surnames = entity.split(' ')[0], entity[len(entity.split(' ')[0])+1:]
			offset_ini_name = len(sentence)
			offset_fi_name = offset_ini_name + len(name)
			offset_ini_surname = offset_fi_name+1
			offset_fi_surname = offset_ini_name + len(name)
			return {
				"text": "{}{}".format(sentence, entity),
				"intent": self.intent,
				"entities": [
					{
						'start': offset_ini_name,
						'end': offset_fi_name,
						'value': name,
						'entity': 'teacher_name',
					},
					{
						'start': offset_ini_surname,
						'end': offset_fi_surname,
						'value': surnames,
						'entity': 'teacher_surname',
					}
				]
			}
		if self.type == 'subject':
			offset_ini = len(sentence)
			offset_fi = offset_ini + len(entity)
			return {
				"text": "{}{}".format(sentence, entity),
				"intent": self.intent,
				"entities": [
					{
						'start': offset_ini,
						'end': offset_fi,
						'value': entity,
						'entity': 'subject_acronym',
					}
				]
			}


def main(amount = 250):

	intros_teacher_mail = ['cual es el correo de ', 'correo de ']
	intros_teacher_desk = ['cual es el despacho de ', 'despacho de ', 'dime el despacho de ']


	intros_subject_free_spots = ['plazas libres de ', 'cuantas plazas quedan de ', 'plazas de ']
	intros_subject_schedule = ['horario de ', 'cual es el horario de ', 'a que hora tengo ']
	intros_subject_clasroom = ['en que clase hay ', 'en que clase tengo ', 'donde tengo ']

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

	teacher_mail_gen = Data_generator(teacher_gen, intro_mail_gen, type_="teacher", intent="ask_teacher_mail")
	teacher_desk_gen = Data_generator(teacher_gen, intro_desk_gen, type_="teacher", intent="ask_teacher_desk")
	subject_spots_gen = Data_generator(subject_gen, intro_spots_gen, type_="subject", intent="ask_free_spots")
	subject_schedule_gen = Data_generator(subject_gen, intro_schedule_gen, type_="subject", intent="ask_subject_schedule")
	subject_classroom_gen = Data_generator(subject_gen, intro_classroom_gen, type_="subject", intent="ask_subject_classroom")

	common_examples.extend( teacher_mail_gen.get_examples(amount) )
	common_examples.extend( teacher_desk_gen.get_examples(amount) )
	common_examples.extend( subject_spots_gen.get_examples(amount) )
	common_examples.extend( subject_schedule_gen.get_examples(amount) )
	common_examples.extend( subject_classroom_gen.get_examples(amount) )

	result = {"rasa_nlu_data": {
					"regex_features": regex_features,
					"entity_synonyms": entity_synonyms,
					"common_examples": common_examples}
			 }
	print ("Size of the dataset: %d"%len(common_examples))
	json_ = str(json.dumps(result, indent=2))
	file = open("./Data/Dataset.json","w")
	file.write(json_)
	file.close()


if __name__ == "__main__":
	amount = input("How many examples for each type?")
	if amount: main(int(amount))
	else: main()
