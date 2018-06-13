#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
import os
import requests
from pprint import pprint
from random import randint
from termcolor import colored
import json

#-- 3rd party imports --#
from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.channels import UserMessage
from rasa_core.channels.console import ConsoleInputChannel
from telegram import ChatAction

#-- local imports --#
from Fibot.NLP.nlu import NLU_unit


class Query_answer_unit(object):

	""" This object contains tools to answer in natural language any message Fib related

	Attributes:
		nlu(:class:`Fibot.NLP.nlu.NLU_unit`): Object that interprets queries
		training_data_file(:obj:`str`): String indicating the path to the stories markdown file
		model_path(:obj:`str`): String indicating where the dialog model is
		agent_ca(:class:`rasa_core.agent.Agent`): Agent capable of handling any incoming messages in catalan
		agent_es(:class:`rasa_core.agent.Agent`): Agent capable of handling any incoming messages in spanish
		agent_en(:class:`rasa_core.agent.Agent`): Agent capable of handling any incoming messages in english
	"""
	def __init__(self):
		self.nlu = NLU_unit()
		self.training_data_file = './Fibot/NLP/core/stories.md'
		self.domain_path = './Fibot/NLP/core/domain.yml'
		self.model_path = './models/dialogue'
		self.agent_ca =  Agent(self.domain_path,
			                  policies=[MemoizationPolicy(), KerasPolicy()])
		self.agent_es =  Agent(self.domain_path,
							  policies=[MemoizationPolicy(), KerasPolicy()])
		self.agent_en =  Agent(self.domain_path,
							  policies=[MemoizationPolicy(), KerasPolicy()])
		self.agent_ca.toggle_memoization(activate = True)
		self.agent_es.toggle_memoization(activate = True)
		self.agent_en.toggle_memoization(activate = True)


	def log(self, text):
		print(colored("LOG: {}".format(text), 'cyan'))

	"""
		Parameters:
			train (:obj:`bool`): Specifies if the agents have to be trained
		This function loads the model into the agents, and trains them if necessary
	"""
	def load(self, trainNLG=False, trainNLU=False, train_list = None):
		self.log("Cargando word vectors")
		self.nlu.load(trainNLU, train_list = train_list)
		self.log("Modelos NLU cargados")
		if trainNLG: self.train()
		self.agent_ca = Agent.load(self.model_path,
				interpreter = self.nlu.interpreter_ca)
		self.agent_es = Agent.load(self.model_path,
				interpreter = self.nlu.interpreter_es)
		self.agent_en = Agent.load(self.model_path,
				interpreter = self.nlu.interpreter_en)
		self.log("Agentes de diálogo cargados")

	"""
		Parameters:
			augmentation_factor (:obj:`int`): augmentation factor for the training
			max_history (:obj:`int`): max_history factor for the training
			epochs (:obj:`int`): epochs (steps) for the training
			batch_size (:obj:`int`): batch_size for the training
			validation_split (:obj:`int`): validation_split factor for the error calculation

		This function trains the agents and saves the models in the dialog's model path
	"""
	def train(self, augmentation_factor=200, max_history=7, epochs=300, batch_size=256, validation_split=0.3):
		self.agent_es.train(self.training_data_file,
			#augmentation_factor=augmentation_factor,
			#max_history=max_history,
			epochs=epochs,
		 	batch_size=batch_size,
			validation_split=validation_split
		)
		self.agent_es.persist(self.model_path)

	"""
		Parameters:
			augmentation_factor (:obj:`int`): augmentation factor for the training
			max_history (:obj:`int`): max_history factor for the training
			epochs (:obj:`int`): epochs (steps) for the training
			batch_size (:obj:`int`): batch_size for the training
			validation_split (:obj:`int`): validation_split factor for the error calculation

		This function makes it possible to generate new stories manually.
	"""
	def train_manual(self, augmentation_factor=50, max_history=2, epochs=500, batch_size=50, validation_split=0.2):
		self.agent_es.train_online(self.training_data_file,
			input_channel = ConsoleInputChannel(),
			augmentation_factor=augmentation_factor,
			max_history=max_history,
			epochs=epochs,
		 	batch_size=batch_size,
			validation_split=validation_split
		)

	"""
		Parameters:
			message (:obj:`str`): the incoming message from some user
			sender_id(:obj:`str`): The id (chat_id) of the sender of the messages
			language(:obj:`str`): The language of the sender ('ca', 'es' or 'en')
			debug(:obj:`bool`): Boolean value indicating wether it has to output model's response

		This function returns the response from the agent using the actions
		defined in Fibot/NLP/core/actions.py
	"""
	def get_response(self, message, sender_id=UserMessage.DEFAULT_SENDER_ID, language = 'es', debug=True):
		confidence = self.nlu.get_intent(message, language)['confidence']
		if debug:
			print("\n\n\n#######  UN USUARIO HA DICHO: {} #######".format(colored(message, 'magenta')))
			print("\n\nINFORMACIÓN DE MENSAJE:")
			print("__________________________________________")
			print("El intérprete ha predecido la siguiente intención:")
			intent = self.nlu.get_intent(message, language)
			entities = self.nlu.get_entities(message, language)
			print('Intención: ' + colored(intent['name'], 'cyan', attrs=['bold']))
			print('Confianza: ' + colored(str(intent['confidence'])[:8], 'cyan'))
			if entities: print("\nY las siguientes entidades:")
			else: print("\nNo se han encontrado entidades en el mensaje")
			i = 0
			for entity in entities:
				print(colored('['+str(i)+']', 'red'))
				print('Tipo: ' + colored(entity['entity'], 'cyan', attrs=['bold']))
				print('Valor: ' + colored(entity['value'], 'cyan', attrs=['bold']))
				print('Confianza: ' + colored(str(entity['confidence'])[:8], 'cyan'))
				i+=1
		if confidence < 0.5:
			with open('./Data/error_responses.json', 'rb') as fp:
				messages = json.load(fp)['not_understand']
			return [{'recipient_id': sender_id, 'text': messages[language][randint(0,len(messages[language])-1)]}]
		if language == 'ca':
			return self.agent_ca.handle_message(message, sender_id=sender_id)
		elif language == 'es':
			return self.agent_es.handle_message(message, sender_id=sender_id)
		else:
			return self.agent_en.handle_message(message, sender_id=sender_id)
