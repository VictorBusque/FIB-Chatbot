#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
import requests
import os
import urllib
import json
import datetime


class API_raco(object):

	""" This object can interact with raco's api v2.0

		Attributes:
			client_id(:obj:`str`): the client_id for our api application
			client_secret(:obj:`str`): the client_secret for our api application
			base_url(:obj:`str`): the base url for checking content on the api_raco
			language(:obj:`dict`): allows to find information in 3 different languages
	"""
	def __init__(self):
		self.client_id = os.getenv('client_id')
		self.client_secret = os.getenv('client_secret')
		self.base_url = 'https://api.fib.upc.edu/v2/'


	"""
		Parameters:
			access_token(:obj:`str`): Access token of the user to get the schedule from
			language(:obj:`str`): Name of the language for the search

		This function returns:
			True if funcion with acronym or name parameters exist,
			False otherwise
	"""
	def get_schedule(self, access_token, language = 'es'):
		url = 'https://api.fib.upc.edu/v2/jo/classes/'
		headers = {"client_id": self.client_id,
				"Accept": "application/json",
				"Accept-Language": language,
				"Authorization": 'Bearer {}'.format(access_token)
		}
		response = requests.get(url, headers = headers)
		if response.status_code == 200:
			return response.json().get('results')


	"""
		Parameters:
			acronym(:obj:`str` or None): Acronym for the subject if any
			language(:obj:`str`): Name if the language for the search

		This function returns:
			True if funcion with acronym or name parameters exist,
			False otherwise
	"""
	def subject_exists(self, acronym, language = 'es'):
		url = self.base_url+"{}".format("assignatures/{}".format(acronym.upper()))
		headers = {"client_id": self.client_id,
				"Accept": "application/json",
				"Accept-Language": language
		}
		response = requests.get(url, headers=headers)
		return response.status_code == 200


	"""
		Parameters
			acces_token(:obj:`str`): Access token of the user to get subjects from
			language(:obj:`str`): Name if the language for the search

		This function returns:
			(:obj:`list`): Name of the subjects with acronym as the parameter (if it exists)
			(None): otherwise
	"""
	def get_subjects_user(self, access_token, language = 'es'):
		url = "https://api.fib.upc.edu/v2/jo/assignatures/"
		headers = {"client_id": self.client_id,
				"Accept": "application/json",
				"Accept-Language": language,
				"Authorization": 'Bearer {}'.format(access_token)
		}
		response = requests.get(url, headers = headers)
		if response.status_code == 200:
			response_json = response.json().get('results')
			for subject in response_json:
				yield subject['sigles']
		return []


	"""
		Parameters:
			acronym(:obj:`str` or None): Acronym for the subject if any
			access_token(:obj:`str`): Access token from user to check subject

		This function returns:
			True if funcion with acronym or name parameters is a subject the user is enrolled,
			False otherwise
	"""
	def user_enrolled_subject(self, acronym, access_token, language = 'es'):
		return acronym.upper() in self.get_subjects_user(access_token, language)


	"""
		Parameters
			acronym(:obj:`str` or None): Acronym for the subject
			language(:obj:`str`): Name if the language for the search

		This function returns:
			(:obj:`str`): Name of the subject with acronym as the parameter (if it exists)
			(None): otherwise
	"""
	def get_subject_name(self, acronym, language = 'es'):
		url = self.base_url+"{}".format("assignatures/{}".format(acronym.upper()))
		headers = {"client_id": self.client_id,
				"Accept": "application/json",
				"Accept-Language": language
		}
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.json()['nom']


	"""
		Parameters
			acces_token(:obj:`str`): Access token of the user to get subjects from
			language(:obj:`str`): Name if the language for the search

		This function returns:
			(:obj:`list`): List of exams of a user
	"""
	def get_exams_user(self, access_token, language = 'es'):
		subjects = list(self.get_subjects_user(access_token, language))
		for subject in subjects:
			exam = list(self.get_examens(subject, language))
			yield exam


	"""
		Parameters
			assig(:obj:`str`): Acronym for the subject
			language(:obj:`str`): Name if the language for the search

		This function returns:
			(:obj:`list`): List with the exams of subject assig
	"""
	def get_examens(self, acronym, language = 'es'):
		acronym = acronym.upper()
		actual_semester_url = 'https://api.fib.upc.edu/v2/quadrimestres/actual/'
		headers = {"client_id": self.client_id,
				"Accept": "application/json",
				"Accept-Language": language
		}
		response = requests.get(actual_semester_url, headers = headers)
		if response.status_code == 200:
			response_json = response.json()
			examens_url = response_json['examens']
			response = requests.get(examens_url, headers = headers)
			if response.status_code == 200:
				result = []
				response_json = response.json().get('results')
				for item in response_json:
					if item['assig'] == acronym: yield item


	"""
		Parameters
			acces_token(:obj:`str`): Access token of the user to get subjects from
			assig(:obj:`str` or None): Acronym of the assig if this is a specific search, o None if it is general
			language(:obj:`str`): Name if the language for the search

		This function returns:
			(:obj:`list`): List with the practical works open of subject assig (if any)
	"""
	def get_practiques(self, access_token, assig = None, language = 'es'):
		if assig: assig = assig.upper()
		practiques_url = 'https://api.fib.upc.edu/v2/jo/practiques/'
		headers = {"client_id": self.client_id,
				"Accept": "application/json",
				"Accept-Language": language,
				"Authorization": 'Bearer {}'.format(access_token)
		}
		response = requests.get(practiques_url, headers = headers)
		if response.status_code == 200:
			response_json = response.json().get('results')
			if not assig: return response_json
			else:
				result = []
				for item in response_json:
					if item['codi_asg'] == assig:
						result.appen(item)
				return result
		return []


	"""
		Parameters:
			access_token(:obj:`string`): the access token of the retriever

		This function returns:
			(:obj:`list`): list of avisos of the user with access_token
	"""
	def get_avisos(self, access_token, language = 'es'):
		params = {}
		headers = {"client_id": self.client_id,
				"Accept": "application/json",
				"Accept-Language": language,
				"Authorization": 'Bearer {}'.format(access_token)
		}
		url = "https://api.fib.upc.edu/v2/jo/avisos/"
		response = requests.get(url, headers = headers, params = params)
		if response.status_code == 200:
			response_json = response.json().get('results')
			return response_json


	"""
		Parameters:
			acronym(:obj:`str` or None): Acronym for the subject
			language(:obj:`str`): Name if the language for the search

		This function returns:
			(:obj:`list`): list of dictionaries with info like:
				[
					{
						"nom": "Jorge Castro Rabal",
						"email": "castro@cs.upc.edu",
						"is_responsable": false
					},
					...
				]
	"""
	def get_subject_teachers(self, acronym = None, language = 'es'):
		acronym = acronym.upper() #Should do a matching maybe, but not all subjects exist
		url_guia = "https://api.fib.upc.edu/v2/assignatures/{}/guia/".format(acronym)
		headers = {"client_id": self.client_id,
				"Accept": "application/json",
				"Accept-Language": language
		}
		response = requests.get(url_guia, headers=headers)
		if response.status_code == 200:
			teachers = response.json().get('professors')
			return teachers
		return []


	"""
		Parameters:
			query(:obj:`dict`): json format of the query (p.e. {'places-matricula': { 'field': 'assig', 'value': 'APC' } } )
			public(:obj:`bool`): Tells whether we are doing a public retrieval or nothing
			access_token(:obj:`string`): In case of a private retrieval, the access token of the retriever

		This function returns:
			None: If something goes wrong
			dict: result of the query
	"""
	def get_main(self, query, public = True, access_token = None, language = 'es'):
		params = {}
		headers = {"client_id": self.client_id,
				"Accept": "application/json",
				"Accept-Language": language
		}
		if not public:
			headers['Authorization'] = 'Bearer {}'.format(access_token)
		response = requests.get(self.base_url, headers = headers, params = params)
		if response.status_code == 200:
			if public:
				response_json = response.json().get('public')
			else:
				response_json = response.json().get('privat')
			for key in query.keys():
				query_url = response_json.get(key, [])
				print(query_url )
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
	def get_objects(self, url, query, headers, params = {}):
		response = requests.get(url, headers = headers, params = params)
		if response.status_code == 200:
			result = []
			field_name = query['field']
			field_value = query['value']
			response_json = response.json().get('results')
			for items in response_json:
				if items[field_name] == field_value:
					result.append(items)
			return result
		else:
			return None
