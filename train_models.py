#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- Local imports --#
from Fibot.fibot import Fibot
import argparse

"""
    Allows to decide the training type:
        by hand: trains rapidly the model and allows the user to add new stories interactively
        not by hand: trans both the nlu and dialog model and stores them in the model folder.
"""
def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--nlu',
                        nargs=1,
                        required = True,
                        choices=['y','n'],
                        default = ['y'],
                        help='Language for the interpretation')
    parser.add_argument('--dialog',
                        nargs=1,
                        required = False,
                        choices=['y','n'],
                        default = ['n'],
                        help='File for the interpreter to use')
    args = parser.parse_args()
    print(args)
    trainNLU = False
    trainNLG = False
    if args.nlu: trainNLU = bool(args.nlu[0] == 'y')
    if args.dialog: trainNLG = bool(args.nlu[0] == 'n')

    fibot = Fibot()
    fibot.qa.load(trainNLG=trainNLG, trainNLU = trainNLU)
    return

if __name__ == "__main__":
    main()
