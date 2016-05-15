import csv, sys, os, nltk, re, string, collections
import numpy as np
import matplotlib.pyplot as plt
import jsonrpc
from simplejson import loads
from scipy import stats
from sklearn import cluster
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

def get_pca_tfidf(dir_path, components=0):
	'''
    reads all character's csv files and finds the TF-IDF for each character,
    treating each character's file as a single document. A PCA (principle
    Component Analysis) is run on these values and filtered for the most 
	principled dimensions (threshold set at .5%). Function returns 2 
	variables, 1) the list of characters in order of processing 2) the 
	filtered principle values of the PCA
    '''
	list_of_characters_csv=[]
	token_dict = collections.defaultdict(list)
	similarity_dict = collections.defaultdict(list)

	for subdir, dirs, files in os.walk(os.path.join(dir_path, 'csv')):
	    print 'Number of files present: ' + str(len(files))
	    for file in files:
	        list_of_characters_csv.append(file[0:-4])
	        file_path = subdir + os.path.sep + file
	        shakes = open(file_path, 'r')
	        text = shakes.read()
	        token_dict[file] = text

	# find TF-IDF
	tf = TfidfVectorizer(analyzer='word', min_df = 0)
	tfidf_matrix =  tf.fit_transform(token_dict.values())

	# conduct PCA
	if (components == 0):
		pca = PCA()
		pca_tfidf = pca.fit_transform(tfidf_matrix.toarray())
		sig_components = [x for x in pca.explained_variance_ if x > .005]

		pca = PCA(n_components = len(sig_components))
		return list_of_characters_csv, pca.fit_transform(tfidf_matrix.toarray())
	else:
		pca = PCA(n_components = components)
		return list_of_characters_csv, pca.fit_transform(tfidf_matrix.toarray())

def get_char_grammar(dir_path):
	'''
    cleans all character's txt files and finds the character's set of verbs,
    attributes, and modifier words. Function returns 5 variables:
    1) the list of characters in order of processing 
	2) the dictionary of every character's list of sentences {'character': ['sentence 1', 'sentence 2']}
	3) the character's set of verb words
	4) the character's set of attribute words
	5) the character's set of modifier words
    '''
	list_of_characters_txt=[]
	charact_vocab = collections.defaultdict(list)
	tagged_vocab = collections.defaultdict(list)
	charact_sents = collections.defaultdict(list)
	charact_verbs = collections.defaultdict(list)
	charact_attrs = collections.defaultdict(list)
	charact_mods = collections.defaultdict(list)
	attrsets = collections.defaultdict(list)
	modsets = collections.defaultdict(list)
	verbsets = collections.defaultdict(list)

	for subdir, dirs, files in os.walk(os.path.join(dir_path, 'txt')):
	    print 'Number of files present: ' + str(len(files))
	    for file in files:
	        character_name = file[0:-4]
	        list_of_characters_txt.append(character_name)
	        file_path = subdir + os.path.sep + file
	        shakes = open(file_path, 'r')
	        corpus = shakes.read()
	        charact_vocab[character_name] = corpus.split(" ")
	        tagged_vocab[character_name] = nltk.pos_tag(corpus.split(" "))
	        charact_sents[character_name] = re.split('[?!;.:]',corpus)
	        del charact_sents[character_name][-1]
	        
	        verbs = []
	        attrs = []
        	mods = []
	        for pair in tagged_vocab[character_name]:
	            word, tag = pair
	            if re.search('V', tag):
	                verbs.append(word)
	            if re.search('JJ', tag) or re.search('NN', tag):
                	attrs.append(word)
	            if re.search('JJ', tag) or re.search('RB', tag):
	                mods.append(word)
	        charact_verbs[character_name] = verbs
	        verbsets[character_name] = set(verbs)
	        charact_attrs[character_name] = attrs
	        attrsets[character_name] = set(attrs)
	        charact_mods[character_name] = mods
	        modsets[character_name] = set(mods)
	return list_of_characters_txt, charact_sents, verbsets, attrsets, modsets

def get_grammar(dir_path, dbug=False):
	'''
    takes character's sentences (found with get_char_grammar) and counts
    the number of Agent Verbs (AV), Patient Verbs(PV), Attributes(Attr), 
    and Modifiers (Mod).
    (the first three are as described by Bamman et al., 2014; see project
    proposal for citation)

	Function returns 2 variables:
    1) the list of characters in order of processing 
	2) the count matrix of each dependency case's occurance, with 4 columns 
	(one for each type of dependency set(AV, PV, Attr, Mod)), and each row 
	represents one character's set of dependency type counts. 
		(size of matrix will be len(characters)X4)
    '''
    server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),jsonrpc.TransportTcpIp(addr=("127.0.0.1", 8080)))
    list_of_characters_txt, charact_sents, verbsets, attrsets, modsets = get_char_grammar(dir_path)

    verb_types = collections.defaultdict(list)
    agent_tags = set(['nsubj','agent'])
    patient_tags = set(['dobj','nsubjpass','iobj'])
    mod_types = collections.defaultdict(list)
    attr_tags = set(['nsubj','appos','amod','nn'])
    mod_tags = set(['acomp','advmod','prepc','tmod','xcomp'])

    char_dep = np.zeros((len(list_of_characters_txt),4))
    for c,character in enumerate(list_of_characters_txt):
        if dbug:
            print 'processing: ' + character + ' number: ' + str(c)

        cur_verbset = verbsets[character]
        cur_attrset = attrsets[character]
        cur_modset = modsets[character]
        for s, sentence in enumerate(charact_sents[character]):
        	# pre-process the sentence and make sure corenlp works for it
            if len(sentence) == 0:
                continue
            elif sentence[0] in set(string.punctuation):
                sentence = sentence[2:]
            elif ' - ' in sentence:
                sentence = sentence.replace(' - ','')
                
            try:
                result = loads(server.parse(sentence))
            except:
                failed_sent = (character, str(s), sentence)
                txtfile = open(os.path.join(dir_path, "failed_sentences.txt"), "wb")
                txtfile.write(' '.join(failed_sent))
                break

            #ID dependencies
            for relation in result['sentences'][0]['dependencies']:

                if (relation[1] in cur_verbset) or (relation[2] in cur_verbset):
                    if relation[0] in agent_tags:
                        char_dep[c,0] += 1
                    elif (relation[0] in patient_tags) or ('prep_' in relation[0]):
                        char_dep[c,1] += 1

                elif (relation[1] in cur_attrset) or (relation[2] in cur_attrset):
                    if relation[0] in attr_tags:
                        char_dep[c,2] += 1

                elif (relation[1] in cur_modset) or (relation[2] in cur_modset):
                    if relation[0] in mod_tags:
                        char_dep[c,3] += 1

    return list_of_characters_txt, char_dep

def get_context_matrix(A,B):
	'''
	Z-score matrix B and combine it with matrix A.
	Row counts between A and B should be same. Column count doesn't matter.
	Function returns concatenated matrix of A and Z-scored matrix B
    '''
	agent = stats.zscore(B[:,0])
	patient = stats.zscore(B[:,1])
	attr = stats.zscore(B[:,2])
	mod = stats.zscore(B[:,3])
	grammar_matrix = np.column_stack((agent,patient,attr,mod))
	return np.concatenate((A,grammar_matrix), axis=1)

def clustering(num, matrix, query=True, characters=[]):
	'''
    Optimize k-means clustering on inputted 'matrix' across 'num' number 
    of possible clusters. 

	query=True state:
    Function plots 2 figures of inertia change as number of clusters 
    increment. 

    query=False state:
    User can iput number ('num') of clusters to group data in 'matrix'.
    Function returns 3 variables: 1) overall percentage distribution of 
    data in 'num' number of clusters, 2) dictionary to look up which 
	cluster each character ('characters') is assigned 
	{'character': cluster # (int)}
	, and 3) dictionary	to look up which characters a cluster contains
	{cluster # (int): ['character 1', 'character 2']}
    '''

    if query:
        n = num
        inertias = []

        for i in range(n):
            centroids,labels,inertia = cluster.k_means(matrix,n_clusters=i+1)
            inertias.append(inertia)

        #find fit
        coefficients = np.polyfit(range(n), inertias, 6)
        polynomial = np.poly1d(coefficients)
        fit_y = polynomial(range(n))

        #Absolute change in inertia
        delta_yfit = np.diff(fit_y)
        plt.plot(range(1,len(delta_yfit)+1), delta_yfit)
        plt.xlabel('Nth cluster',fontsize=14)
        plt.ylabel('inertia change',fontsize=14)
        plt.title('Inertia changes for various number of clusters',fontsize=18)
        plt.show()

        # Relative change in inertia
        for i in range(n-1):
            print [i,i+1,abs(np.round(delta_yfit[i]/fit_y[i],2))]

        plt.plot(range(1,len(delta_yfit)+1), abs(delta_yfit/fit_y[0:num-1]))
        plt.xlabel('Nth cluster',fontsize=14)
        plt.ylabel('% change in inertia',fontsize=14)
        plt.title('abs(% of Inertia change) for various number of clusters',fontsize=18)
        plt.show()

    else:
        cluster_func = cluster.KMeans(n_clusters=num, n_init =20)
        cluster_func.fit(matrix)
        assignments = cluster_func.labels_

        # find overall distribution
        counts = np.zeros(num)
        for i in range(len(assignments)):
            counts[assignments[i]] +=1
        overallDist = np.round(np.divide(counts, float(sum(counts))),4)

        # make dict out of cluster -> characters
        cluster_assign = collections.defaultdict(list)
        for ith in range(0,num):
            cluster_assign[ith] = [characters[i] for i in np.where(cluster_func.labels_==ith)[0]]

        # make dict out of characters -> clusters
        charact_assign = dict(zip(characters, cluster_func.labels_))

        return overallDist, charact_assign, cluster_assign

def validation(characterlist, similarity, char_assign):
	'''
	Counts the number of overlap in character similarity based on cosine
	similarity analysis vs. character groupings based on k-means clustering.
	Function returns 2 variables: 
	1) accuracy (as overlap between the two analyses)
	2) dictionary of each character's list of related characters as 
	calculated by cosine similarity analysis (this dictionary contains
	3 lists of the top three closely related characters (totalling 9); the 
	first list is the top three characters as judged by magnitude of cosine
	similarity, the second list as judged by positive similarity, and third
	list as judged by negative similarity, i.e. opposite or foil characters)
	{'character': [mag#1,.., mag#3, similar#1,.., similar#3, opposite#1, .., 
	opposite#3]}
	'''
    char_ind = collections.defaultdict(list)
    for c,character in enumerate(characterlist):
        char_ind[character]=c

    top3 = collections.defaultdict(list)
    for c,character in enumerate(characterlist):
        similarity[c] = [val if val < similarity[c].max() else 0.0 for val in similarity[c]]
        magnitude = [abs(val) for val in similarity[c]]
        top3_mag = sorted(zip(magnitude, characterlist), reverse=True)[:3]
        top3_names = [name for val, name in top3_mag]
        vals = []
        for name in top3_names:
            vals.append(similarity[c][char_ind[name]])
                
        sim3 = sorted(zip(similarity[c], characterlist), reverse=True)[:3]
        op3 = sorted(zip(similarity[c], characterlist), reverse=False)[:3]
        top3_list = []
        top3_list.append(zip(vals, top3_names))
        top3_list.append(sim3)
        top3_list.append(op3)
        top3[character] = [item for sublist in top3_list for item in sublist]

    correct = 0
    incorrect = 0
    for pair in top3[character]:
        if pair[0] > .5:
            if char_assign[pair[1]] == char_assign[character]:
                correct +=1
            else:
                incorrect +=1

    return float(correct)/(correct + incorrect), top3

def main(dir_path):
    characterlistcsv, tfidf = get_pca_tfidf(dir_path)
    print 'I now have PCA on TF-IDF.'
    characterlisttxt, grammar = get_grammar(dir_path, True)
    print 'I now have Grammar.'
    
    reordered_gram = np.zeros((len(characterlistcsv),4))
    for n,name in enumerate(characterlistcsv):
        grammar_ind = characterlisttxt.index(name)
        reordered_gram[n,:] = grammar[grammar_ind,:]
    context_matrix = get_context_matrix(tfidf, reordered_gram)
    similarity = cosine_similarity(context_matrix)
    
    clustering(len(characterlistcsv), context_matrix, query=True, characters= characterlistcsv)
    
    requested_clusters = input('Based on inertia change, how many clusters would you like?')
    distribution, char_labels, clusters = clustering(requested_clusters, context_matrix, query=False, characters= characterlistcsv)

    accuracy, top3 = validation(characterlistcsv, similarity, char_labels)

    print clusters
    print distribution
    # print top3
    print accuracy

if __name__ == '__main__':
	# main('/home/eshaw/Documents/NLP/eshaw2-finalproject/')
	main(sys.argv[1])
