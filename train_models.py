#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- Local imports --#
from Fibot.fibot import Fibot


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
