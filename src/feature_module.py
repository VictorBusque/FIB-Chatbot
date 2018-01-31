#!/usr/bin/env python
# -*- coding: utf-8 -*-

import API_module

#ask_teacher_mail, ask_teacher_desk, ask_free_spots, ask_subject_schedule, ask_subject_classroom

def retrieve_data(intent, entities):
	intention = intent['name']
	if intention =='ask_teacher_mail':
		return "not ready yet"
	elif intention == 'ask_teacher_desk':
		return "not ready yet"
	elif intention == 'ask_free_spots':
		print ("Estoy mirando free spots")
		subject = entities[0]['value']
		print(subject)
		query = {'places-matricula': { 'field': 'assig', 'value': subject } }
		return API_module.get_main(query, True)
	elif intention == 'ask_subject_schedule':
		subject = entities[0]['value']
		query = {'horari': {'field': 'codi_assig' , 'value': subject}}
		return API_module.get_main(query, False)
	elif intention == 'ask_subject_classroom':
		subject = entities[0]['value']
		query = {'horari': {'field': 'codi_assig' , 'value': subject}}
		return API_module.get_main(query, False)
	return "not ready yet"

