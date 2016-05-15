import nltk
import sys
import csv
import string
import os
import fnmatch

def get_text(xmlplay, play_name, punctuation=False):
    '''
    loads a shakespeare xml file and returns a dictionary in the form of 
    {charachter: ['tokenized','text']}
    '''
    xml = nltk.corpus.shakespeare.xml(xmlplay)
    new = {}

    if punctuation==False:
        for i in xml.getiterator():

            # detect characters
            if i.text and i.tag == 'SPEAKER':
                char = i.text.lower()
                name = char +' ('+ play_name+')'
                if name not in new.keys():
                    new[name]=[]

            # detect words
            if i.text and i.tag == 'LINE':
                mytext = i.text
                for word in nltk.wordpunct_tokenize(mytext):
                    cur_word = word.lower().translate(None, string.punctuation)
                    if cur_word not in ['']:
                        new[name].append(cur_word)
                	# word for word, tag in withloc if tag not in ['.',',',';','"','?','\'']
                    # new[char].append(word)
        # words = [word for word in new if word not in ['.',',',';','"','?','\'']]
    elif punctuation:
        for i in xml.getiterator():

            # detect characters
            if i.text and i.tag == 'SPEAKER':
                char = i.text.lower()
                name = char +' ('+ play_name+')'
                if name not in new.keys():
                    new[name]=[]
            # detect words
            if i.text and i.tag == 'LINE':
                mytext = i.text
                for word in nltk.wordpunct_tokenize(mytext):
                    # cur_word = word.lower()
                    new[name].append(word)
    return new

def csv_file(file_path, dir, play):
    '''
    takes dictionary created by get_text function and creates csv files
    of the tokenized words for each major character (defined as having
    over 500 words) 
    '''
    speeches = get_text(file_path, play, True)

    for character in speeches.keys():
        if len(speeches[character]) > 500:
            wr_file_to = os.path.join(dir, 'csv/')
            csvfile = csv.writer(open(wr_file_to+character+".csv", "wb"), delimiter = ',')
            csvfile.writerow(speeches[character])

def txt_file(file_path, dir, play):
    '''
    takes dictionary created by get_text function and creates txt files
    of all lines spoken by each major character (defined as having
    over 500 words) 
    '''
    speeches = get_text(file_path, play, True)

    for character in speeches.keys():
        if len(speeches[character]) > 500:
            wr_file_to = os.path.join(dir, 'txt/')
            txtfile = open(wr_file_to+character+".txt", "wb")
            txtfile.write(' '.join(speeches[character]))


def main(text_path, store_path):
    '''
    Creates csv and txt files for each major character at specified location
    '''
    for subdir, dirs, files in os.walk(text_path):
        for file in files:
            if fnmatch.fnmatch(file, '*.xml'):
                print file
                path = os.path.join(text_path, file)
                csv_file(path, store_path, file[0:-4])
                txt_file(path, store_path, file[0:-4])



if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])