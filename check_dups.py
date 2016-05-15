import nltk
import sys
import csv
import string
import os
import fnmatch
import collections
from collections import Counter


def get_text(xmlplay):
	xml = nltk.corpus.shakespeare.xml(xmlplay)
	new = {}
	# w_dups = []

	for i in xml.getiterator():

		# detect characters
            if i.text and i.tag == 'SPEAKER':
                char = i.text.lower()
                if char not in new.keys():
                    new[char]=[]
            # detect words
            if i.text and i.tag == 'LINE':
                mytext = i.text
                for word in nltk.wordpunct_tokenize(mytext):
                    # cur_word = word.lower()
                    new[char].append(word)

	return new

def count_dups(dir_path):
	char_total = []


	for subdir, dirs, files in os.walk(dir_path):
		for file in files:
			if fnmatch.fnmatch(file, '*.xml'):
				# print file
				path = os.path.join(dir_path, file)
				speeches = get_text(path)
				for character in speeches.keys():
					if len(speeches[character]) > 500:
						char_total.append(character)
	print Counter(char_total)

def main(dir_path):
	dups = {'messenger': 9, 'first lord': 6, 'clown': 6, 'gloucester': 5, 'antonio': 5, 'bardolph': 4, 'northumberland': 4, 'servant': 4, 'york': 4, 'warwick': 4, 'first gentleman': 4, 'second lord': 3, 'westmoreland': 3, 'clarence': 3, 'buckingham': 3, 'first senator': 3, 'katharine': 3, 'pistol': 3, 'queen margaret': 3, 'suffolk': 3, 'prologue': 3, 'falstaff': 3, 'somerset': 3, 'king henry vi': 3, 'prince henry': 3, 'balthasar': 2, 'paris': 2, 'lord': 2, 'charles': 2, 'pompey': 2, 'hostess': 2, 'king edward iv': 2, 'mistress quickly': 2, 'claudio': 2, 'captain': 2, 'richard': 2, 'burgundy': 2, 'exeter': 2, 'king henry iv': 2, 'angelo': 2, 'duchess of york': 2, 'gower': 2, 'queen elizabeth': 2, 'flavius': 2, 'nym': 2, 'montague': 2, 'king henry v': 2, 'helena': 2, 'fool': 2, 'lady percy': 2, 'ferdinand': 2, 'duchess': 2, 'king of france': 2, 'soothsayer': 2, 'mariana': 2, 'demetrius': 2, 'lucius': 2, 'first murderer': 2, 'portia': 2, 'shallow': 2, 'third citizen': 2, 'maria': 2, 'queen': 2, 'prince edward': 2, 'third gentleman': 2, 'shepherd': 2, 'gentleman': 2, 'vernon': 2, 'poins': 2, 'gratiano': 2, 'archbishop of york': 2, 'hastings': 2, 'sebastian': 2, 'page': 2, 'first citizen': 2, 'peter': 2, 'clifford': 2, 'porter': 2, 'host': 2, 'duke': 2, 'salisbury': 2, 'brutus': 2, 'lucilius': 2, 'mortimer': 2, 'bianca': 2, 'margaret': 2}

	loc_dups = collections.defaultdict(list)
	for subdir, dirs, files in os.walk(dir_path):
		for file in files:
			if fnmatch.fnmatch(file, '*.xml'):
				speeches={}
				# print file
				path = os.path.join(dir_path, file)
				speeches = get_text(path)
				for character in speeches.keys():
					if len(speeches[character]) > 200:
						overlap = set(speeches.keys()).intersection(dups.keys())
						loc_dups[file]=overlap
	print dups.keys()

if __name__ == '__main__':
    count_dups('/home/eshaw/Documents/NLP/eshaw2-finalproject/texts')
    # for subdir, dirs, files in os.walk('/home/eshaw/Documents/NLP/eshaw2-finalproject/txt'):
    #     for file in files:
    #     	print file
            # if fnmatch.fnmatch(file, '*.txt'):
            #     print file