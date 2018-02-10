#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
import os
import requests
import json
import re
from pprint import pprint

#-- 3rd party imports --#
from telegram import ChatAction

#-- Local imports --#
from Fibot.chats import Chats
from Fibot.api_raco import API_raco
from Fibot.NLP.nlu import NLU_unit
from Fibot.NLP.nlg import NLG_unit
from Fibot.NLP.language import Translator

class Fibot(object):

	""" This object contains information and methods to manage the bot, and interact with
		its users.

	Attributes:
		name(:obj:`str`): Unique identifier for the bot
		bot_token(:obj:`str`): Token to access the bot
		chats(:class:`Fibot.Chat`): Object that represents the chats
		api_raco(:class:`Fibot.API_raco`): Object that interacts with Raco's api
		nlu(:class:`Fibot.NLP.nlu.NLU_unit`): Object that interprets querys
		nlg(:class:`Fibot.NLP.nlg.NLG_unit`): Object that interacts with non FIB messages
		~ query_answer(:class:`Fibot.NLP.nlg.Query_answer_unit`): Object that responds to FIB-related queries
		translator(:class:`Fibot.NLP.language.Translator`): Object that eases the translation of the messages
		messages(:obj:`dict`): Object that contains the Fibot configuration messages
		state_machine(:obj:`dict`): Object that simplifies the state machine management
	"""
	def __init__(self, name = 'Fibot'):
		self.name = name
		self.bot_token = os.getenv('FibotTOKEN')
		self.chats = Chats()
		self.api_raco = API_raco()
		self.nlu = NLU_unit()
		self.nlg = NLG_unit()
		self.translator = Translator()
		self.messages = {}
		self.state_machine = {
			'MessageHandler': '0',
			'Authorise': '1',
			'Wait_authorisation': '2',
			'Erase_user': '3',
			'Push_notification': '4',
		}

	"""
		Loads the following components:
			chats: Loads the chats information from persistence
			nlu: Loads the trained model
			nlg: Loads the trained model
	"""
	def load_components(self):
		self.chats.load()
		print("Chats loaded")
		self.nlu.load()
		print("NLU model loaded")
		self.nlg.load()
		print("NLG model loaded")
		with open('./Data/messages.json', 'r') as fp:
			self.messages = json.load(fp)

	"""
		Sends an action to a chat (using ChatAction helper)
	"""
	def send_chat_action(self, chat_id, action = ChatAction.TYPING):
		params = {
			'chat_id': chat_id,
			'action': action
		}
		base_url = 'https://api.telegram.org/bot{}/sendChatAction'.format(self.bot_token)
		response = requests.get(base_url, params = params)

	"""
		Sends a message to the chat with chat_id with content text
	"""
	def send_message(self, chat_id, message, typing = False, reply_to = None):
		if typing: self.send_chat_action(chat_id)
		user_language = self.chats.get_chat(chat_id)['language']
		if user_language != 'English':
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
			if urls: message = message.replace(urls[0],"{}")
			message = self.translator.translate(message , to = user_language)
			if urls: message = message.format(urls[0])
		params = {
			'chat_id': chat_id,
			'text': message
		}
		if reply_to: params['reply_to_message_id'] = reply_to
		base_url = 'https://api.telegram.org/bot{}/sendMessage'.format(self.bot_token)
		response = requests.get(base_url, params = params)

	"""
		Parameters:
			chat_id (:obj:`str`): chat_id of the user to send the message to
			preset (:obj:`str`): the preset of the message to send
			param (:obj:`str` or None): the parameter of the messages

		This function sends a preset message to the user with user id.
		See /Data/messages.json to see the preset messages.
	"""
	def send_preset_message(self, chat_id, preset, param = None):
		print("sending {}".format(preset))
		if param:
			message = self.messages[preset].format(param)
		else:
			message = self.messages[preset]
		message = self.translator.translate(message, to = 'English', _from = 'Spanish')
		self.send_message(chat_id, message, typing=True)

	"""
		Parameters:
			chat_id (:obj:`str`): chat_id of the user that sent the messages
			message (:obj:`str`): text the user sent

		This function receives a message from a user and decides which mechanism is responsible
		for responding the message.
	"""
	def process_income_message(self, chat_id, message, message_id = None, debug = False):
		print("Processing income message...")
		if debug: #Translation in the future should be before this
			pprint(self.nlu.get_intent(message))
			pprint(self.nlu.get_entities(message))
			self.send_message(chat_id, "The intent is: {}".format(self.nlu.get_intent(message)['name']))
			for entity in self.nlu.get_entities(message):
				self.send_message(chat_id, "One entity is: {}: {}".format(entity['entity'], entity['value']))

		user_language = self.chats.get_chat(chat_id)['language']
		if user_language != 'English':
			message = self.translator.translate(message , to = 'English', _from = user_language)
		response = self.nlg.get_response(message)
		if message_id: self.send_message(chat_id, response, typing=True, reply_to = message_id)
		else: self.send_message(chat_id, response, typing=True)


	"""
		Returns the bot's name
	"""
	def name(self):
		return self.name

	"""
		Returns the bot's token
	"""
	def bot_token(self):
		return self.bot_token

	"""
		Returns the object chats
	"""
	def chats(self):
		return self.chats

	"""
		Returns the object api_raco
	"""
	def api_raco(self):
		return self.api_raco

	"""
		Returns the object nlu
	"""
	def nlu(self):
		return self.nlu

	"""
		Returns the object nlg
	"""
	def nlg(self):
		return self.nlg

	"""
		Returns the object state_machine
	"""
	def state_machine(self):
		return self.state_machine
