import sqlite3
import random
import nltk
import pickle

from nltk import FreqDist
from nltk.tokenize import word_tokenize
# from nltk.tokenize import wordpunct_tokenize
# wordpunct_tokenize(s)

db = sqlite3.connect('../canada_subreddit_test.db')
cur = db.cursor()
cur.execute('''
SELECT c.body, s.label
FROM submissions as s, comments as c
WHERE s.submission_id = c.submission_id
AND (s.label = 'Housing'
OR s.label = 'Pot');
''')

documents = [(word_tokenize(c[0]), c[1]) for c in cur]
random.shuffle(documents)

all_words = []
for w in documents:
    for k in w[0]:
        all_words.append(k.lower())
all_words = FreqDist(all_words)

db.close()

# Select the first 3000 words from reviews to be your features
# Returns a dictionary of booleans of whether or not a word in a review is in your features
word_features = list(all_words.keys())[:3000]
def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features
featuresets = [(find_features(rev), category) for (rev, category) in documents]

k = - int(len(featuresets) / 5)
training_set = featuresets[:k]
testing_set = featuresets[k:]

# posterior = (prior * likelihood) / evidence
classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
classifier.show_most_informative_features(30)

choice = input("Pickle? Enter True/False:")
if choice:
    save_classifier = open("naivebayes_housing_pot.pickle","wb")
    pickle.dump(classifier, save_classifier)
    pickle.dump(training_set, save_classifier)
    pickle.dump(testing_set, save_classifier)
    save_classifier.close()
