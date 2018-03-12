#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
import os
import requests
from pprint import pprint

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
		domain_path(:obj:`str`): String indicating where the domain yml file is
		agent(:class:`rasa_core.agent.Agent`): Agent capable of handling any incoming messages
	"""
	def __init__(self):
		self.nlu = NLU_unit()
		self.training_data_file = './Fibot/NLP/core/stories.md'
		self.domain_path = './Fibot/NLP/core/domain.yml'
		self.model_path = './models/dialogue'
		self.agent =  Agent(self.domain_path,
			                  policies=[MemoizationPolicy(), KerasPolicy()])

	"""
		Parameters:
			train (:obj:`bool`): Specifies if the agent has to be trained
		This function loads the model into the agent, and trains if necessary
	"""
	def load(self, train=False):
		self.nlu.load(train)
		if train: self.train()
		self.agent = Agent.load(self.model_path,
				interpreter = self.nlu.interpreter)

	"""
		Parameters:
			augmentation_factor (:obj:`int`): augmentation factor for the training
			max_history (:obj:`int`): max_history factor for the training
			epochs (:obj:`int`): epochs (steps) for the training
			batch_size (:obj:`int`): batch_size for the training
			validation_split (:obj:`int`): validation_split factor for the error calculation

		This function trains the agent and saves the model in the dialog's model path
	"""
	def train(self, augmentation_factor=50, max_history=2, epochs=500, batch_size=50, validation_split=0.2):
		self.agent.train(self.training_data_file,
			augmentation_factor=augmentation_factor,
			max_history=max_history,
			epochs=epochs,
		 	batch_size=batch_size,
			validation_split=validation_split
		)
		self.agent.persist(self.model_path)

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
		self.agent.train_online(self.training_data_file,
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

		This function returns the response from the agent using the actions
		defined in Fibot/NLP/core/actions.py
	"""
	def get_response(self, message, sender_id=UserMessage.DEFAULT_SENDER_ID, debug=True):
		if debug:
			print("Interpreter understood the following intent:")
			pprint(self.nlu.get_intent(message))
			print("And the following entities:")
			pprint(self.nlu.get_entities(message))
		return self.agent.handle_message(message, sender_id=sender_id)
