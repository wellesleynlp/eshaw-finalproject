# Final Project

Assignment description: http://wellesleynlp.github.io/spring16/project.html

By filling out my/our name(s) and information in the spaces below,
I certify that this is original work,
and that the submission from this commit onwards is ready to be graded.

Name: **Elena Shaw**, **eshaw2@wellesley.edu**


Link to small-vocabulary dataset: 

**1** extension days: 1 for Elena Shaw

------------------------------------------------------------------------------

# Getting Started

0 - Analyses in this repository uses a Stanford corenlp wrapper library which can be downloaded at https://github.com/dasmith/stanford-corenlp-python. Follow the repo's README for set up.

1 - Download and save set of Shakespeare's plays in xml format as linked (to Google Drive) above. (It is recommended that a separate directory is set aside for these files as well as all created files we will be making below)

2 - First, we'll create the necessary csv and txt files for each individual (main) character. The following command will create 2 folders (names 'csv' and 'txt') in the user specified directory. Within the directory of the downloaded repository, run command:
`python xml_tokenize.py path/to/xml/texts path/to/store/character/files`

For myself, I set the xml path as 'Documents/NLP/eshaw2-finalproject/texts/'and the character file path as 'Documents/NLP/eshaw2-finalproject/' to keep things in the same location.

3 - Before doing anything else, we need to set up our server for accessing Stanford corenlp. Within the downloaded python wrapper library for Stanford's corenlp directory that contains 'corenlp.py', run the following command:
`python corenlp.py`

4 - Now that we've created 443 main character files, let's run our analyses on the characters. With the directory to csv and txt files as our path, we can run the command for doing so is:
`python analysis.py 'path/to/csv/and/txt/files'`

5 - The analysis will take a while. It will update you as it analyzes each character. As the analyses run, there wil be a few user inputs required. First, 2 line plots will pop up. The plots are meant to help you choose the optimal number of clusters to group the characters into. I would suggest picking the number of cluster based on minimizing inertia (the first plot) AND minimizing the (percentage) change in inertia (the second plot). Only by closing the first plot can you view the second plot. Second, the command line will then prompt with the number of optimal clusters to run the k-means clustering analysis. Enter your chosen number and the analysis will continue.

6 - At the end, once all analyses are done, 3 things will be printed:
	a) A dictionary showing the list of characters assigned to each cluster number
	b) The percentage distribution of all characters across all clusters
	c) The percentage overlap between character similarity as assigned by cosine similarity and character similarity as assigned by k-means clustering

