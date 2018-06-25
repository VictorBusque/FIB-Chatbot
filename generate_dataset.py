#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- general imports --#
import json
import random


class Item_generator(object):

	"""This class allows random generation of items (such as teachers)

		Parameters:
			data(:obj:`list` or :obj:`str`): list of items or path to get the file with
				the data
			num_items(:obj:`int`): limit of items that the generator can generate

		Attributes:
			num_items(:obj:`int`): limit of items that the generator can generate
			items(:obj:`list`): list of the items that can be generated
	"""
	def __init__(self, data, num_items = 9999, name = False):
		self.name = name
		if isinstance(data, list):
			d_size = len(data)
			self.num_items = min(num_items, d_size)
			self.items = data[:self.num_items]
		else:
			d_size = len(open(data,'r').readlines())
			self.num_items = min(num_items, d_size)
			self.items = open(data,'r').readlines()[:self.num_items]
	"""
		Returns a random element of the item list
	"""
	def get_random(self):
		i_idx = random.randint(0, self.num_items-1)
		shorten = random.randint(0,100) <= 50;
		if shorten and self.name:
			length = random.randint(1, len(self.items[i_idx])-1)
			return ' '.join(self.items[i_idx].split(' ')[0:length])
		return self.items[i_idx]


class Data_generator(object):

	"""This class allows random generation of data (for instance, questions)

		Parameters:
			i_g(:class:`Item_generator`): Item generator for the data (items)
			s_g(:class:`Item_generator`): Item generator for the sentences (not items)
			type_(:type:`str`): can either be 'teacher' or 'subject', defines the type of item used
			intent(:type:`str`): defines the intent of the sentence to be generated

		Attributes:
			num_items(:obj:`int`): limit of items that the generator can generate
			items(:obj:`list`): list of the items that can be generated
	"""
	def __init__(self, i_g, s_g, type_, intent, language = 'ca'):
		if i_g: self.i_g = i_g
		else: self.i_g = None
		self.s_g = s_g
		self.type = type_
		self.intent = intent
		self.language = language

	"""
		Parameters:
			num_examples(:obj:`int`): defines the amount of examples to be generated

		This function returns a list (of size num_examples) of random generated examples
	"""
	def get_examples(self, num_examples):
		examples = []
		for i in range(num_examples):
			examples.append(self.get_random_element())
		return examples

	"""
		This function returns a random sentence generated with both generators
	"""
	def get_random_element(self):
		sentence = self.s_g.get_random()
		if self.intent == "ask_free_spots":
			chosen_grp = random.randint(10, 45)
			grp_str = "grup"
			if self.language == 'es': grp_str = "grupo"
			elif self.language == 'en': grp_str = "group"
			aux = grp_str+' {}'
			sentence = sentence.replace(aux, aux.format(chosen_grp))
		if self.i_g and "{}" in sentence:
			entity = self.i_g.get_random().lower().rstrip()
			offset_ini = 0
			for char in sentence:
				if char != "{":
					offset_ini += 1
				else: break
			offset_fi = offset_ini + len(entity)
			sentence = sentence.format(entity)
			if self.type == 'teacher': entity_type = 'teacher_name'
			if self.type == 'subject': entity_type = 'subject_acronym'
			if self.intent == "ask_free_spots" and grp_str in sentence:
				grp_start = sentence.find(grp_str)+len(grp_str)+1
				grp_end = grp_start+2;
				return {
					"text": sentence,
					"intent": self.intent,
					"entities": [
						{
							'start': offset_ini,
							'end': offset_fi,
							'value': entity,
							'entity': entity_type,
						},
						{
							'start': grp_start,
							'end': grp_end,
							'value': '{}'.format(chosen_grp),
							'entity': 'group',
						}
					]
				}
			else:
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
		else:
			return {
				"text": sentence,
				"intent": self.intent
			}


def main(amount = 250, language = 'es'):
	random.seed(22)
	with open('Data/data_gen.json', 'rb') as jsonfile:
		data = json.load(jsonfile)[language]

	regex_features = [
		{
			"name": "group",
			"pattern": "([0-9]{2}|grup.|group)"
		},
		{
			"name": "plazas",
			"pattern": "(sitios|plazas|huecos|spots|places|matr.cula)"
		},
		{
			"name": "mail",
			"pattern": "(mail|corre.|email)"
		},
		{
			"name": "despacho",
			"pattern": "(despacho|oficina|office|despatx)"
		},
		{
			"name": "hora",
			"pattern": "(hora)"
		},
		{
			"name": "aula",
			"pattern": "(aula)"
		},
		{
			"name": "examen",
			"pattern": "(ex.m|test)"
		},
		{
			"name": "practicas",
			"pattern": "(pr.ct)"
		},
		{
			"name": "saludo",
			"pattern": "(hola|hello|buen|hey)"
		},
		{
			"name": "gracias",
			"pattern": "(gr.ci|thank|ty)"
		}
	]
	entity_synonyms = []
	common_examples = []

	teacher_gen = Item_generator(data = "./Data/Professors.txt", name = True)
	subject_gen = Item_generator(data = "./Data/Subjects.txt")

	intro_mail_gen = Item_generator(data = data['intros_teacher_mail'])
	intro_desk_gen = Item_generator(data = data['intros_teacher_desk'])
	intro_spots_gen = Item_generator(data = data['intros_subject_free_spots'])
	intro_schedule_gen = Item_generator(data = data['intros_subject_schedule'])
	intro_classroom_gen = Item_generator(data = data['intros_subject_clasroom'])
	intro_subject_teacher_mail_gen = Item_generator(data = data['intros_subject_teacher_mail'])
	intro_subject_teacher_office_gen = Item_generator(data = data['intros_subject_teacher_office'])
	intro_subject_teacher_name_gen = Item_generator(data = data['intros_subject_teacher_name'])
	intro_next_class_gen = Item_generator(data = data['intros_now_class'])
	intro_exams_gen = Item_generator(data = data['intros_exams'])
	intro_pracs_gen = Item_generator(data = data['intros_pracs'])
	intro_inform_gen = Item_generator(data = data['intros_inform'])
	intro_greet_gen = Item_generator(data = data['greet'])
	intro_thank_gen = Item_generator(data = data['thank'])
	#intro_inform_teacher_gen = Item_generator(data = intros_inform_teacher)
	#intro_inform_subject_gen = Item_generator(data = intros_inform_subject)

	teacher_mail_gen = Data_generator(teacher_gen, intro_mail_gen, type_="teacher", intent="ask_teacher_mail")
	teacher_desk_gen = Data_generator(teacher_gen, intro_desk_gen, type_="teacher", intent="ask_teacher_office")
	subject_spots_gen = Data_generator(subject_gen, intro_spots_gen, type_="subject", intent="ask_free_spots", language = language)
	subject_schedule_gen = Data_generator(subject_gen, intro_schedule_gen, type_="subject", intent="ask_subject_schedule")
	subject_classroom_gen = Data_generator(subject_gen, intro_classroom_gen, type_="subject", intent="ask_subject_classroom")
	subject_teacher_mail_gen = Data_generator(subject_gen, intro_subject_teacher_mail_gen, type_ ="subject", intent = "ask_subject_teacher_mail")
	subject_teacher_office_gen = Data_generator(subject_gen, intro_subject_teacher_office_gen, type_ = "subject", intent = "ask_subject_teacher_office")
	subject_teacher_name_gen = Data_generator(subject_gen, intro_subject_teacher_name_gen, type_="subject", intent = "ask_subject_teacher_name")
	next_class_gen = Data_generator(None, intro_next_class_gen, type_ = None, intent = "ask_next_class")
	next_exam_gen = Data_generator(subject_gen, intro_exams_gen, type_="subject", intent = "ask_exams")
	next_pracs_gen = Data_generator(subject_gen, intro_pracs_gen, type_ = "subject", intent = "ask_pracs")
	inform_subject = Data_generator(subject_gen, intro_inform_gen, type_ = "subject", intent = "inform")
	inform_teacher = Data_generator(teacher_gen, intro_inform_gen, type_ = "teacher", intent = "inform")
	greet = Data_generator(None, intro_greet_gen, type_ = None, intent = "greet")
	thank = Data_generator(None, intro_thank_gen, type_ = None, intent = "thank")
	#inform_teacher_gen = Data_generator(teacher_gen, intro_inform_teacher_gen, type_="teacher", intent="inform")
	#inform_subject_gen = Data_generator(subject_gen, intro_inform_subject_gen, type_="subject", intent="inform")

	common_examples.extend( teacher_mail_gen.get_examples(amount) )
	common_examples.extend( teacher_desk_gen.get_examples(amount) )
	common_examples.extend( subject_spots_gen.get_examples(amount) )
	common_examples.extend( subject_schedule_gen.get_examples(amount) )
	common_examples.extend( subject_classroom_gen.get_examples(amount) )
	common_examples.extend( subject_teacher_mail_gen.get_examples(amount) )
	common_examples.extend( subject_teacher_office_gen.get_examples(amount) )
	common_examples.extend( subject_teacher_name_gen.get_examples(amount) )
	common_examples.extend( next_class_gen.get_examples(amount) )
	common_examples.extend( next_exam_gen.get_examples(amount) )
	common_examples.extend( next_pracs_gen.get_examples(amount) )
	common_examples.extend( inform_subject.get_examples(amount) )
	common_examples.extend( inform_teacher.get_examples(amount) )
	common_examples.extend( greet.get_examples(amount) )
	common_examples.extend( thank.get_examples(amount) )
	#common_examples.extend( inform_teacher_gen.get_examples(amount) )
	#common_examples.extend( inform_subject_gen.get_examples(amount) )

	file_path = './Data/Dataset_{}.json'.format(language)

	result = {"rasa_nlu_data": {
					"regex_features": regex_features,
					"entity_synonyms": entity_synonyms,
					"common_examples": common_examples}
			 }
	print ( "Size of the dataset: {}".format(len(common_examples)))
	json_ = str(json.dumps(result, indent=2))
	file = open(file_path,"w")
	file.write(json_)
	file.close()


if __name__ == "__main__":
	language = input("Qué idioma quieres generar? (es/ca/en/all)\n")
	if not (language == 'ca' or language == 'es' or language == 'en' or language == 'all'):
		language = None
	amount = input("How many examples for each type? ")
	if amount:
		if language == 'all':
			main(int(amount), 'ca')
			main(int(amount), 'es')
			main(int(amount), 'en')
		else: main(int(amount), language)
	else: main(language)
