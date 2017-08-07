import sqlite3
from FeatureSet import Threads

submission_id = "6ehv49"
database = '../canada_subreddit_test.db'
thread_folder = 'threads/'

db = sqlite3.connect(database)
cur = db.cursor()
cur.execute('''
SELECT s.submission_id, s.label
FROM submissions as s
WHERE (s.label = "Internet"
OR s.label = "Housing"
OR s.label = "Pot")
AND s.created <= "2017-08-01"
AND s.created >= "2017-07-01";
''')
submissions = cur.fetchall()
db.close()

th = Threads(database)

for s in submissions:
    print(s[1],s[0],'is being added...')
    print('Currently:',submissions.index(s)+1,'of',len(submissions))
    folder = thread_folder + s[1] + '/'
    th.create_threads(s[0], folder)
