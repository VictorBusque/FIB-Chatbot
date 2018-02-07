from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement

from telegram import ChatAction

import os
import requests

class NLG_unit(object):

	""" This object contains tools to answer in natural language any message

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
		bot_token = '464845676:AAG4XGgjfUC_pkuAcJHRDYebQvuTZgx4jUo'#os.getenv('FibotTOKEN')
		base_url = 'https://api.telegram.org/bot%s/sendMessage'%bot_token
		response = requests.get(base_url, params = params)

	"""
		Parameters:
			chat_id (:obj:`str`): chat_id of the person to process the answer for
			action (:obj:`str`): action to send of the messages

		This function allows nlg class to send messages for the training duties
	"""
	def send_chat_action(self, chat_id, action = ChatAction.TYPING):
		params = {
			'chat_id': chat_id,
			'action': action
		}
		bot_token = '464845676:AAG4XGgjfUC_pkuAcJHRDYebQvuTZgx4jUo'#os.getenv('FibotTOKEN')
		base_url = 'https://api.telegram.org/bot%s/sendChatAction'%bot_token
		response = requests.get(base_url, params = params)
