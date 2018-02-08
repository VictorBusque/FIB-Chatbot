#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
import os
import requests

#-- 3rd party imports --#
from telegram import ChatAction

#-- Local imports --#
from Fibot.chats import Chats
from Fibot.api_raco import API_raco
from Fibot.NLP.nlu import NLU_unit
from Fibot.NLP.nlg import NLG_unit


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
		state_machine(:obj:`dict`): Object that simplifies the state machine management
	"""
	def __init__(self, name = 'Fibot'):
		self.name = name
		self.bot_token = os.getenv('FibotTOKEN')
		self.chats = Chats()
		self.api_raco = API_raco()
		self.nlu = NLU_unit()
		self.nlg = NLG_unit()
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
		self.nlu.load()
		self.nlg.load()

	"""
		Sends an action to a chat (using ChatAction helper)
	"""
	def send_chat_action(self, chat_id, action = ChatAction.TYPING):
		params = {
			'chat_id': chat_id,
			'action': action
		}
		base_url = 'https://api.telegram.org/bot%s/sendChatAction'%self.bot_token
		response = requests.get(base_url, params = params)

	"""
		Sends a message to the chat with chat_id with content text
	"""
	def send_message(self, chat_id, text, typing = False, reply_to = None):
		if typing: self.send_chat_action(chat_id)
		params = {
			'chat_id': chat_id,
			'text': text
		}
		if reply_to != None: params['reply_to_message_id'] = reply_to
		base_url = 'https://api.telegram.org/bot%s/sendMessage'%self.bot_token
		response = requests.get(base_url, params = params)

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
		Returns the object query_answer
	"""
	def query_answer(self):
		return self.query_answer

	"""
		Returns the object state_machine
	"""
	def state_machine(self):
		return self.state_machine
