#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- Local imports --#
from Fibot.fibot import Fibot


def main():
    fibot = Fibot()
    fibot.qa.load(train=True)
    return

if __name__ == "__main__":
    main()
