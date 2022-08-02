# StudyFrenchWords
Given a database of words in French consisting of a word and its frequency count:

Via the command prompt, the user is prompted to think of a definition for a french word.
Then the definition is shown via collins dictionary
Then, the user is asked to provide a score of 1 to 5 based on how well I know this definition with 5 being very well and 1 being not at all.
The knowledge of the word(based on a numeric value 1 to 5) is stored in an SQLite databse based on this input.

The algorithm continues to choose words to study based on the criteria of a simple reinforcement learning algorithm called the greedy bandit's algorithm
whereby 80% of the time it greedily asks me to think of a definition for the word that has the highest frequency count + lowest user knowledge score combination. However, it does not choose a word that has already been seen on the same day.
20% of the time it asks to provide a definition for a random word that is stored in the database without paying attention to the frequency count + user knowledge score combination.
I will likely tweak the algorithm in the future until I find a more optimal way of computing a frequency count + user knowledge score combination. In particular, the last date revised can be used as a variable along with the old knowledge score to be combined with the new knowledge score to provide a more accurate overall view of the knowledge of the given card.
