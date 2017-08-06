import sqlite3
import random
import nltk
from nltk import FreqDist
from nltk.tokenize import word_tokenize

class Features(object):
    """
    This object will hold a feature set that will be used to train classifiers.
    They are intiated with SQL statement that needs to have the following:
    SELECT c.body, s.label
    FROM comments as c, submissions as s
    The WHERE statement can be anything really.
    """
    def __init__(self, SQL_query, SQL_db):
        self.SQL_query = SQL_query
        self.SQL_db = SQL_db


    @staticmethod
    def find_features(body, feature_list):
        words = set(body)
        features = {}
        for w in feature_list:
            features[w] = (w in words)
        return features

    def make_featureset(self):
        db = sqlite3.connect(self.SQL_db)
        cur = db.cursor()
        cur.execute(self.SQL_query)
        comments = [(word_tokenize(c[0]), c[1]) for c in cur]
        db.close()

        random.shuffle(comments)
        all_words = []
        for c in comments:
            for w in c[0]:
                word = w
                if word[:2] != "//":
                    if '*' in word:
                        word = word.replace('*','')
                    all_words.append(word.lower())
        all_words = FreqDist(all_words)
        word_features = list(all_words.keys())[:4000]

        featuresets = []
        for (comment, label) in comments:
            featuresets.append((self.find_features(comment,word_features), label))

        return featuresets

class Threads(object):
    '''
    This file will create threads from a given database and put them in the
    given folder.
    '''
    def __init__(self,database,folder):
        self.database = database
        self.folder = folder

    def search_roots(self, cursor,p_id,thread_file):
        cursor.execute('SELECT body, comment_id  FROM comments WHERE parent_id = ?',(p_id,))
        children = cursor.fetchall()
        for c in children:
            thread_file.write(c[0] + '\n')
            self.search_roots(cursor,c[1], thread_file)

    def make_thread(self,submission):
        db = sqlite3.connect(self.database)
        cur = db.cursor()
        cur.execute('''
        SELECT c.comment_id, c.body, s.label
        FROM comments as c, submissions as s
        WHERE c.submission_id = s.submission_id
        AND c.parent_id = ?
        ''',(submission,))
        parents = cur.fetchall()
        for p in parents:
            file_name = self.folder + p[2] + '_' + p[0] + ".txt"
            with open(file_name,"w") as file:
                file.write(p[1] + '\n')
                self.search_roots(cur,p[0], file)
                file.close
        db.commit()
        db.close()
