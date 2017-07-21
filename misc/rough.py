import pandas as pd
import numpy as py
import sqlite3

db = sqlite3.connect(r"canada_subreddit.db")
cur = db.cursor()
cur.execute('''
SELECT s.label, s.title, s.domain, s.score, s.ratio, s.comments, c.*
FROM submissions as s, comments as c
WHERE s.submission_id = c.submission_id;
''')

all_comments_labeled = pd.DataFrame(
    columns=['label',
              'sub_title',
              'sub_domain',
              'sub_score',
              'sub_ratio',
              'sub_total_comments',
              'comment_id',
              'submission_id',
              'user_id',
              'user_flair',
              'upvotes',
              'controversiality',
              'gold',
              'depth',
              'parent_id',
              'created',
              'edited',
              'body',
              'deleted'])

for c in cur:
    all_comments_labeled.append(list(c))

db.close()
