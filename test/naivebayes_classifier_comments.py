import pickle
import nltk
from redditSQL import Features

pickle_file = "naive_bayes_classifier.pickle"
database = 'canada_subreddit.db'
SQL_query = '''
SELECT c.body, s.label
FROM submissions as s, comments as c
WHERE s.submission_id = c.submission_id
AND (s.label = "Internet"
OR s.label = "Housing"
OR s.label = "Pot");
'''

featuresets = Features(SQL_query,database).make_featureset()

split = lambda x: - int(len(x) / 5)
k = split(featuresets)
training_set = featuresets[:k]
testing_set = featuresets[k:]

Naive_classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(Naive_classifier, testing_set)) * 100)
Naive_classifier.show_most_informative_features(30)

# with open(pickle_file,"wb") as save_classifier:
#     pickle.dump(Naive_classifier, save_classifier)
#     save_classifier.close()
