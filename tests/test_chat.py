

from Fibot.NLP.nlg import Query_answer_unit

def main():
    qa = Query_answer_unit()
    qa.load()
    message = ""
    while message != "bye":
        message = input("Send me a message:\n")
        print("\n\nbot says: {}".format(qa.get_response(message)))

if __name__ == "__main__":
    main()
