import os
import sqlite3
import random
import nltk

from datetime import datetime
from pytz import timezone

from nltk import FreqDist
from nltk.tokenize import word_tokenize


class Database(object):
    def __init__(self,directory=None):
        self.directory = directory
        self.database = None

    def connect(self):
        self.database = sqlite3.connect(self.directory)

    def close(self):
        self.database.close()
        self.database = None

    def commit(self):
        self.database.commit()

    def cursor(self):
        return self.database.cursor()

class Query(Database):
    def __init__(self,directory):
        super(Query,self).__init__(directory)

    def execute(self,statement,variables=None):
        if variables is None:
            self.database.execute(statement)
        else:
            self.database.execute(statement,variables)

    @staticmethod
    def addquote(s):
        ls = list(s)
        i = 0
        for k in ls:
            if k == '\'':
                ls[i] = '\'\''
            i += 1
        k = "".join(ls)
        return k
