import sqlite3

from Database import Query
from Labels import LabelMaker

# Need a "fake" submission in order to work with redditSQL
class fakeSubmis:
    def __init__(self,name,domain):
        self.name = name
        self.domain = domain


whichDatabase = r"canada_subreddit.db"
db = Query(whichDatabase)

db.connect()

cur = db.cursor()
cur.execute('SELECT title, domain, submission_id FROM submissions')

lm = LabelMaker()
labels = []
for c in cur:
    fs = fakeSubmis(c[0],c[1])
    cur_label = lm.create(fs)
    labels.append((cur_label, c[2]))

cur.executemany("UPDATE submissions SET label = ? WHERE submission_id = ?", labels)
db.commit()

db.close()
