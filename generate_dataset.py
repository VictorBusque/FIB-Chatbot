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
	def __init__(self, data, num_items = 9999):
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
	def __init__(self, i_g, s_g, type_, intent):
		self.i_g = i_g
		self.s_g = s_g
		self.type = type_
		self.intent = intent

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


def main(amount = 250, language = 'es'):
	intros_teacher_mail = ["correo de {}", "cual es el correo de {}", "cual es el correo de {}?", "mail de {}", "cual es el mail de {}?"]
	intros_teacher_desk = ["cual es el despacho de {}?", "cual es el despacho de {}", "despacho de {}", "donde esta el despacho de {}?", "dónde está el despacho de {}"]
	intros_subject_free_spots = ['plazas libres en {}', 'plazas libres de {}', 'cuantas plazas libres quedan en {}?',
			'cuantos huecos hay en {}', 'plazas de {}', 'plazas en {}', "cuantas plazas libres hay en {}?",
			"plazas en {}", "cuantas plazas hay en {}"]
	intros_subject_schedule = ['horario de {}', "cual es el horario de {}?",
			"cuando tengo {}?", 'cuando tengo{}', "cuando hago {}?", "cuando hago {}"]
	intros_subject_clasroom = ['en que clase hago {}?', "en que clase tengo {}",
			'donde hago {}', "clase de {}", 'cual es la clase de {}?',
			"aula de {}", "en que aula tengo {}"]
	if language == 'en':
		intros_teacher_mail = ["{}'s mail", "what is {}'s mail", "what is {}'s mail?", "mail of {}", "what's the mail of {}"]
		intros_teacher_desk = ["what's {}'s office?", "what's {}'s office", "{}'s office", "office of {}", "what's the office of {}"]
		intros_subject_free_spots = ['free spots in {}', 'how many free spots are in {}?',
				'how many free spots are in {}', 'spots left in {}', "how many free spots are there in {}",
				"free spots of {}", "{}'s free spots"]
		intros_subject_schedule = ['schedule of {}', "what's {}'s schedule?",
				"what's {}'s schedule", 'when do i have {}', "when do i do {}"]
		intros_subject_clasroom = ['in which class do i have {}?', "where do i do {}",
				'in which class do i have {}', "{}'s classroom", 'where do i have {}',
				"classroom of {}", "class of {}"]
		intros_inform_teacher = ['the teacher is {}', '{}']
		intros_inform_subject = ['the subject is ', '{}']
		#intros_inform_teacher = ['the teacher is {}', '{}']
		#intros_inform_subject = ['the subject is ', '{}']
	elif language == 'ca':
		intros_teacher_mail = ["correu de {}", "quin es el correu de {}", "quin es el mail de {}?", "mail de {}", "quin és el mail de {}?"]
		intros_teacher_desk = ["quin es el despatx de {}?", "quin és el despatx {}", "despatx de {}", "on esta el despatx de {}?", "on es el despatx de {}"]
		intros_subject_free_spots = ['places lliures en {}', 'places lliures de {}', 'quantes places lliures queden a {}?',
				'quants espais hi ha a {}', 'places de {}', 'places a {}', "quantes places lliures hi ha a {}?",
				"plazas en {}", "cuantas plazas hay en {}"]
		intros_subject_schedule = ['horari de {}', "quin és l'horari de {}?",
				"quant tinc {}?", 'quan hi ha {}', "quan faig {}?", "quan tindré {}"]
		intros_subject_clasroom = ['a quina classe faig{}?', "a quina classe faig {}",
				'on tinc {}', "aula de {}", 'quina és la classe de {}?',
				"aula de {}", "a quina aula tinc {}?"]
		#intros_inform_teacher = ['the teacher is {}', '{}']
		#intros_inform_subject = ['the subject is ', '{}']

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
	#intro_inform_teacher_gen = Item_generator(data = intros_inform_teacher)
	#intro_inform_subject_gen = Item_generator(data = intros_inform_subject)

	teacher_mail_gen = Data_generator(teacher_gen, intro_mail_gen, type_="teacher", intent="ask_teacher_mail")
	teacher_desk_gen = Data_generator(teacher_gen, intro_desk_gen, type_="teacher", intent="ask_teacher_office")
	subject_spots_gen = Data_generator(subject_gen, intro_spots_gen, type_="subject", intent="ask_free_spots")
	subject_schedule_gen = Data_generator(subject_gen, intro_schedule_gen, type_="subject", intent="ask_subject_schedule")
	subject_classroom_gen = Data_generator(subject_gen, intro_classroom_gen, type_="subject", intent="ask_subject_classroom")
	#inform_teacher_gen = Data_generator(teacher_gen, intro_inform_teacher_gen, type_="teacher", intent="inform")
	#inform_subject_gen = Data_generator(subject_gen, intro_inform_subject_gen, type_="subject", intent="inform")

	common_examples.extend( teacher_mail_gen.get_examples(amount) )
	common_examples.extend( teacher_desk_gen.get_examples(amount) )
	common_examples.extend( subject_spots_gen.get_examples(amount) )
	common_examples.extend( subject_schedule_gen.get_examples(amount) )
	common_examples.extend( subject_classroom_gen.get_examples(amount) )
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
	language = input("Qué idioma quieres generar? (es/ca/en)")
	if not (language == 'ca' or language == 'es' or language == 'en'):
		language = None
	amount = input("How many examples for each type? ")
	if amount: main(int(amount), language)
	else: main(language)
