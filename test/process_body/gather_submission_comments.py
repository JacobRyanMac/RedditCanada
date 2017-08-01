from pprint import pprint
import sqlite3
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

sub_ID = '6e7kr0'
# ID = input("submission_id:")
stop_words = set(stopwords.words("english"))
stop_words.update(['.', ',', '"', "'", '?', '!',
                   '>', "\'\'", "``", "...",
                   ':', ';', '(', ')', '[', ']', '{', '}'])

db = sqlite3.connect(r'../canada_subreddit_test.db')
cur = db.cursor()
cur.execute('''
SELECT c.body
FROM submissions as s, comments as c
WHERE s.submission_id = c.submission_id
AND s.submission_id = ?
''', (sub_ID,))

all_comments = []
for c in cur:
    all_comments.extend(word_tokenize(c[0]))
filterwords = [w for w in all_comments if not w in stop_words]

fd = FreqDist(filterwords)

db.close()
