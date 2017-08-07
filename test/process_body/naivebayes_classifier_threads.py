import pickle
import nltk
from FeatureSet import Features
from FeatureSet import Threads

pickle_file = "NB_classifier_threads.pickle"
database = '../canada_subreddit_test.db'
thread_folder = 'threads/'
labels = ['Pot','Housing','Internet']

th = Threads(database)
thread_body = th.make_body(labels,thread_folder)
featuresets = Features(body=thread_body).make_featureset()

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
