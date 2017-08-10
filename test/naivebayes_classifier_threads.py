import pickle
import nltk
from redditSQL import Features, Threads

pickle_file = "naivebayes_threads.pickle"
database = 'canada_subreddit.db'
thread_folder = 'threads/'
labels = ['Climate','Housing']

th = Threads(database)
thread_body = th.make_body(labels,thread_folder)
featuresets = Features(body=thread_body).make_featureset()

split = lambda x: - int(len(x) / 5)
k = split(featuresets)
training_set = featuresets[:k]
testing_set = featuresets[k:]

print('Now training...')

Naive_classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Naive Bayes accuracy percent:", (nltk.classify.accuracy(Naive_classifier, testing_set)))
Naive_classifier.show_most_informative_features(20)

with open(pickle_file,"wb") as save_classifier:
    pickle.dump(Naive_classifier, save_classifier)
    save_classifier.close()
