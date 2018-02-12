#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
import json
import os.path

#-- 3rd party imports --#
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer, Metadata, Interpreter
import spacy


class NLU_unit(object):

	""" This object contains the interpreter for the NLU model, and tools to train and retrieve it

	Attributes:
		name(:class:`rasa_nlu.model.Interpreter`): Interpreter for the users FIB-related queries
	"""
	def __init__(self):
		self.interpreter = None

	"""
		Parameters:
			train (:obj:`bool`): indicates if it has to re-train the model

		This function loads a model from persistency (if train == False)
		or re-trains and loads the trained model
	"""
	def load(self, train = False):
		if train:
			training_data = load_data('./Data/Dataset.json')
			print("Data Loaded")
			trainer = Trainer(RasaNLUConfig("./config/config_spacy.json"))
			print("Trainer launched")
			trainer.train(training_data)
			print("Training done")
			model_directory = trainer.persist('./models/default/')  # Returns the directory the model is stored in
			# where `model_directory points to the folder the model is persisted in
			self.interpreter = Interpreter.load(model_directory, RasaNLUConfig("./config/config_spacy.json"))
		else:
			self.interpreter = Interpreter.load("./models/projects/default/default/model_20180201-142832", RasaNLUConfig("./config/config_spacy.json"))

	"""
		Parameters:
			query (:obj:`str`): query or user messages

		This function returns the intent as predicted by the interpreter
	"""
	def get_intent(self, query):
		parsed = self.interpreter.parse(query)
		return parsed['intent']


	"""
		Parameters:
			query (:obj:`str`): query or user messages

		This function returns the entities as predicted by the interpreter
	"""
	def get_entities(self, query):
		parsed = self.interpreter.parse(query)
		return parsed['entities']



"""
if __name__ == '__main__':
	create_interpreter()

	query = input("Introduce query")
	intent = get_intent(query)
	entities = get_entities(query)
	print("For query: "+query)
	print("The intent is: " + str(intent))
	print("The entities are: " + str(entities))
"""
