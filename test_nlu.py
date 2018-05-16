from Fibot.NLP.nlu import NLU_unit
from pprint import pprint

if __name__ == '__main__':
    nlu = NLU_unit()
    nlu.load()
    language = input("Qué idioma quieres probar? (ca, es, en): ")
    message = None
    while message != "quit":
        message = input("Introduce el mensaje:\n")
        print("Esta es la intención del mensaje:")
        pprint(nlu.get_intent(message, language))
        print("\nEstas son las entidades")
        pprint(nlu.get_entities(message, language))
        print("\n\n")
