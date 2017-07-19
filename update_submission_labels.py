import sqlite3
from redditSQL import SQL_submission

# Need a "fake" submission in order to work with redditSQL
class fakeSubmis:
    def __init__(self,name,domain):
        self.name = name
        self.domain = domain


whichDatabase = r"canada_subreddit.db"
db = sqlite3.connect(whichDatabase)
cur = db.cursor()
cur.execute('SELECT title, domain, submission_id FROM submissions')

labels = []
for c in cur:
    fs = fakeSubmis(c[0],c[1])
    rs = SQL_submission(fs)
    cur_label = rs.label
    labels.append((cur_label, c[2]))

cur.executemany("UPDATE submissions SET label = ? WHERE submission_id = ?", labels)
db.commit()
db.close()
