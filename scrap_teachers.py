#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
from __future__ import division
from codecs import decode
import requests
import re
import json
import os

class Directory(object):

    """This class contains all the necessary procedures to scrap http://directori.upc.edu

    Attributes:
        type(:obj:`str`): string like 'cs','ac','essi' corresponding to UPC's FIB departments
        teacher_url(:obj:`str`): url that can easily be formatted to access teacher's pages
        url(:obj:`str`): url of the root site for the department (contains IDs for all teachers of the department)
        data(:obj:`dict`): dictonary with the following format that contains the information about the teachers
            {
                name: {
                    'mail': value,
                    'office': value
                }
            }
            where value can either be None or (:obj:`str`)
    """
    def __init__(self, key):
        self.type = key
        print("Scraper defined for {}'s department".format(self.type))
        self.teacher_url = 'http://directori.upc.edu/directori/dadesPersona.jsp?id={}'
        with open('./Data/urls_upc.json', 'r') as fp:
        	self.url = json.load(fp)[key]
        self.data = {}

        self.start_id = '<a href="dadesPersona.jsp?id='
        self.end_id = '">'

        self.start_name = '<td colspan="2"><b>'
        self.end_name = '</b></td>'

        self.start_mail = '<span class="mail">'
        self.end_mail = '</span>'

        self.start_office = '</a><br />'
        self.end_office = '<br/>C. JORDI GIRONA, 1-3<br/>'

    """
        This function scraps the directory saving the ids of each teacher, and uses
        the teacher url formatted with each id to get the information parsing the html
        file using regular expressions.
    """
    def scrap_directory(self):
        print("scraping {} ...".format(self.url))
        response = requests.get(self.url)
        content = str(response.content)
        ids = self.get_ids(content)
        total = len(ids)
        current = 0
        for item in ids:
            print("{}%".format(int(float(current)/float(total) *100)))
            query_url = self.teacher_url.format(item)
            content = requests.get(query_url).content
            mail = self.get_mail(content)
            name = self.get_name(content)
            office = self.get_office(content)
            if office:
                self.data[name] = {
                    'mail': mail,
                    'office': office
                }
            else:
                self.data[name] = {
                    'mail': mail,
                    'office': None
                }
            current +=1
        self.dump_data()
        print("Scraping done succesfully!")
        print("Scraped {} teachers.".format(len(ids)))

    """
        Helper function that parses html page to extract each teacher id
    """
    def get_ids(self, content):
        ids = []
        for i in str(content).split(self.start_id):
            for item in i.split(self.end_id):
                try:
                    ids.append(int(item))
                except:
                    pass
        return ids

    """
        Helper function that parses html page to extract a mail from a teachers page
    """
    def get_mail(self, content):
        try:
            mail = str(re.findall('%s(.*)%s' % (self.start_mail, self.end_mail), str(content))[0])
            mail = mail.replace('\\n','').replace('\\t','')
            mail = mail.replace('<img src="img/arrobaG.gif" align="top"/>', '@')
            mail = mail.split('<')[0]
            return mail
        except:
            print("Teacher without mail...")
            return None

    """
        Helper function that parses html page to extract a office from a teachers page
    """
    def get_office(self, content):
        content = str(content).replace('\\n','').replace('\\t','')
        try:
            office = str(re.findall('%s(.*)%s' % (self.start_office, self.end_office), str(content))[0])
            office = office.replace('<br/>',' ').title()
            office = office.split('C. Jordi Girona')[0]
            office = office.replace('Edifici', 'Building').replace('Despatx', 'Office').replace('Planta', 'Floor')
            return office
        except:
            print ("Teacher without office...")
            return None

    """
        Helper function that parses html page to extract the name from a teachers page
    """
    def get_name(self, content):
        name = re.findall('%s(.*)%s' % (self.start_name, self.end_name), str(content))[0]
        name = str(name.replace('\\n','').replace('\\t','').replace('  ', ' ').split('<b>')[-1])
        name = decode(name, 'unicode_escape')
        if name[-1] == ' ': name = name[:-1]
        return name.lower()

    """
        Helper function that stores the results into persistence
        files can be found at Data/teachers/*.json
    """
    def dump_data(self):
        print("Dumping data into persistence...")
        try:
            os.remove('./Data/teachers/{}.json'.format(self.type))
        except:
            pass
        with open('./Data/teachers/{}.json'.format(self.type), 'w') as fp:
        	json.dump(self.data, fp, indent = 2)


if __name__ == "__main__":
    directory = input("Which directory do you want to scrap? (type 'all' to scrap every directory)\n")
    if directory != 'all':
        directory = Directory(directory)
        directory.scrap_directory()
    else:
        directories = ['essi','cs','ac']
        for directory in directories:
            directory = Directory(directory)
            directory.scrap_directory()
