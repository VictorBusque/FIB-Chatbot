#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- Local imports --#
from Fibot.fibot import Fibot


"""
    Allows to decide the training type:
        by hand: trains rapidly the model and allows the user to add new stories interactively
        not by hand: trans both the nlu and dialog model and stores them in the model folder.
"""
def main(mode):
    fibot = Fibot()
    if mode == "train": fibot.qa.load(train=True)
    if mode == "manual":
        fibot.qa.load(train=False)
        fibot.qa.train_manual()
    return

if __name__ == "__main__":
    y_s = None
    while (y_s != "y" and y_s != "n"): y_s = input("Do you wish to input stories by hand? [y/n]\n")
    if y_s == "y": main("manual")
    else: main("train")
