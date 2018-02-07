#!/usr/bin/env python
# -*- coding: utf-8 -*-

import API_module

#ask_teacher_mail, ask_teacher_desk, ask_free_spots, ask_subject_schedule, ask_subject_classroom

def retrieve_data(intent, entities, chat_id):
	intention = intent['name']
	if intention == 'non_query':
		return "Y si me preguntas algo de la FIB campeón máquina fiera mastodonte tifón."
	if intention =='ask_teacher_mail':
		return "not ready yet"
	elif intention == 'ask_teacher_desk':
		return "not ready yet"
	elif intention == 'ask_free_spots':
		print ("Estoy mirando free spots")
		subject = entities[0]['value'].upper()
		print(subject)
		query = {'places-matricula': { 'field': 'assig', 'value': subject } }
		return API_module.get_main(query, public = True)
	elif intention == 'ask_subject_schedule':
		print("Preguntaste por tu horario")
		subject = entities[0]['value'].upper()
		print("subject = %s"%subject)
		query = {'horari': {'field': 'codi_assig' , 'value': subject}}
		print(query)
		return API_module.get_main(query, chat_id, False)
	elif intention == 'ask_subject_classroom':
		print("Preguntaste por alguna clase")
		subject = entities[0]['value'].upper()
		print("subject = %s"%subject)
		query = {'horari': {'field': 'codi_assig' , 'value': subject}}
		print(query)
		return API_module.get_main(query, chat_id, False)
	return "not ready yet"
