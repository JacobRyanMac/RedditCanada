from Canada import Database, Query
import sqlite3



# I think this is suppose to be a reddit submission
# be clear what the difference is between a submission found on reddit and the ones used in the database
# they have the same properties but different names for them.
class Submission(object):
    def __init__(self,submis=None):
        self.submis = submis
        if self.submis is not None:
            self.id = submis.id
            self.author = submis.author.name
            self.subreddit = submis.subreddit_name_prefixed[2:]
            self.title = submis.title
            self.ups = submis.ups
            self.ratio = submis.upovte_ratio
            self.comments = submis.num_comments
            self.reports = submis.num_reports()
            self.pemalink = submis.permalink
            self.domain = submis.domain
            self.locked = submis.locked
            self.created = submis.created
        self.label = None

class SubmissionQuery(Submission,Query):
    def __init__(self,submis):
        # super(SubmissionQuery,self).__init__()
        self.id = submis.id
        self.author = submis.author.name
        self.title = submis.title
        self.ups = str(submis.ups)
        self.ratio = str(submis.upovte_ratio))
        self.comments = str(submis.num_comments)
        self.reports = str(submis.num_reports)
        self.pemalink = str(submis.permalink)
        self.domain = str(submis.domain)
        self.locked = str(submis.locked)

    def insert(self):
        if self.author is None:
            self.author = 'None'
        self.created = datetime.fromtimestamp(
            cur_submis.created,
            tz=timezone('US/Eastern')).strftime("%Y-%m-%d")

        if insert:
            submis_title = self.addquote(cur_submis.title)
            submis_label = self.label
            query = "INSERT INTO submissions VALUES (" + \
            "'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                cur_submis.id,
                sauth,
                cur_submis.subreddit_name_prefixed[2:],
                submis_title,
                str(cur_submis.ups),
                str(cur_submis.upvote_ratio),
                str(cur_submis.score),
                str(cur_submis.num_comments),
                str(cur_submis.num_reports),
                str(cur_submis.permalink),
                str(cur_submis.domain),
                str(cur_submis.locked),
                s_created,
                submis_label)

class SubmissionInsert(SubmissionQuery):
    pass

class SubmissionUpdate(SubmissionQuery):
    pass


    def insert_update(self):

        cur_submis = self.submis

        if cur_submis.author  is None:
            sauth = 'None'
        else:
            sauth = cur_submis.author.name
        s_created = datetime.fromtimestamp(
            cur_submis.created,
            tz=timezone('US/Eastern')).strftime("%Y-%m-%d")
        if insert:
            submis_title = self.addquote(cur_submis.title)
            submis_label = self.label
            query = "INSERT INTO submissions VALUES (" + \
            "'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                cur_submis.id,
                sauth,
                cur_submis.subreddit_name_prefixed[2:],
                submis_title,
                str(cur_submis.ups),
                str(cur_submis.upvote_ratio),
                str(cur_submis.score),
                str(cur_submis.num_comments),
                str(cur_submis.num_reports),
                str(cur_submis.permalink),
                str(cur_submis.domain),
                str(cur_submis.locked),
                s_created,
                submis_label)
        else:
            query = "UPDATE submissions SET " + \
            "upvotes = '{}', ratio = '{}', score = '{}', comments = '{}', reports = '{}', locked = '{}' WHERE submission_id = '{}'".format(
                    str(cur_submis.ups),
                    str(cur_submis.upvote_ratio),
                    str(cur_submis.score),
                    str(cur_submis.num_comments),
                    str(cur_submis.num_reports),
                    str(cur_submis.locked),
                    cur_submis.id)
        return query
        pass

print(help(SubmissionQuery))


class Comment(object):
    pass

class CommentQuery(Comment):
    pass

class User():
    pass

class UserQuery(User, Submission,Comment):
    #from submissions
    def make_user_query(self, insert):
        entry = self.submis
        auth = entry.author.name
        if insert:
            query = "INSERT INTO users VALUES(" + \
                "'{}','None', 0, 1, 0, '{}')".format(
                auth,str(entry.score))
        else:
            if entry.author_flair_text is None:
                fl = 'None'
            else:
                fl = entry.author_flair_text
            query = "UPDATE users SET " + \
            "flair = '{}', ".format(fl) + \
            "num_of_submissions = num_of_submissions + 1, " + \
            "total_sub_score = total_sub_score + {} WHERE user_id = '{}'".format(
            str(entry.ups),auth)
        return query

    # From comments
    def make_user_query(self, insert):
        entry = self.comment
        auth = entry.author.name
        if insert:
            query = "INSERT INTO users VALUES(" + \
                "'{}','None', 0, 1, 0, '{}')".format(
                auth,str(entry.score))
        else:
            if entry.author_flair_text is None:
                fl = 'None'
            else:
                fl = entry.author_flair_text
            query = "UPDATE users SET " + \
            "flair = '{}', ".format(fl) + \
            "num_of_comments = num_of_comments + 1, " + \
            "total_com_score = total_com_score + {} WHERE user_id = '{}'".format(
            str(entry.ups),auth)
        return query
