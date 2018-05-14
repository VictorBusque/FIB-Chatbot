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
	def get_schedule(self, access_token, language = 'es', acronym = None):
		url = 'https://api.fib.upc.edu/v2/jo/classes/'
		headers = {"client_id": self.client_id,
				"Accept": "application/json",
				"Accept-Language": language,
				"Authorization": 'Bearer {}'.format(access_token)
		}
		response = requests.get(url, headers = headers)
		if response.status_code == 200:
			results = response.json().get('results')
			if not acronym:
				return results
			else:
				acronym = acronym.upper()
				output = []
				for lecture in results:
					if lecture['codi_assig'] == acronym:
						output.append(lecture)
				return  output


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
			for subject in response_json: yield subject['sigles']
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
	def get_practiques(self, access_token, language = 'es'):
		practiques_url = 'https://api.fib.upc.edu/v2/jo/practiques/'
		headers = {"client_id": self.client_id,
				"Accept": "application/json",
				"Accept-Language": language,
				"Authorization": 'Bearer {}'.format(access_token)
		}
		response = requests.get(practiques_url, headers = headers)
		if response.status_code == 200:
			return response.json().get('results')


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
		Parameters
			assig(:obj:`str` or None): Acronym of the assig if this is a specific search, o None if it is general
			language(:obj:`str`): Name of the language for the search

		This function returns:
			(:obj:`list`): List with the free spots for the subject with acronym
	"""
	def get_free_spots(self, acronym, language = 'es'):
		acronym = acronym.upper()
		url_places = 'https://api.fib.upc.edu/v2/assignatures/places/'
		headers = {"client_id": self.client_id,
				"Accept": "application/json",
				"Accept-Language": language
		}
		response = requests.get(url_places, headers=headers)
		if response.status_code == 200:
			places = response.json().get('results')
			for subject in places:
				if subject['assig'] == acronym: yield subject
