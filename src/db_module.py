#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import os
from pprint import pprint


'''
user_status = { chat_id: {
					'name': username, 
					'access_token': None/at, 
					'refresh_token': None/rt, 
					'current_state': state, 
					'expire_time_ini': None/eti, 
					'expire_time_end': None/ete,
					'logged': true/false
					}  
				}
'''

chat_status = {}

'''
class chat:
	def __init__(self, chat_id, name, access_token = None, refresh_token = None, 
		current_state = None, expire_time_ini = None, expire_time_end = None, logged = None):

		self.chat_id = str(chat_id)
		self.data = {
					'name': name, 
					'access_token': access_token, 
					'refresh_token': refresh_token, 
					'current_state': current_state, 
					'expire_time_ini': expire_time_ini, 
					'expire_time_end': expire_time_end,
					'logged': logged
		}
'''


def user_has_data(chat_id):
	global chat_status
	return str(chat_id) in chat_status.keys()


def load_data():
	global chat_status
	try:
		with open('./Data/chat_status.json', 'r') as fp:
			chat_status = json.load(fp)
		print(chat_status)
		print("----------------")
	except:
		print("There is no db file")
		with open('./Data/chat_status.json', 'w') as fp:
			json.dump({}, fp, indent = 2)


def update_chat(chat_id, data, compulsory = True):
	global chat_status
	if compulsory:
		chat_status[str(chat_id)] = data
		dump_data()
	else:
		print ("Starting, no need to rewrite")


def update_info(chat_id, field, value, overwrite = False):
	global chat_status
	chat_status[str(chat_id)][field] = value
	if overwrite:
		dump_data()


def dump_data():
	global chat_status
	print(chat_status)
	print("----------------")
	os.remove('./Data/chat_status.json')
	with open('./Data/chat_status.json', 'w') as fp:
		json.dump(chat_status, fp, indent = 2)


def get_chat(chat_id):
	global chat_status
	return chat_status[str(chat_id)]