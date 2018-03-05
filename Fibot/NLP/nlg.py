#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
import os
import requests
from pprint import pprint

#-- 3rd party imports --#
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.channels import UserMessage
from rasa_core.channels.console import ConsoleInputChannel
from telegram import ChatAction

#-- local imports --#
from Fibot.NLP.nlu import NLU_unit


class NLG_unit(object):

	""" This object contains tools to answer in natural language any message non-Fib related

	Attributes:
		chatterbot_bot(:class:`chatterbot.ChatBot`): chatterbot bot to process the non-fib-Related questions
		train_queue(:obj:`dict`): dictionary that act as a queue of training concepts
		conversation_id(:obj:`int` or None): Identifier that keeps track of the diferent amounts of conversations learnt
	"""
	def __init__(self):
		self.chatterbot_bot = ChatBot(
			"Fibot",
			storage_adapter="chatterbot.storage.SQLStorageAdapter",
		)
		self.train_queue = {}
		self.conversation_id = None

	"""
		This function load the learnt model for chatterbot
	"""
	def load(self):
		self.conversation_id = self.chatterbot_bot.storage.create_conversation()

	"""
		Parameters:
			chat_id (:obj:`str`): chat_id of the person to get feedback from
			correct (:obj:`bool`): tells whether the prediction was correct_statement
			correct_statement (:obj:`str` or None): Correction if there is

		This function enables the chatterbot bot to learn if he predicted good and allows
		him to learn new responses.
	"""
	def give_feedback(self, chat_id, correct = True, correct_statement = None):
		if not correct:
			message = self.train_queue[chat_id]['message']
			correct_statement = Statement(correct_statement)
			self.chatterbot_bot.learn_response(correct_statement, message)
			self.chatterbot_bot.storage.add_to_conversation(self.conversation_id, message, correct_statement)
			self.send_message(chat_id, "Aprendido!. Mándame más si quieres, o desactívame usando /train_off")
		else:
			self.send_message(chat_id, "Bien. Mándame más si quieres, o desactívame usando /train_off")

	"""
		Parameters:
			chat_id (:obj:`str`): chat_id of the person to process the answer for
			message (:obj:`str`): message the user introduced to be processed

		This function makes the bot predict the following message, and
		asks for checks.
	"""
	def process_answer_training(self, chat_id, message):
		print("Query de %s con mensaje %s"%(chat_id, message))
		self.send_chat_action(chat_id)
		input_statement = Statement(message)
		statement, response = self.chatterbot_bot.generate_response(input_statement, self.conversation_id)
		self.send_message(chat_id,'Es "{}" una respuesta coherente a "{}"? (Sí/No)'.format(response, message))
		self.train_queue[chat_id] = {
			'message': input_statement,
			'response': response
		}

	"""
		Parameters:
			message (:obj:`str`): message the user introduced to be processed
			debug (:obj:`bool`): indicates the level of verbosity

		This function returns the predicted responses for message
	"""
	def get_response(self, message, debug = False):
		input_statement = Statement(message)
		_, response = self.chatterbot_bot.generate_response(input_statement, self.conversation_id)
		if debug:
			return "%s, confidence = %d"%(response['text'], response['confidence'])
		else:
			return str(response)

	"""
		Parameters:
			chat_id (:obj:`str`): chat_id of the person to process the answer for
			message (:obj:`str`): content of the messages

		This function allows nlg class to send messages for the training duties
	"""
	def send_message(self, chat_id, message):
		params = {
			'chat_id': chat_id,
			'text': message
		}
		bot_token = os.getenv('FibotTOKEN')
		base_url = 'https://api.telegram.org/bot%s/sendMessage'%bot_token
		response = requests.get(base_url, params = params)

	"""
		Parameters:
			chat_id (:obj:`str`): chat_id of the person to process the answer for
			action (:obj:`str`): action to send of the messages

		This function allows nlg class to send chat_action for the training duties
	"""
	def send_chat_action(self, chat_id, action = ChatAction.TYPING):
		params = {
			'chat_id': chat_id,
			'action': action
		}
		bot_token = os.getenv('FibotTOKEN')
		base_url = 'https://api.telegram.org/bot%s/sendChatAction'%bot_token
		response = requests.get(base_url, params = params)


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
