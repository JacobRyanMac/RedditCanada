import sqlite3
import praw

# from Database import Database, Query


# I think this is suppose to be a reddit submission
# be clear what the difference is between a submission found on reddit and the ones used in the database
# they have the same properties but different names for them.
class Submission(object):
    def __init__(self,submission):
        self.submission = submission
        self.id = submission.id
        self.author = submission.author.name
        self.flair = str(submission.author_flair_text)
        self.subreddit_name = submission.subreddit_name_prefixed[2:]
        self.title = submission.title
        self.ups = int(submission.ups)
        self.ratio = float(submission.upvote_ratio)
        self.score = int(submission.score)
        self.num_comments = int(submission.num_comments)
        self.num_reports = submission.num_reports
        self.permalink = str(submission.permalink)
        self.domain = str(submission.domain)
        self.locked = int(submission.locked)
        self.created = submission.created
        self.label = None

class Comment(object):
    def __init__(self,comment):
        self.comment = comment
        self.submission = comment._submission
        self.id = str(comment.id)
        if comment.author is not None:
            self.author = comment.author.name
        else:
            self.author = None
        self.flair = str(comment.author_flair_text)
        self.ups = int(comment.ups)
        self.controversiality = int(comment.controversiality)
        self.gold = int(comment.gilded)
        self.depth = int(comment.depth)
        self.parent_id = comment.parent_id[3:]
        self.created = comment.created
        self.edited = comment.edited
        self.body = comment.body
        self.deleted = None
