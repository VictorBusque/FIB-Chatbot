#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import requests.auth
import urllib
import json
import datetime
import db_module


CLIENT_ID = 'QEcwkDLH8yO9x9g4vpSxIcS6FhUUJGRSZ71rQEoZ'
CLIENT_SECRET = 'TXlgFLpju2usHzhWi1vqmpQqsgdz1MYausyhfCHj6VvzdAorE5ZRdvxvElPt3jibxACvi59F7YtyYVylNqdtnoTGuDM3BYgeBPmYjCqaymOmme3R4bdq1JCdRAILZkTb'
REDIRECT_URI = 'https://localhost:5001' 

URL_BASE = 'https://api.fib.upc.edu/v2/'

AUTHORIZATION_PAGE = 'https://api.fib.upc.edu/v2/o/authorize'
TOKEN_PAGE = 'https://api.fib.upc.edu/v2/o/token'

LANGUAGE = {'Catalan': 'ca', 'Spanish': 'es', 'English': 'en'}


def get_autho_full_page():
	global CLIENT_ID, AUTHORIZATION_PAGE
	params = {"client_id": CLIENT_ID,
		   	  "redirect_uri": REDIRECT_URI,
			  "response_type": "code",
			  "scope": "read"}
	return AUTHORIZATION_PAGE + '?' + urllib.parse.urlencode(params)


def process_oauth(code, chat_id):
	global CLIENT_ID, CLIENT_SECRET, TOKEN_PAGE, REDIRECT_URI
	AUTH_CODE = code
	print("Authorizing user")
	payload = {"grant_type": "authorization_code",
			"code": code,
	   	  	"redirect_uri": REDIRECT_URI,
			"client_id": CLIENT_ID,
			"client_secret": CLIENT_SECRET
	}
	headers = {u'content-type': u'application/x-www-form-urlencoded'}
	response = requests.post(TOKEN_PAGE, data = payload, headers = headers)
	if response.status_code == 200:
		response_json = response.json()
		db_module.update_info(chat_id, 'access_token' , response_json['access_token'])
		db_module.update_info(chat_id, 'refresh_token', response_json['refresh_token'])
		TOKEN_EXPIRE_TIME = response_json['expires_in']
		ini_time = datetime.datetime.now()
		expire_time_ini = {'day': ini_time.day,
						'month': ini_time.month,
						'year': ini_time.year,
						'hour': ini_time.hour,
						'minute': ini_time.minute,
						'second': ini_time.second}
		db_module.update_info(chat_id, 'expire_time_ini' , expire_time_ini)
		end_time = datetime.datetime.now() + datetime.timedelta(hours=10)
		expire_time_end = {'day': end_time.day,
						'month': end_time.month,
						'year': end_time.year,
						'hour': end_time.hour,
						'minute': end_time.minute,
						'second': end_time.second}
		db_module.update_info(chat_id, 'expire_time_end' , expire_time_end)
		db_module.update_info(chat_id, 'logged', True, overwrite = True)
		print("Authorization correct, token expires %s"%expire_time_end)
		return True
	else:
		return False


def refresh_token(chat_id):
	global CLIENT_ID, CLIENT_SECRET, TOKEN_PAGE, REDIRECT_URI
	print("Refreshing token")
	REFRESH_TOKEN = db_module.get_chat(chat_id)['refresh_token']
	payload = {"grant_type": "refresh_token",
			"refresh_token": REFRESH_TOKEN,
			"client_id": CLIENT_ID,
			"client_secret": CLIENT_SECRET
	}
	headers = {u'content-type': u'application/x-www-form-urlencoded'}
	response = requests.post(TOKEN_PAGE, data = payload, headers = headers)
	print (response.status_code)
	if response.status_code == 200:
		response_json = response.json()
		db_module.update_info(chat_id, 'access_token' , response_json['access_token'])
		db_module.update_info(chat_id, 'refresh_token', response_json['refresh_token'])
		TOKEN_EXPIRE_TIME = response_json['expires_in']
		ini_time = datetime.datetime.now()
		expire_time_ini = {'day': ini_time.day,
						'month': ini_time.month,
						'year': ini_time.year,
						'hour': ini_time.hour,
						'minute': ini_time.minute,
						'second': ini_time.second}
		db_module.update_info(chat_id, 'expire_time_ini' , expire_time_ini)
		end_time = datetime.datetime.now() + datetime.timedelta(hours=10)
		expire_time_end = {'day': end_time.day,
						'month': end_time.month,
						'year': end_time.year,
						'hour': end_time.hour,
						'minute': end_time.minute,
						'second': end_time.second}
		db_module.update_info(chat_id, 'expire_time_end' , expire_time_end, overwrite = True)

		print("Authorization correct, token expires %s"%expire_time_end)
		return True
	else:
		return False

#query: {'places-matricula': { 'field': 'assig', 'value': 'APC' } }
def get_main(query, public = True):
	params = {}
	headers = {"client_id": CLIENT_ID,
			"Accept": "application/json",
			"Accept-Language": LANGUAGE['Spanish']
	}
	if not public:
		headers['Authorization'] = 'Bearer %s'%OAUTH_TOKEN
	response = requests.get(URL_BASE, headers = headers, params = params)
	if response.status_code == 200:
		print("Got a query: %s"%str(query))
		if public:
			response_json = response.json().get('public')
		else:
			response_json = response.json().get('privat')
		for key in query.keys():
			query_url = response_json.get(key, [])
			print (query_url)
			if query_url:
				return get_objects(query_url, query[key], headers)
			else:
				print ("I got nothing.")
				return ""


def get_objects(url, query, headers, params = {}):
	print("Getting info")
	response = requests.get(url, headers = headers, params = params)
	if response.status_code == 200:
		field_name = query['field']
		field_value = query['value']
		response_json = response.json().get('results')
		for items in response_json:
			if items[field_name] == field_value:
				print("appending item!")
				print(items)
				yield items
	else:
		yield "Error"