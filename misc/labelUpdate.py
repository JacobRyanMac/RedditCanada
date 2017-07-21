import sqlite3
from redditETL import Label_maker as LM

labels = []
whichDatabase = '/Users/jacobmacdougall/canada/canada.db'
db = sqlite3.connect(whichDatabase)
cur = db.cursor()
cur.execute('select title, domain, submission_id from submissions')
for c in cur:
    cur_label = LM.make_label(c[0], c[1])
    labels.append((cur_label, c[2]))
cur.executemany("Update submissions set label = ? where submission_id = ?", labels)
# cur.execute("Update submissions set label = 'Terrorism' where submission_id = '6fam0t'")
db.commit()
db.close()
