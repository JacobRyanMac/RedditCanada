# import Labels
import random
from nltk import word_tokenize
from nltk.probability import FreqDist
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
        super(Feature,self).__init__(body)
        self.label = label
        # self.word_features =

    def create_feature(self, word_bank):
        words = set(self.tokens)
        features = {}
        for w in word_bank:
            features[w] = (w in words)
        return features, self.label

class FeaturePipeline(Feature):
    def __init__(self):
        pass
        # self.data = data

    def create_set(self, data):
        random.shuffle(data)
        wb = self.gather_features(data)
        fs = []
        for d in data:
            fs.append((Feature(d[0],d[1]).create_feature(wb)))
        return fs

    def gather_features(self, data):
        all_bodies = []
        for d in data:
            for t in Body(d[0]).tokens:
                all_bodies.append(t)
        all_words = FreqDist(all_bodies)
        word_features = list(all_words.keys())[:3000]
        return word_features
