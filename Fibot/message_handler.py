#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
from os import getenv
import requests
import json
from pprint import pprint
from time import time

#-- 3rd party imports --#
from telegram import ChatAction


class Message_handler(object):


    def __init__(self, chats):
        self.bot_token = getenv('FibotTOKEN')
        self.chats = chats


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
    def send_message(self, chat_id, message, typing = False, reply_to = None, parse_mode = 'Markdown'):
    	ini = time()
    	if isinstance(message, list):
    		for item in message:
    			self.send_message(chat_id, item, typing, reply_to)
    	else:
            if typing: self.send_chat_action(chat_id)
            print("chat action sent in {}".format( (time()-ini) ))
            user_language = self.chats.get_chat(chat_id)['language']
            params = {
            	'chat_id': chat_id,
            	'text': message
            }
            if parse_mode: params['parse_mode'] = parse_mode
            if reply_to: params['reply_to_message_id'] = reply_to
            print("This are the params of the message: {}".format(params))
            base_url = 'https://api.telegram.org/bot{}/sendMessage'.format(self.bot_token)
            response = requests.get(base_url, params = params)
            print("message sent in {}".format( (time()-ini) ))
