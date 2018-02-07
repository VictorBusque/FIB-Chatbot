#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import requests.auth
import urllib
import json
import datetime
from threading import Thread
from time import sleep

class API_raco(object):

	""" This object can interact with raco's api v2.0

		Attributes:
			client_id(:obj:`str`): the client_id for our api application
			client_secret(:obj:`str`): the client_secret for our api application
			base_url(:obj:`str`): the base url for checking content on the api_raco
			redirect_uri(:obj:`str`): the uri to be redirected when authenticating
			authorisation_url(:obj:`str`): the url where a user can log in
			token_url(:obj:`str`): the url where we can request the tokens
			language(:obj:`dict`): allows to find information in 3 different languages
	"""
	def __init__(self):
		self.client_id = 'QEcwkDLH8yO9x9g4vpSxIcS6FhUUJGRSZ71rQEoZ'#os.getenv('client_id')
		self.client_secret = 'TXlgFLpju2usHzhWi1vqmpQqsgdz1MYausyhfCHj6VvzdAorE5ZRdvxvElPt3jibxACvi59F7YtyYVylNqdtnoTGuDM3BYgeBPmYjCqaymOmme3R4bdq1JCdRAILZkTb'#os.getenv('client_secret')
		self.base_url = 'https://api.fib.upc.edu/v2/'
		self.redirect_uri = 'https://localhost:5001'
		self.authorisation_url = 'https://api.fib.upc.edu/v2/o/authorize'
		self.token_url = 'https://api.fib.upc.edu/v2/o/token'
		self.language =  {'Catalan': 'ca', 'Spanish': 'es', 'English': 'en'}

	"""
		Returns the url where a student can log in
	"""
	def get_autho_full_page(self):
		params = {"client_id": self.client_id,
				  "redirect_uri": self.redirect_uri,
				  "response_type": "code",
				  "scope": "read"}
		return self.authorisation_url + '?' + urllib.parse.urlencode(params)

	"""
		Parameters:
			auth_code(:obj:`str`): the code for the first part of the oauth2.0 protocol given by the users

		This function does the 2nd part of the oauth2.0 protocol, and returns:
			None: if something went wrong
			Dict{
				access_token: value,
				refresh_token: value,
				expire_time_end: value,
				logged: value
			}
			if the authorisation goes well.
	"""
	def authenticate(self, auth_code):
		payload = {"grant_type": "authorization_code",
				"code": auth_code,
				"redirect_uri": self.redirect_uri,
				"client_id": self.client_id,
				"client_secret": self.client_secret
		}
		headers = {u'content-type': u'application/x-www-form-urlencoded'}
		response = requests.post(self.token_url, data = payload, headers = headers)
		if response.status_code == 200:
			response_json = response.json()
			end_time = datetime.datetime.now() + datetime.timedelta(hours=10)
			expire_time_end = {'day': end_time.day,
							'month': end_time.month,
							'year': end_time.year,
							'hour': end_time.hour,
							'minute': end_time.minute,
							'second': end_time.second}
			return {'access_token': response_json['access_token'],
				'refresh_token': response_json['refresh_token'],
				'expire_time_end': expire_time_end,
				'logged': True}
		else:
			return None

	"""
		Parameters:
			refresh_token(:obj:`str`): The refresh token to the user to refresh its access_token

		This function returns:
			None: if the refresh process went wrong
			Dict{
					access_token: value,
					refresh_token: value,
					expire_time_end: value,
					logged: value
				}
				if the refreshment goes well.
	"""
	def refresh_token(self, refresh_token):
		payload = {"grant_type": "refresh_token",
				"refresh_token": refresh_token,
				"client_id": self.client_id,
				"client_secret": self.client_secret
		}
		headers = {u'content-type': u'application/x-www-form-urlencoded'}
		response = requests.post(self.token_url, data = payload, headers = headers)
		if response.status_code == 200:
			response_json = response.json()
			end_time = datetime.datetime.now() + datetime.timedelta(hours=10)
			expire_time_end = {'day': end_time.day,
							'month': end_time.month,
							'year': end_time.year,
							'hour': end_time.hour,
							'minute': end_time.minute,
							'second': end_time.second}
			return {'access_token': response_json['access_token'],
				'refresh_token': response_json['refresh_token'],
				'expire_time_end': expire_time_end,
				'logged': True}
		else:
			return None

	"""
		Parameters:
			query(:obj:`dict`): json format of the query (p.e. {'places-matricula': { 'field': 'assig', 'value': 'APC' } } )
			public(:obj:`bool`): Tells whether we are doing a public retrieval or nothing
			access_token(:obj:`string`): In case of a private retrieval, the access token of the retriever

		This function returns:
			None: If something goes wrong
			dict: result of the query
	"""
	def get_main(self, query, public = True, access_token = None):
		params = {}
		headers = {"client_id": self.client_id,
				"Accept": "application/json",
				"Accept-Language": self.language['Spanish']
		}
		if not public:
			#if token_is_deprecated(chat_id):
				#refresh_token(chat_id)
			headers['Authorization'] = 'Bearer %s'%access_token
		response = requests.get(self.base_url, headers = headers, params = params)
		if response.status_code == 200:
			if public:
				response_json = response.json().get('public')
			else:
				response_json = response.json().get('privat')
			for key in query.keys():
				query_url = response_json.get(key, [])
				if query_url:
					return self.get_objects(query_url, query[key], headers)
				else:
					return None
		else:
			return None

	"""
		Parameters:
			url(:obj:'str'): url of the api for the query
			query(:obj:`dict`): query to look for
			headers(:obj:`dict`): headers to do the request
			params(:obj:`dict`): parameters to do the requests

		This function returns:
			None: if the query or the request goes wrong
			dict: result of the query
	"""
	def get_objects(url, query, headers, params = {}):
		response = requests.get(url, headers = headers, params = params)
		if response.status_code == 200:
			field_name = query['field']
			field_value = query['value']
			response_json = response.json().get('results')
			for items in response_json:
				if items[field_name] == field_value:
					yield items
		else:
			yield None








"""
threads = []


def thread_func(seconds, chat_id):
	sleep(seconds)
	refresh_token(chat_id)

def schedule_refreshment(chat_id):
	expire_time_end = db_module.get_chat(chat_id)['expire_time_end']
	expire_time_end = datetime.datetime(expire_time_end['year'],
										expire_time_end['month'],
										expire_time_end['day'],
										expire_time_end['hour'],
										expire_time_end['minute'],
										expire_time_end['second'])
	actual_time = datetime.datetime.now()
	delay = (expire_time_end-actual_time).total_seconds()
	print("delay is %s"%str(delay))
	thread = Thread(target = thread_func, args = [delay, chat_id])
	thread.start()
	threads.append(thread)
"""
