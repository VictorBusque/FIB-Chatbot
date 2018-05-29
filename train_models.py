#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- Local imports --#
from Fibot.fibot import Fibot
import argparse
import tensorflow as tf


"""
    Allows to decide the training type:
        by hand: trains rapidly the model and allows the user to add new stories interactively
        not by hand: trans both the nlu and dialog model and stores them in the model folder.
"""
def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--nlu',
                        nargs=1,
                        required = False,
                        choices=['es', 'ca', 'en', 'n'],
                        action = 'append',
                        help='Language for the interpretation')
    parser.add_argument('--dialog',
                        nargs=1,
                        required = False,
                        choices=['y','n'],
                        default = [],
                        help='File for the interpreter to use')
    args = parser.parse_args()
    print(args)
    trainNLU = False
    trainNLG = False
    languages = []
    if args.nlu:
        languages = [i[0] for i in args.nlu]
        trainNLU = True
    if args.dialog: trainNLG = bool(args.dialog[0] == 'y')

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    tf.Session(config=config)

    fibot = Fibot()
    fibot.qa.load(trainNLG=trainNLG, trainNLU = trainNLU, train_list = languages)
    return

if __name__ == "__main__":
    main()
