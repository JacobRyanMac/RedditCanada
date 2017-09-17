import random
import nltk

import sqlite3

from datetime import datetime
from pytz import timezone

from Database import Query
from RedditObjects import Submission,Comment
from Labels import LabelMaker

import praw.models.reddit

class CommentQuery(Comment,Query):
    def __init__(self,comment):
        super(CommentQuery,self).__init__(comment)
        if self.author is None:
            self.author = 'None'
        if not self.edited:
            self.edited = str(0)
        else:
            self.edited = str(1)
        if self.body == '[removed]' or self.body == '[deleted]':
            self.deleted = str(1)
        else:
            self.deleted = str(0)
        self.created = datetime.fromtimestamp(
            self.created, tz=timezone('US/Eastern')).strftime("%Y-%m-%d")
        self.body = Query.addquote(self.body)

    def __repr__(self):
        return self.submissionself.body

    def insert(self):
        query = '''
        INSERT INTO comments
        VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
        '''.format(
            self.id,
            self.submission,
            self.author,
            self.flair,
            self.ups,
            self.controversiality,
            self.gold,
            self.depth,
            self.parent_id,
            self.created,
            self.edited,
            self.body,
            self.deleted)
        return query

    def update(self):
        if self.deleted:
            query = '''
            UPDATE comments
            SET body = '{}',
            upvotes = '{}',
            controversiality = '{}',
            gold = '{}',
            edited = '{}',
            deleted = '{}'
            WHERE comment_id = '{}'
            '''.format(
            self.body,
            self.ups,
            self.controversiality,
            self.gold,
            self.edited,
            self.deleted,
            self.id)
        else:
            query = '''
            UPDATE comments
            SET upvotes = '{}',
            controversiality = '{}',
            gold = '{}',
            edited = '{}',
            deleted = '{}'
            WHERE comment_id = '{}'
            '''.format(
            self.upvotes,
            self.controversiality,
            self.gold,
            self.edited,
            self.deleted,
            self.id)
        return query

class SubmissionQuery(Submission,Query):
    def __init__(self,submission):
        super(SubmissionQuery,self).__init__(submission)
        if self.author is None:
            self.author = 'None'
        self.title = Query.addquote(self.title)
        self.label = LabelMaker().create(self.submission)
        self.created = datetime.fromtimestamp(
            self.created, tz=timezone('US/Eastern')).strftime("%Y-%m-%d")

    def __repr__(self):
        return self.title

    def insert(self):
        query = '''
        INSERT INTO submissions
        VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
        '''.format(
            self.id,
            self.author,
            self.subreddit_name,
            self.title,
            self.ups,
            self.ratio,
            self.score,
            self.num_comments,
            self.num_reports,
            self.permalink,
            self.domain,
            self.locked,
            self.created,
            self.label)
        return query

    def update(self):
        query = '''
        UPDATE submissions
        SET upvotes = '{}',
        ratio = '{}',
        score = '{}',
        comments = '{}',
        reports = '{}',
        locked = '{}'
        WHERE submission_id = '{}'
        '''.format(
                self.ups,
                self.ratio,
                self.score,
                self.num_comments,
                self.num_reports,
                self.locked,
                self.id)
        return query

class UserQuery(Submission, Comment, Query):
    def __init__(self,entry):
        self.entry = entry
        if entry.author is not None:
            self.id = entry.author.name
        else:
            self.id = None
        self.flair = entry.author_flair_text
        self.ups = entry.ups

    def __repr__(self):
        return self.entry.author.name

    def insert(self):
        if type(self.entry) is praw.models.reddit.submission.Submission:
            values = "('{}','{}','0','1','0','{}')".format(
                self.id, self.flair, self.ups)
        elif type(self.entry) is praw.models.reddit.comment.Comment:
            values = "('{}','{}','1','0','{}','0')".format(
                self.id, self.flair, self.ups)
        query = 'INSERT INTO users VALUES {}'.format(values)
        return query

    def update(self):
        num_c, num_s, total_c, total_s = 0,0,0,0
        if type(self.entry) is praw.models.reddit.submission.Submission:
            num_s = 1
            total_s = self.ups
        elif type(self.entry) is praw.models.reddit.comment.Comment:
            num_c = 1
            total_c = self.ups
        query = '''
        UPDATE users
        SET flair = '{}',
        num_of_comments = num_of_comments + {},
        num_of_submissions = num_of_submissions + {},
        total_com_score = total_com_score + {},
        total_sub_score = total_sub_score + {}
        WHERE user_id = '{}'
        '''.format(
        self.flair,
        num_c,
        num_s,
        total_c,
        total_s,
        self.id)
        return query
