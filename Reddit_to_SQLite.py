import datetime
from redditETL import Transform
import praw
import sqlite3 as sql

# Constants
whichSubreddit = 'canada'
whichDatabase = '/Users/jacobmacdougall/canada/canada.db'
textDirectory = '/Users/jacobmacdougall/canada/submissions/'
scoreMin = 50
commentMin = 50
commentLimit = 100
commentThreshold = 0
days_back = 3
# ext_to = datetime.datetime.now()
# ext_from = ext_to - datetime.timedelta(days=days_back)
ext_to = datetime.datetime(2017, 6, 1, 12, 0, 0, 0)
ext_from = ext_to - datetime.timedelta(days=days_back)

reddit = praw.Reddit(user_agent='CanadaGather',
                     client_id='tuM5-a7hYWtsQw',
                     client_secret='m5IziOvCOw3-GqyhrePtSFnj858',
                     username='reddit_python_can',
                     password='hnasjss345oqkcnakHHKasd')
canada = reddit.subreddit(whichSubreddit)

allSubmissions = canada.submissions(int(ext_from.strftime('%s')), int(ext_to.strftime('%s')))
for submis in allSubmissions:
    db = sql.connect(whichDatabase)
    if submis.score >= scoreMin or submis.num_comments >= commentMin:
        try:
            db.execute(Transform.make_submission_query(submis, True))
            if submis.author is not None:
                db.execute(Transform.make_user_query(submis, True))
        except sql.IntegrityError:
            db.execute(Transform.make_submission_query(submis, False))
            if submis.author is not None:
                db.execute(Transform.make_user_query(submis, False))
        db.commit()
        print(submis.id + " has been inserted")
        submis.comments.replace_more(limit=commentLimit, threshold=commentThreshold)
        textfilename = textDirectory + str(submis.id) + '.txt'
        with open(textfilename, 'w', newline='') as file:
            for c in submis.comments.list():
                try:
                    db.execute(Transform.make_comment_query(c, True))
                    if c.author is not None:
                        db.execute(Transform.make_user_query(c, True))
                    file.write(c.body.encode('utf-8').decode('ascii', 'ignore'))
                except sql.IntegrityError as e:
                    db.execute(Transform.make_comment_query(c, False))
                    if c.author is not None:
                        db.execute(Transform.make_user_query(c, False))
                    file.write(c.body.encode('utf-8').decode('ascii', 'ignore'))
                db.commit()
        file.close()
    db.close()

db = sql.connect(whichDatabase)
db.execute("update comments set edited = NULL where edited = 'NULL';")
db.commit()
db.close()
