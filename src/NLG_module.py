from chatterbot import ChatBot
from chatterbot.conversation import Statement

import bot


# Create a new instance of a ChatBot
chatbot = ChatBot(
    "Fibot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter"
)


train_queue = {}
CONVERSATION_ID = 0


def load_bot():
	global CONVERSATION_ID, chatbot
	CONVERSATION_ID = chatbot.storage.create_conversation()


def give_feedback(chat_id, correct = True, correct_statement = ''):
	global CONVERSATION_ID, chatbot, train_queue
	if not correct:
		message = train_queue[chat_id]['message']
		correct_statement = Statement(correct_statement)
		chatbot.learn_response(correct_statement, message)
		chatbot.storage.add_to_conversation(CONVERSATION_ID, message, correct_statement)
		bot.send_message(chat_id,'Conocimiento añadido al sistema! Gracias!')
	else:
		bot.send_message(chat_id,'Estupendo!')



def process_answer_training(chat_id, message):
	global train_queue, chatbot
	print("Query de %s con mensaje %s"%(chat_id, message))
	input_statement = Statement(message)
	statement, response = chatbot.generate_response(input_statement, CONVERSATION_ID)
	print(statement)
	print(response)
	bot.send_message(chat_id,'Es "{}" una respuesta coherente a "{}"? (Sí/No)'.format(response, message))
	train_queue[chat_id] = {
		'message': input_statement,
		'response': response
	}


def get_response(message, debug = False):
	global CONVERSATION_ID, chatbot
	input_statement = Statement(message)
	_, response = chatbot.generate_response(input_statement, CONVERSATION_ID)
	print(response)
	if debug:
		return "%s, confidence = %d"%(response['text'], response['confidence'])
	else:
		return str(response)
