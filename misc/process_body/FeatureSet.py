import os
import sqlite3
import random
import nltk
from nltk import FreqDist
from nltk.tokenize import word_tokenize

class Features(object):
    """
    This object create feature sets that will be used to train classifiers.
    Body must be of a list of tuples.
    Each tuple will be a string of text of any length and a label
    Example:
        [("this is an example", Internet),
         ("strings can be threads or comments!", Housing)]

    This method can create bodies if given a SQL statement with the form:
    SELECT c.body, s.label
    FROM comments as c, submissions as s
    """
    def __init__(self, SQL_query=None, SQL_db=None, body=None):
        self.body = body
        self.SQL_query = SQL_query
        self.SQL_db = SQL_db
        if self.body is None and SQL_query is not None:
            self.query_body()

    def query_body(self):
        db = sqlite3.connect(self.SQL_db)
        cur = db.cursor()
        cur.execute(self.SQL_query)
        body = [(c[0], c[1]) for c in cur]
        db.close()
        self.body = body

    def make_featureset(self):
        token_body = [(word_tokenize(b),l) for (b,l) in self.body]
        random.shuffle(token_body)
        all_words = []
        for c in token_body:
            for w in c[0]:
                word = w
                if word[:2] != "//":
                    if '*' in word:
                        word = word.replace('*','')
                    all_words.append(word.lower())
        all_words = FreqDist(all_words)
        word_features = list(all_words.keys())[:3000]
        featuresets = []
        for (words, label) in token_body:
            featuresets.append((self.find_features(words,word_features), label))
        return featuresets

    @staticmethod
    def find_features(body, feature_list):
        words = set(body)
        features = {}
        for w in feature_list:
            features[w] = (w in words)
        return features

class Threads(object):
    '''
    Object to create and transfer threads with
    '''
    def __init__(self,SQL_db=None):
        self.SQL_db = SQL_db

    def search_roots(self,cursor,p_id,thread_file):
        cursor.execute('SELECT body, comment_id FROM comments WHERE parent_id = ?',(p_id,))
        children = cursor.fetchall()
        for c in children:
            thread_file.write(c[0] + '\n')
            self.search_roots(cursor,c[1], thread_file)

    def create_threads(self,submission,folder):
        db = sqlite3.connect(self.SQL_db)
        cur = db.cursor()
        cur.execute('''
        SELECT c.comment_id, c.body
        FROM comments as c, submissions as s
        WHERE c.submission_id = s.submission_id
        AND c.parent_id = ?
        ''',(submission,))

        parents = cur.fetchall()
        for p in parents:
            file_name = folder + p[0] + ".txt"
            with open(file_name,"w", encoding='utf-8', newline='') as file:
                file.write(p[1])
                self.search_roots(cur,p[0],file)
                file.close

        db.commit()
        db.close()

    def make_body(self,labels,folder):
        body = []
        for label in labels:
            directory = os.fsencode(folder.encode('utf-8') + label.encode('utf-8') +b'/')
            for file in os.listdir(directory):
                with open(directory + file,'r', encoding='utf-8') as th_file:
                    text = str(th_file.read())
                    body.append((text,label))
        return body
