from Fibot.NLP.nlu import NLU_unit
from pprint import pprint
import numpy as np
import argparse

INTENT_AMOUNT = 11
intent2idx = {
    'ask_teacher_mail': 0,
    'ask_teacher_office': 1,
    'ask_free_spots': 2,
    'ask_subject_classroom': 3,
    'ask_subject_schedule': 4,
    'ask_subject_teacher_mail': 5,
    'ask_subject_teacher_office': 6,
    'ask_subject_teacher_name': 7,
    'ask_next_class': 8,
    'ask_exams': 9,
    'ask_pracs': 10
}
idx2intent = {
    0: 'ask_teacher_mail',
    1: 'ask_teacher_office',
    2: 'ask_free_spots',
    3: 'ask_subject_classroom',
    4: 'ask_subject_schedule',
    5: 'ask_subject_teacher_mail',
    6: 'ask_subject_teacher_office',
    7: 'ask_subject_teacher_name',
    8: 'ask_next_class',
    9: 'ask_exams',
    10: 'ask_pracs'
}
intent_conf_matrix = np.zeros([INTENT_AMOUNT,INTENT_AMOUNT])


def conf2precision(conf_matrix):
    global intent2idx
    intents = intent2idx.keys()
    accuracy_dict = {}
    for intent in intents:
        row = intent2idx[intent]
        hits = conf_matrix[row][row]
        total = sum(conf_matrix[row])
        if total == 0: accuracy_dict[intent] = 0
        else: accuracy_dict[intent] = hits/total
    return accuracy_dict

def conf2recall(conf_matrix):
    global intent2idx
    intents = intent2idx.keys()
    recall_dict = {}
    for intent in intents:
        col = intent2idx[intent]
        hits = conf_matrix[col][col]
        total = sum(conf_matrix[:,col])
        if total == 0: recall_dict[intent] = 0
        else: recall_dict[intent] = hits/total
    return recall_dict

def print_conf_matrix(conf_matrix):
    global idx2intent
    for row in range(0, len(conf_matrix)):
        if row in [0,1,3,4]: fill = "\t\t"
        elif row in [2,8,9,10]: fill = "\t\t\t"
        else: fill = "\t"
        print("{}:{}{}".format(idx2intent[row], fill, conf_matrix[row]))

def get_global_accuracy(conf_matrix):
    return sum(conf_matrix.diagonal())/sum(sum(conf_matrix))


def get_avg_precision(conf_matrix):
    precisions = conf2precision(conf_matrix)
    val = list(precisions.values())
    return np.mean(val)

def get_avg_recall(conf_matrix):
    recalls = conf2recall(conf_matrix)
    val = list(recalls.values())
    return np.mean(val)

if __name__ == '__main__':
    nlu = NLU_unit()
    nlu.load()

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--lan',
                        nargs=1,
                        required = True,
                        choices=['cat','es','en'],
                        default = ['cat'],
                        help='Language for the interpretation')
    parser.add_argument('--file',
                        nargs=1,
                        required = False,
                        help='File for the interpreter to use')
    parser.add_argument('--stats',
                        nargs=1,
                        required = False,
                        choices = ['y', 'n'],
                        default = ['n'],
                        help='If the test has to output stats')
    args = parser.parse_args()

    language = args.lan[0]
    if args.file: file_route = args.file[0]
    else: file_route = None
    if args.stats: stats = args.stats[0] == 'y'
    else: stats = False

    if not file_route:
        print("Para salir del modo de test escribe 'quit'")
        message = input("Introduce el mensaje:\n")
        while message != "quit":
            print("Esta es la intención del mensaje:")
            pprint(nlu.get_intent(message, language))
            print("\nEstas son las entidades")
            pprint(nlu.get_entities(message, language))
            print("\n\n")
            if stats:
                hit = input("Está bien la intención? (y/n): ") == 'y'
                pred_intent = nlu.get_intent(message, language)['name']
                pred_idx = intent2idx[pred_intent]
                if hit: intent_conf_matrix[pred_idx][pred_idx] += 1
                else:
                    pprint(idx2intent)
                    ok_idx = -1
                    while not ok_idx in range(0,11):
                        ok_idx = input("Cuál de los anteriores es el correcto? (0..10)\n")
                        ok_idx = int(ok_idx)
                    intent_conf_matrix[ok_idx][pred_idx] += 1
            message = input("Introduce el mensaje:\n")
    else:
        with open(file_route, 'r') as file:
            contents = file.readlines()
            size = len(contents)
            for message_idx in range(0, size, 2):
                message = contents[message_idx].rstrip()
                ok_intent = contents[message_idx+1].rstrip()
                ok_idx = intent2idx[ok_intent]
                pred_intent = nlu.get_intent(message, language)['name']
                pred_idx = intent2idx[pred_intent]
                if ok_idx != pred_idx: print("\n{}: {} -> {}".format(message, ok_intent, pred_intent))
                intent_conf_matrix[ok_idx][pred_idx] += 1


    print("\n\nLa matriz de confusión resultante es la siguiente:")
    print_conf_matrix(intent_conf_matrix)
    print("\n\nLa precisión por intenciones es la siguiente:")
    pprint(conf2precision(intent_conf_matrix))
    print("\nLa precisión promedio es {}".format(get_avg_precision(intent_conf_matrix)))
    print("\n\nEl recall por intenciones es la siguiente:")
    pprint(conf2recall(intent_conf_matrix))
    print("\nEl recall promedio es {}".format(get_avg_recall(intent_conf_matrix)))
    print("\n\nLa precisión global es de: {}".format(get_global_accuracy(intent_conf_matrix)))
