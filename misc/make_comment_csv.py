import sqlite3
import csv

# from nltk.tokenize import wordpunct_tokenize
# wordpunct_tokenize(s)

db = sqlite3.connect(r"canada_subreddit.db")
cur = db.cursor()
cur.execute('''
SELECT s.label, s.title, s.domain, s.score, s.ratio, s.comments, c.*
FROM submissions as s, comments as c
WHERE s.submission_id = c.submission_id;
''')

with open('comments_labeled.csv', 'w', newline='', encoding='utf-8') as file:
    tsvfile = csv.writer(file, delimiter='\t')
    tsvfile.writerow(['label',
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
    tsvfile.writerows(c for c in cur)
file.close()
db.close()
