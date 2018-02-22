#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
from os import getenv
import requests
import json
import re
from pprint import pprint
from time import time

#-- 3rd party imports --#
from telegram import ChatAction

#-- Local imports --#
from Fibot.chats import Chats
from Fibot.api.oauth import Oauth
from Fibot.NLP.nlg import NLG_unit, Query_answer_unit
from Fibot.NLP.language import Translator

class Fibot(object):

	""" This object contains information and methods to manage the bot, and interact with
		its users.

	Attributes:
		name (:obj:`str`): Unique identifier for the bot
		bot_token (:obj:`str`): Token to access the bot
		chats (:class:`Fibot.Chat`): Object that represents the chats
		oauth (:class:`Fibot.api.Oauth`): Object that does the oauth communication necessary
		nlg (:class:`Fibot.NLP.nlg.NLG_unit`): Object that interacts with non FIB messages
		qa (:class:`Fibot.NLP.nlg.Query_answer_unit`): Object that responds to FIB-related queries
		translator (:class:`Fibot.NLP.language.Translator`): Object that eases the translation of the messages
		messages (:obj:`dict`): Object that contains the Fibot configuration messages
		state_machine (:obj:`dict`): Object that simplifies the state machine management
	"""
	def __init__(self, name = 'Fibot'):
		self.name = name
		self.bot_token = getenv('FibotTOKEN')
		self.chats = Chats()
		self.oauth = Oauth()
		self.nlg = NLG_unit()
		self.qa = Query_answer_unit()
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
		self.nlg.load()
		print("NLG model loaded")
		self.qa.load(train=False)
		print("Query answering model loaded")
		with open('./Data/messages.json', 'r') as fp:
			self.messages = json.load(fp)
		print("Preset messages loaded")

	"""
		Parameters:
			chat_id (:obj:`int`): chat id of the user to send the message to
			action (:obj:`str`): defines the action to send the user (default is typing)

		This function sends an action to the chat with chat_id (using ChatAction helper)
	"""
	def send_chat_action(self, chat_id, action = ChatAction.TYPING):
		params = {
			'chat_id': chat_id,
			'action': action
		}
		base_url = 'https://api.telegram.org/bot{}/sendChatAction'.format(self.bot_token)
		response = requests.get(base_url, params = params)

	"""
		Parameters:
			chat_id (:obj:`int`): chat id of the user to send the message to
			message (:obj:`str`): content of the message to be sent
			typing (:obj:`bool`): value that defines whether to send typing action or not
			reply_to (:obj:`int` or None): If defined, it is the message_id of the message
				that will be replied to, else no message will be replied.

		This function sends a message to the chat with chat_id with content text,
		and depending on the rest of the parameters i might do extra functionality.
	"""
	def send_message(self, chat_id, message, typing = False, reply_to = None):
		ini = time()
		if isinstance(message, list):
			for item in message:
				self.send_message(chat_id, item, typing, reply_to)
		else:
			if typing: self.send_chat_action(chat_id)
			print("chat action sent in {}".format( (time()-ini) ))
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
			print("message sent in {}".format( (time()-ini) ))


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
		self.send_message(chat_id, message, typing=True)

	"""
		Parameters:
			chat_id (:obj:`str`): chat_id of the user that sent the messages
			message (:obj:`str`): text the user sent
			message_id (:obj:`int`): message_id of the message to reply to


		This function receives a message from a user and decides which mechanism is responsible
		for responding the message.
	"""
	def process_income_message(self, chat_id, message, message_id = None):
		print("Processing income message...")
		user_language = self.chats.get_chat(chat_id)['language']
		if user_language != 'English':
			message = self.translator.translate(message , to = 'English', _from = user_language)
		ini = time()
		response = self.qa.get_response(message, sender_id = chat_id)
		print("Getting response time is {}".format( (time()-ini) ))
		print(response)
		if message_id:
			self.send_message(chat_id, response, typing=True, reply_to = message_id)
		else: self.send_message(chat_id, response, typing=True)
