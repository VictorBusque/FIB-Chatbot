#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
import json
import os.path
from time import time

#-- 3rd party imports --#
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
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
	def load(self, train = False):
		if train:
			now = time()
			training_data_ca = load_data('./Data/Dataset_ca.json')
			training_data_es = load_data('./Data/Dataset_es.json')
			training_data_en = load_data('./Data/Dataset_en.json')
			print("Data Loaded in {}s".format(time()-now))
			now = time()
			trainer_ca = Trainer(RasaNLUConfig("./config/config_spacy_ca.json"))
			trainer_es = Trainer(RasaNLUConfig("./config/config_spacy_es.json"))
			trainer_en = Trainer(RasaNLUConfig("./config/config_spacy_en.json"))
			print("NLU Trainer launched in {}s".format(time()-now))
			print("Training CA NLU model")
			trainer_ca.train(training_data_ca)
			print("Training ES NLU model")
			trainer_es.train(training_data_es)
			print("Training EN NLU model")
			trainer_en.train(training_data_en)
			print("NLU Training done")
			model_directory = trainer_ca.persist('models/nlu_ca', fixed_model_name = 'current')  # Returns the directory the model is stored in
			model_directory = trainer_es.persist('models/nlu_es', fixed_model_name = 'current')  # Returns the directory the model is stored in
			model_directory = trainer_en.persist('models/nlu_en', fixed_model_name = 'current')  # Returns the directory the model is stored in
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

	"""
		Parameters:
			query (:obj:`str`): query or user messages

		This function returns the entities as predicted by the interpreter
	"""
	def get_entities(self, query, lang):
		parsed = None
		if lang == 'ca':
			parsed = self.interpreter_ca.parse(query)
		elif lang == 'es':
			parsed = self.interpreter_es.parse(query)
		else:
			parsed = self.interpreter_en.parse(query)
		return parsed['entities']
