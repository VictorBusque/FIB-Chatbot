#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
import json
import os.path
from time import time

#-- 3rd party imports --#
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer, Metadata, Interpreter
import spacy


class NLU_unit(object):

	""" This object contains the interpreter for the NLU model, and tools to train and retrieve it

	Attributes:
		interpreter_ca(:class:`rasa_nlu.model.Interpreter`): Interpreter for the users FIB-related queries in catalan
		interpreter_es(:class:`rasa_nlu.model.Interpreter`): Interpreter for the users FIB-related queries in spanish
		interpreter_en(:class:`rasa_nlu.model.Interpreter`): Interpreter for the users FIB-related queries in english
	"""
	def __init__(self):
		self.interpreter_ca = None
		self.interpreter_es = None
		self.interpreter_en = None

	"""
		Parameters:
			train (:obj:`bool`): indicates if it has to re-train the model

		This function loads a model from persistency (if train == False)
		or re-trains and loads the trained model
	"""
	def load(self, train = False, train_list = None):
		if train:
			print("Training this languages: {}".format(train_list))
			now = time()
			if not train_list or 'ca' in train_list:
				print("Training CA NLU model")
				training_data_ca = load_data('./Data/Dataset_ca.json')
				trainer_ca = Trainer(config.load("./config/config_spacy_ca.yml"))
				trainer_ca.train(training_data_ca, num_threads=3)
				model_directory = trainer_ca.persist('models/nlu_ca', fixed_model_name = 'current')  # Returns the directory the model is stored in
				print("Total elapsed time for CA: {}".format(time()-now))
			now = time()
			if not train_list or 'es' in train_list:
				print("Training ES NLU model")
				training_data_es = load_data('./Data/Dataset_es.json')
				trainer_es = Trainer(config.load("./config/config_spacy_es.yml"))
				trainer_es.train(training_data_es, num_threads=3)
				model_directory = trainer_es.persist('models/nlu_es', fixed_model_name = 'current')  # Returns the directory the model is stored in
				print("Total elapsed time for ES: {}".format(time()-now))
			now = time()
			if not train_list or 'en' in train_list:
				print("Training EN NLU model")
				training_data_en = load_data('./Data/Dataset_en.json')
				trainer_en = Trainer(config.load("./config/config_spacy_en.yml"))
				trainer_en.train(training_data_en, num_threads=3)
				model_directory = trainer_en.persist('models/nlu_en', fixed_model_name = 'current')  # Returns the directory the model is stored in
				print("Total elapsed time for EN: {}".format(time()-now))
			print("NLU Training done")
			# where `model_directory points to the folder the model is persisted in
		self.interpreter_ca = RasaNLUInterpreter("./models/nlu_ca/default/current")
		self.interpreter_es = RasaNLUInterpreter("./models/nlu_es/default/current")
		self.interpreter_en = RasaNLUInterpreter("./models/nlu_en/default/current")
		print("NLU loaded")

	"""
		Parameters:
			query (:obj:`str`): query or user messages

		This function returns the intent as predicted by the interpreter
	"""
	def get_intent(self, query, lang = 'es'):
		parsed = None
		if lang == 'ca':
			parsed = self.interpreter_ca.parse(query)
		elif lang == 'es':
			parsed = self.interpreter_es.parse(query)
		else:
			parsed = self.interpreter_en.parse(query)
		return parsed['intent']

	def get_intent_ranking(self, query, lang = 'es'):
		parsed = None
		if lang == 'ca':
			parsed = self.interpreter_ca.parse(query)
		elif lang == 'es':
			parsed = self.interpreter_es.parse(query)
		else:
			parsed = self.interpreter_en.parse(query)
		return parsed['intent_ranking']

	"""
		Parameters:
			query (:obj:`str`): query or user messages

		This function returns the entities as predicted by the interpreter
	"""
	def get_entities(self, query, lang= 'es'):
		parsed = None
		if lang == 'ca':
			parsed = self.interpreter_ca.parse(query)
		elif lang == 'es':
			parsed = self.interpreter_es.parse(query)
		else:
			parsed = self.interpreter_en.parse(query)
		return parsed['entities']
