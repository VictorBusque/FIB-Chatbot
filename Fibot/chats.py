#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
import json
import os
from datetime import datetime
from pprint import pprint


class Chats(object):

	""" This object contains the necessary information of the chats

	Attributes:
		chats(:obj:`dict`): storage of the necessary information

		the format is the following:
		{
		chat_id: {
			'name': (:obj:`str`) the name of the user with chat_id key),
			'language': (:obj:`str`) the name of the language ['Spanish', 'Catalan', 'English']
			'access_token': (:obj:`str` or None) the access_token of the user with chat_id key,
			'refresh_token': (:obj:`str` or None) the refresh_token of the user with chat_id key,
			'current_state': (:obj:`str`) the state (in the Fibot state definition) the user with chat_id key is on,
			'expire_time_end': (:obj:`dict`) time when the access_token expires,
			'logged': (:obj:`bool`) specifies if the user with chat_id key is logged or not,
			'training': (:obj:`bool`) specifies if the user with chat_id key is in training mode,
			'notifications': (:obj:`bool`) specifies if the user with chat_id has notifications active currently
			}
		}
	"""
	def __init__(self):
		self.chats = {}

	"""
		Returns the data from persistence of user with chat_id
	"""
	def get_chat_lite(self, chat_id):
		with open('./Data/chat_status.json', 'r') as fp:
			return json.load(fp)[str(chat_id)]

	"""
		Loads the data from persistence (if any)
	"""
	def load(self):
		try:
			with open('./Data/chat_status.json', 'r') as fp:
				self.chats = json.load(fp)
		except:
			print("There is no db file")
			with open('./Data/chat_status.json', 'w') as fp:
				json.dump({}, fp, indent = 2)
		pprint(self.chats)

	"""
		Parameters:
			chat_id (:obj:`int`): chat_id of the chat

		This function returns:
			True: if chat_id exists on chats dictionary
			False: otherwise
	"""
	def user_has_data(self, chat_id):
		return str(chat_id) in self.chats.keys()

	"""
		Parameters:
			chat_id (:obj:`int`): chat_id of the chat
			data (:obj:`dict`): dict with new data for user with chat_id
			compulsory (:obj:`bool`): boolean value indicating if function has to replace information
			full_data (:obj:`bool`): boolean value indicating if data contains the whole data or just a part

		This function changes the whole internal state of the chat_id depending on the compulsory parameter
		and dumps into persistence
	"""
	def update_chat(self, chat_id, data, compulsory = True, full_data = True):
		if compulsory:
			if full_data:
				self.chats[str(chat_id)] = data
				self.dump_data()
			else:
				for field in data.keys():
					self.chats[str(chat_id)][field] = data[field]
				self.dump_data()

	"""
		Parameters:
			chat_id (:obj:`int`): chat_id of the chat
			field (:obj:`str`): indicates the field to be updated
			value (:obj:`str` or :obj:`dict` or :obj:`bool` or None): the updated value
			overwrite (:obj:`bool`): boolean value indicating if the data has to be dumped into persistence

		This function updates  the old value of the field passed as parameter to the new one (the parameter) of the chat of chat_id.
		Also, depending on the overwrite parameter, it will dump the data into persistence too.
	"""
	def update_info(self, chat_id, field, value, overwrite = False):
		self.chats[str(chat_id)][field] = value
		if overwrite:
			self.dump_data()

	"""
		This function updates persistence with the contents of the dict chats.
	"""
	def dump_data(self):
		print("Dumping data <--------------")
		print(self.chats)
		os.remove('./Data/chat_status.json')
		with open('./Data/chat_status.json', 'w') as fp:
			json.dump(self.chats, fp, indent = 2)

	"""
		Parameters:
			chat_id(:obj:`str`): chat_id of the chat

		This function returns:
			None: if there is no chat information of the chat_id
			dict: if there is.
	"""
	def get_chat(self, chat_id):
		if self.user_has_data(chat_id):
			return self.chats[str(chat_id)]
		else:
			return None

	"""
		Parameters:
			chat_id(:obj:`str`): chat_id of the chat

		This function returns:
			True: if the access_token from user with chat_id has expired
			False: otherwise
	"""
	def token_has_expired(self, chat_id):
		expiration_time = self.chats[str(chat_id)]['expire_time_end']
		if not expiration_time: return True
		now = datetime.now()
		expiration_time = datetime(
			expiration_time['year'],
			expiration_time['month'],
			expiration_time['day'],
			expiration_time['hour'],
			expiration_time['minute'],
			expiration_time['second']
		)
		return now > expiration_time
