#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
import requests
import os
import urllib
import json
import datetime
#from threading import Thread
#from time import sleep


class Oauth(object):

	""" This object is the responsible for all the Oauth stuff in raco api

		Attributes:
			client_id(:obj:`str`): the client_id for our api application
			client_secret(:obj:`str`): the client_secret for our api application
			base_url(:obj:`str`): the base url for checking content on the api_raco
			redirect_uri(:obj:`str`): the uri to be redirected when authenticating
			authorisation_url(:obj:`str`): the url where a user can log in
			token_url(:obj:`str`): the url where we can request the tokens
	"""
	def __init__(self):
		self.client_id = os.getenv('client_id')
		self.client_secret = os.getenv('client_secret')
		self.base_url = 'https://api.fib.upc.edu/v2/'
		self.redirect_uri = 'https://localhost:5001'
		self.authorisation_url = 'https://api.fib.upc.edu/v2/o/authorize'
		self.token_url = 'https://api.fib.upc.edu/v2/o/token'

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
