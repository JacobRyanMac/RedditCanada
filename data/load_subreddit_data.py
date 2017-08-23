from sys import argv
import praw
import sqlite3
import datetime, time

from Database import Query
from RedditQuery import SubmissionQuery, CommentQuery, UserQuery

# Constants
script, whichDatabase, days_back = argv

commentMin = 50
commentLimit = 100
commentThreshold = 0

ext_to = datetime.datetime.now()
ext_from = ext_to - datetime.timedelta(days=int(days_back))

# Connect to reddit
reddit = praw.Reddit(user_agent='CanadaGather',
                     client_id='tuM5-a7hYWtsQw',
                     client_secret='m5IziOvCOw3-GqyhrePtSFnj858',
                     username='reddit_python_can',
                     password='hnasjss345oqkcnakHHKasd')
canada = reddit.subreddit('canada')

# Extract submisions
allSubmissions = canada.submissions(int(time.mktime(ext_from.timetuple())),
                                    int(time.mktime(ext_to.timetuple())))
# Load the data into sqlite3ite
for submis in allSubmissions:
    db = Query(whichDatabase)
    db.connect()
    if submis.num_comments >= commentMin:
        # Enter submission:
        sq = SubmissionQuery(submis)
        try:
            db.execute(sq.insert())
        except sqlite3.IntegrityError:
            db.execute(sq.update())
        # Enter users:
        uq = UserQuery(submis)
        if uq.id is not None:
            try:
                db.execute(uq.insert())
            except sqlite3.IntegrityError:
                db.execute(uq.update())
            db.commit()
        print("ID:", submis.id, "is added. Now inserting comments...")

        # Enter comment forest
        submis.comments.replace_more(limit=commentLimit, threshold=commentThreshold)
        for c in submis.comments.list():
            # Comment:
            cq = CommentQuery(c)
            try:
                db.execute(cq.insert())
            except sqlite3.IntegrityError as e:
                db.execute(cq.update())
            # User:
            uq = UserQuery(c)
            if uq.id is not None:
                try:
                    db.execute(uq.insert())
                except sqlite3.IntegrityError as e:
                    db.execute(uq.update())
            db.commit()

    db.close()
