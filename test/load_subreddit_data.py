import praw
import datetime, time
import sqlite3 as sql

from Database import Query
from Query import SubmissionQuery, CommentQuery, UserQuery

# Constants
whichDatabase = r'canada_subreddit.db'
whichSubreddit = 'canada'
commentMin = 50
commentLimit = 100
commentThreshold = 0
days_back = 3
ext_to = datetime.datetime.now()
ext_from = ext_to - datetime.timedelta(days=days_back)

# Connect to reddit
reddit = praw.Reddit(user_agent='CanadaGather',
                     client_id='tuM5-a7hYWtsQw',
                     client_secret='m5IziOvCOw3-GqyhrePtSFnj858',
                     username='reddit_python_can',
                     password='hnasjss345oqkcnakHHKasd')
canada = reddit.subreddit(whichSubreddit)

# Extract submisions
allSubmissions = canada.submissions(int(time.mktime(ext_from.timetuple())),
                                    int(time.mktime(ext_to.timetuple())))

# Load the data into SQLite
for submis in allSubmissions:
    db = Query(whichDatabase)
    db.connect()
    if submis.num_comments >= commentMin:
        # Enter submission:
        sq = SubmissionQuery(submis)
        try:
            db.execute(sq.insert())
        except sql.IntegrityError:
            db.execute(sq.update())
        # Enter users:
        uq = UserQuery(submis)
        if uq.id is not None:
            try:
                db.execute(uq.insert())
            except sql.IntegrityError:
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
            except sql.IntegrityError as e:
                db.execute(cq.update())
            # User:
            uq = UserQuery(c)
            if uq.id is not None:
                try:
                    db.execute(uq.insert())
                except sql.IntegrityError as e:
                    db.execute(uq.update())
            db.commit()

    db.close()
