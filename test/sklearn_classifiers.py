import pickle

import nltk
from nltk.classify.scikitlearn import SklearnClassifier

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

pickle_file = "set_housing_internet.pickle"

with open(pickle_file,"rb") as file:
    training_set = pickle.load(file)
    testing_set = pickle.load(file)
    file.close()

Naive_classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(Naive_classifier, testing_set)) * 100)
Naive_classifier.show_most_informative_features(30)


# LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
# LogisticRegression_classifier.train(training_set)
# print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)
#
# LinearSVC_classifier = SklearnClassifier(LinearSVC())
# LinearSVC_classifier.train(training_set)
# print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)
