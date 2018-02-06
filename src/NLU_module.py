from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import (Trainer, Metadata, Interpreter)
import spacy
import json
import os.path

interpreter = ""


def create_interpreter(train = False):
	global interpreter
	if train:
		training_data = load_data('./Data/Dataset.json')
		print("Data Loaded")
		trainer = Trainer(RasaNLUConfig("./src/config_spacy.json"))
		print("Trainer launched")
		trainer.train(training_data)
		print("Training done")
		model_directory = trainer.persist('./projects/default/')  # Returns the directory the model is stored in
		# where `model_directory points to the folder the model is persisted in
		interpreter = Interpreter.load(model_directory, RasaNLUConfig("./src/config_spacy.json"))
	else:
		interpreter = Interpreter.load("./projects/default/default/model_20180201-142832", RasaNLUConfig("./src/config_spacy.json"))
	print("NLU model loaded")


def get_intent(query):
	global interpreter
	parsed = interpreter.parse(query)
	return parsed['intent']


def get_entities(query):
	global interpreter
	parsed = interpreter.parse(query)
	return parsed['entities']


def get_interpreter():
	return interpreter


if __name__ == '__main__':
	create_interpreter()

	query = input("Introduce query")
	intent = get_intent(query)
	entities = get_entities(query)
	print("For query: "+query)
	print("The intent is: " + str(intent))
	print("The entities are: " + str(entities))
