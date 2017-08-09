import praw
import datetime, time
import sqlite3 as sql
from redditSQL import SQL_submission, SQL_comment

# Constants
whichDatabase = r'canada_subreddit.db'
whichSubreddit = 'canada'
scoreMin = 50
commentMin = 50
commentLimit = 100
commentThreshold = 0
days_back = 4
ext_to = datetime.datetime.now()
#ext_to = datetime.datetime(2017, 6, 7, 12, 0, 0, 0)
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
    db = sql.connect(whichDatabase)
    # if submis.score >= scoreMin or submis.num_comments >= commentMin:
    if submis.num_comments >= commentMin:
        # Enter submission:
        cur_submis = SQL_submission(submis)
        try:
            db.execute(cur_submis.make_submission_query(True))
            if submis.author is not None:
                db.execute(cur_submis.make_user_query(True))
        except sql.IntegrityError:
            db.execute(cur_submis.make_submission_query(False))
            if submis.author is not None:
                db.execute(cur_submis.make_user_query(False))
        db.commit()
        print("ID:", submis.id, "is added. Now inserting comments...")
        # Enter comment forest
        submis.comments.replace_more(limit=commentLimit, threshold=commentThreshold)
        for c in submis.comments.list():
            cur_comment = SQL_comment(c)
            try:
                db.execute(cur_comment.make_comment_query(True))
                if c.author is not None:
                    db.execute(cur_comment.make_user_query(True))
            except sql.IntegrityError as e:
                db.execute(cur_comment.make_comment_query(False))
                if c.author is not None:
                    db.execute(cur_comment.make_user_query(False))
            db.commit()
    db.close()
