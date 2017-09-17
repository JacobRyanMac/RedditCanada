import sqlite3
import pickle
from pprint import pprint

from redditSQL import Features

pickle_file = "naivebayes_comments.pickle"
# pickle_file = "naivebayes_threads.pickle"
database = 'canada_subreddit.db'
SQL_query = '''
SELECT c.body, s.label
FROM comments as c, submissions as s
WHERE s.submission_id = c.submission_id
AND s.created <= "2017-08-01"
AND s.created >= "2017-07-27"
AND (s.label = "Climate"
OR s.label = "Housing");
'''

fs = Features(SQL_query,database)
featuresets = fs.make_featureset()

with open(pickle_file,"rb") as file:
    classifier = pickle.load(file)

counter = 0
for f in featuresets:
    guess = classifier.classify(f[0])
    # print('Label:',f[1])
    # print('Guess:',guess)
    if guess == f[1]:
        counter += 1

print(len(featuresets))
print(str(counter))
