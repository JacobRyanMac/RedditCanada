# body is a comment. All string manipulation is done to the body, pardon for the label
from nltk import word_tokenize

import Labels
from Database import Query

class Body(object):
    def __init__(self,body=None):
        self.body = body
        self.tokens = self.tokenize()

    def tokenize(self):
        if self.body is None:
            return None
        else:
            all_words = []
            token_body = word_tokenize(self.body)
            for w in token_body:
                if w[:2] != "//":
                    if '*' in w:
                        word = w.replace('*','')
                    else:
                        word = w
                    all_words.append(word.lower())
            return all_words


class Feature(Body):
    def __init__(self,body,label=None):
        super(FeatureSet,self).__init__(body)
        self.label = label
        # self.word_features = self.choose_features()

    def word_features(self):
        all_words = FreqDist(self.tokens)
        word_features = list(all_words.keys())[:3000]
        return word_features

    def create_feature(self):
        # featuresets = []
        # for (words, label) in token_body:
        words = set(self.tokens)
        features = {}
        for w in self.word_features():
            features[w] = (w in words)
        return (features,self.label)

class FeaturePipeline(Feature):
    def __init__(self):
        # self.data = data

    def feature_set(self, data):
        # data is a list of tuples ie [(body,label), (body,label),...]
        # mostly for cursors in queries, but could be anything really
        fs = []
        for d in data:
            fs.append(Feature(d[0],d[1]).create_feature())
        return fs
