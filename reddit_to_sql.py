import datetime, time
from redditETL import Transform
import praw
import sqlite3 as sql

# Constants
whichSubreddit = 'canada'
# whichDatabase = '/Users/jacobmacdougall/canada/canada.db'
whichDatabase = r"C:\Users\jacob\Documents\Projects\canada\canada.db"
scoreMin = 50
commentMin = 50
commentLimit = 100
commentThreshold = 0
days_back = 5
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

allSubmissions = canada.submissions(int(time.mktime(ext_from.timetuple())), 
                                    int(time.mktime(ext_to.timetuple())))
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
        print(submis.id, " is inserted")
        submis.comments.replace_more(limit=commentLimit, threshold=commentThreshold)
        for c in submis.comments.list():
            try:
                db.execute(Transform.make_comment_query(c, True))
                if c.author is not None:
                    db.execute(Transform.make_user_query(c, True))
            except sql.IntegrityError as e:
                db.execute(Transform.make_comment_query(c, False))
                if c.author is not None:
                    db.execute(Transform.make_user_query(c, False))
            db.commit()
    db.close()

db = sql.connect(whichDatabase)
db.execute("update comments set edited = NULL where edited = 'NULL';")
db.commit()
db.close()
