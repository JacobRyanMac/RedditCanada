from Database import Query
from Body import FeaturePipeline

import pickle
from nltk import NaiveBayesClassifier
from nltk import classify

db = Query('canada_subreddit.db')
db.connect()
cur = db.cursor()
cur.execute('''
SELECT c.body, s.label
FROM submissions as s, comments as c
WHERE s.submission_id = c.submission_id
AND (s.label = "Climate"
OR s.label = "Housing");
''')
data = cur.fetchall()
feature_set = FeaturePipeline().create_set(data)

split = lambda x: - int(len(x) / 5)
k = split(feature_set)
training_set = feature_set[:k]
testing_set = feature_set[k:]


print('Now training...')

Naive_classifier = NaiveBayesClassifier.train(training_set)
print("Naive Bayes Algo accuracy percent:", (classify.accuracy(Naive_classifier, testing_set)))
Naive_classifier.show_most_informative_features(30)
#
# with open(pickle_file,"wb") as save_classifier:
#     pickle.dump(Naive_classifier, save_classifier)
#     save_classifier.close()
