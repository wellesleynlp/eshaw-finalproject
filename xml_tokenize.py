import nltk
import sys

def get_text(xmlplay):
    '''
    loads a shakespeare xml file and returns a dictionary in the form of 
    {charachter: ['tokenized','text']}
    '''
    xml = nltk.corpus.shakespeare.xml(xmlplay)
    new = {}
    for i in xml.getiterator():

        # detect characters
        if i.text and i.tag == 'SPEAKER':
            char = i.text
            if char not in new.keys():
                new[char]=[]
        # detect words
        if i.text and i.tag == 'LINE':
            mytext = i.text
            for word in nltk.wordpunct_tokenize(mytext):
            	# word for word, tag in withloc if tag not in ['.',',',';','"','?','\'']
                new[char].append(word)
    return new

def relationbyword(words):
    '''
    takes a dictionary {charachter: ['tokenized','text']} and plots the
    conditional verbs per character if they say more than 100 lines
    '''
    conditionals = nltk.defaultdict(dict)
    try:
        for char, text in words.items():
            tagged = nltk.pos_tag(text)
            conditionals[char] =  nltk.FreqDist(
                [positionedword for positionedword,
                tag in tagged if tag == 'MD']).items()  

        return conditionals
    except AttributeError:
        print "please enter a dictionary in the form of {character: ['tokenized','text']} "

def graphrelation(words,conditionals):
    '''
    given a speech list in the form of {'YOUNG SIWARD': ['What', 'is','thy',
    'name','?'], } creates a graphviz map of conditionals per (important)
    character
    '''
    import pydot

    all = []
    for char, words in conditionals.items():
        for word in words:
            all.append((char,word[0].lower()))

            
    graphic = pydot.graph_from_edges(all)
    for char in conditionals:
        new = pydot.Node(char,color='green',shape='doubleoctagon',fontname='Arial',fontsize='12',rank='source', ranksep = '1.2')
        graphic.add_node(new)
    for char, word in all:
        new = pydot.Node(word,color='purple',shape='note',fontname='Arial',fontsize='8')
        graphic.add_node(new)


    graphic.set_overlap('TRUE')
    graphic.set_splines('True')
    graphic.set_suppress_disconnected('TRUE')
    graphic.write_png('test.png',prog='twopi')

def main(file_path):
    speeches = get_text(file_path)
    print speeches

    # with open("Output_test.txt", "w") as outfile:
    #     outfile.write("%s" % speeches)

if __name__ == '__main__':
    main('all_well.xml');
    # main(sys.argv[0])