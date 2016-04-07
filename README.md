# eshaw-finalproject
Shakespearean play character analysis

##Project Update

#Did you meet your first milestone? Did you change your milestone?

My original milestone was two-fold:
1) To have a function that parses Shakespeare's plays in a way that allows for easy analysis.
2) To have a rough, initial start on character analysis.
Both milestones have been met via a first pass/iteration. Further improvements can and may still happen based on need.

#What have you finished so far? Include background reading, development, brainstorming, and results.

Background reading:
Most of the background reading for this project were accomplished before the project proposal was submitted.

Development:
There were 3 main points of developement so far.
1) The proposal referenced two GitHub repositories of other users' work done on Shakespeare's text. One was an SQL database of statistical summaries on each of Shakespeare's plays. In order to use this resource, I had to (learn to) set up a local database and feed in the data provided. Currently, my database contains 6 reference tables which contain a lot of summary information on the various plays, characters, setting, and related word forms. This database will serve as a good organizational reference for future analysis (e.g. checking which characters are from which play). The second repository was actually the repository associated with the 2011 Open Shakespeare Project. Out of all that information, I've been able to pull out a couple of useful folders. One is a data source for all of Shakespeare's plays in tagged xml format. Another is a set of functions that take in these xml files and perform basic parsing, tagging, and summary on them. A significant amount of time was spent installing these two repositories (especially since some dependencies were out dated) and understanding what capabilities they had.
2) As part of understanding these repositories and their capabilities, I also implemented ways of improving and building up on them. For example, I wanted a more rigours Part of Speech tagging function than the one provided by the nltk library and had to work on installing the Standford NLP Library and getting it working with a Paython wrapper.
3) As a first pass on running character analysis, I've focused on developing my work on one play first, before scaling. I've put together a rough script that calculates the vector distances between every pair of major character (defined to be characters who say more than 100 words) based on 7 metrics. These metrics are currently very arbitrary, but include frequency counts of: number of words, number of hapaxes, frequency of "yes", "no", "?" etc. However, they are meant to stand in for more relevant metrics later.

Brainstorming:
1) Our recent topics on context vectors has been inspiring me to start thinking about ways I could implement the concept into my analysis. As an outcome of the A5 assignment, I hope to reuse that code for my character analysis.
2) While reading the canonical literary works on Shakespearean character analysis, a reoccurring theme is understanding characters through their relational distances to other characters. I currently have a way of visualizing this, but am still bouncing around ideas on how I can convert this into measurable quantities.

#You should aim to have *some* results by the update. Describe them.
#Are the results satisfactory? If they aren't, what do you plan to modify/add?

The analysis on measuring the distance between character pairs currently returns character pairs that have the shortest distance as a proxy for "similarity". After a first pass on implementing this, a major obstacle I'm running into is a lack of symetry between character pairs. Character A will be paired with Character B with a distance of alpha but Character B will be paired with Character C with a distance of beta. I'm in the process of analyzing the results to 1) figure out where the calculations went wrong, and 2) compare the relative differences in the distance values (since the range seems particularly high for normalize percentage values). Since I'm only just starting on the character analysis, I have a lot of analysis approachs I want to test out first to see which methods make sense and return sensible results.


#Updates to your project plan, like goals and techniques that have changed since your proposal.

Most of the project plan has remained the same. The only addition I'm interested in adding is a visual aspect, to make my results more understandable and summarize them in a more efficient method.
