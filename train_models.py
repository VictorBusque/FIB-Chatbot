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
    main("train")
