#==============================================================================
# Code by Jacob MacDougall
#
# This class is used to make queries for SQLite databases.
# They are to be used the comment and submission object found in the
# praw module.
#==============================================================================

import os
import sqlite3
import random
import nltk

from datetime import datetime
from pytz import timezone

from nltk import FreqDist
from nltk.tokenize import word_tokenize


class SQL_submission(object):
    """
    NOTE:
    The function make_label() is specific only to the Canada subreddit.
    The only purpose is to automate the creation of labels for each submission
    These labels are used in classification ML programs.
    It is NOT a ML program at all. It's purpose is to help me label the
    submissions that come in. A lot of the labels are actually too general
    (e.g. News, Politics, Fluff) and will require human intuition
    in order to come up with a more proper label.
    It's basically just me saving time.
    """
    # Labels:
    politics = "Politics"
    terrorism = "Terrorism"
    climate = "Climate"
    economy = "Economy"
    marijuana = "Pot"
    health = "Health"
    housing = "Housing"
    internet = "Internet"
    fluff = "Fluff"
    islam = "Islam"
    news = "News"
    self_post = "Self-post"
    other = "Other"
    # Words:
    politics_list = ["trudeau", "trump", "bernier", "couillard",
                     "scheer", "wynne", "obama", "layton", "leary",
                     "minister", "mp", "mps", "premier",
                     "tax", "taxes", "hst", "taxpayers", "gst",
                     "vote", "voting",
                     "illegal",
                     "liberals", "NDP", "Conversative",
                     "parliament", "law", "bill",
                     "elections"]
    terrorism_list = ["gun", "attack", "attacker", "terrorism",
                      "archibald","islam", "muslism", "mosque", "allah", "sharia", "syria",
                                    "syrian","imam"]
    islam_list = []
    climate_list = ["climate", "paris"]
    economy_list = ["wage", "job",
                    "economy", "economic", "gdp",
                    "investors", "financial"]
    marijuana_list = ["pot", "weed", "marijuana", "legalization", "cannabis"]
    health_list = ["junk-food",
                   "mdma", "cocaine", "fentanyl", "heroin", "drugs",
                   "cancer"]
    housing_list = ["house", "housing", "home",
                    "homeowner", "homeowners", "estate"]
    internet_list = ["bell", "rogers", "telus",
                     "telecommunicaions", "telecomm", "crtc",
                     "cellular", "cell", "phone", "cellphone",
                     "net", "data"]
    # Domains
    news_domain = ["cbc.ca", "canada.ca", "news.nationalpost.com",
                   "globalnews.ca", "thestar.com", "statcan.gc.ca",
                   "nbcnews.com", "theglobeandmail.com", "macleans.ca",
                   "thestar.com", "ctvnews.ca"]
    economy_domain = ["business.financialpost.com", "financialpost.com"]
    fluff_domain = ["i.redd.it", "i.imgur.com", "twitter.com",
                    "imgur.com",
                    "en.wikipedia.org", "junobeach.org"]
    self_domain = ["self.canada"]


    def __init__(self, submis, label=None):
        self.submis = submis
        self.label = self.make_label()

    def make_label(self):
        name = self.submis.name
        domain = self.submis.domain
        title = word_tokenize(name)
        label = ""
        for w in title:
            word = w.lower()
            # Terrorism
            if word in self.islam_list:
                label = self.islam
            elif word in self.terrorism_list:
                label = self.terrorism
            # Pot
            elif word in self.marijuana_list:
                label = self.marijuana
            # Climate
            elif word in self.climate_list \
                    and label != self.marijuana \
                    and label != self.islam \
                    and label != self.terrorism:
                label = self.climate
            # Housing
            elif word in self.housing_list \
                    and label != self.marijuana \
                    and label != self.islam \
                    and label != self.terrorism:
                label = self.housing
            # Internet
            elif word in self.internet_list \
                    and label != self.marijuana \
                    and label != self.islam \
                    and label != self.terrorism:
                label = self.internet
            # Health
            elif word in self.health_list \
                    and label != self.marijuana \
                    and label != self.islam \
                    and label != self.terrorism:
                label = self.health
            # Economy
            elif word in self.economy_list \
                    and label != self.internet \
                    and label != self.housing \
                    and label != self.marijuana \
                    and label != self.climate \
                    and label != self.terrorism \
                    and label != self.islam \
                    and label != self.health:
                label = self.economy
            # Politics
            elif word in self.politics_list \
                    and label != self.internet \
                    and label != self.housing \
                    and label != self.marijuana \
                    and label != self.climate \
                    and label != self.terrorism \
                    and label != self.islam \
                    and label != self.health:
                label = self.politics
        if label == "":
            if domain in self.news_domain:
                label = self.news
            elif domain in self.economy_domain:
                label = self.economy
            elif domain in self.fluff_domain:
                label = self.fluff
            elif domain in self.self_domain:
                label = self.self_post
            else:
                label = self.other
        return label

    @staticmethod
    def addquote(s):
        ls = list(s)
        i = 0
        for k in ls:
            if k == '\'':
                ls[i] = '\'\''
            i += 1
        k = "".join(ls)
        return k

    def make_submission_query(self, insert):
        cur_submis = self.submis
        if cur_submis.author is None:
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
            query = '''
            UPDATE submissions
            SET upvotes = ,
            ratio = "{}",
            score = "{}",
            comments = "{}",
            reports = "{}",
            locked = "{}"
            WHERE submission_id = "{}"
            '''.format(
                    str(cur_submis.ups),
                    str(cur_submis.upvote_ratio),
                    str(cur_submis.score),
                    str(cur_submis.num_comments),
                    str(cur_submis.num_reports),
                    str(cur_submis.locked),
                    cur_submis.id)
        return query


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


class SQL_comment(object):
    def __init__(self,comment):
        self.comment = comment

    @staticmethod
    def addquote(s):
        ls = list(s)
        i = 0
        for k in ls:
            if k == '\'':
                ls[i] = '\'\''
            i += 1
        k = "".join(ls)
        return k

    def make_comment_query(self, insert):
        comment = self.comment
        # Author:
        if comment.author is None:
            cauth = 'None'
        else:
            cauth = comment.author.name
        # Edited:
        if not comment.edited:
            cedit = str(0)
        else:
            cedit = str(1)
        # Deleted:
        if comment.body == '[removed]' or comment.body == '[deleted]':
            comDel = str(1)
        else:
            comDel = str(0)
        # Created:
        comCreated = datetime.fromtimestamp(
            comment.created, tz=timezone('US/Eastern')).strftime("%Y-%m-%d")
        if insert:
            query = "INSERT INTO comments VALUES ("+ \
            "'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                comment.id,
                str(comment._submission),
                cauth,
                str(comment.author_flair_css_class),
                str(comment.ups),
                str(comment.controversiality),
                str(comment.gilded),
                str(comment.depth),
                comment.parent_id[3:],
                comCreated,
                cedit,
                self.addquote(comment.body),
                comDel)
        elif comDel == "1":
            query = "UPDATE comments SET " + \
            " upvotes = '{}', controversiality = '{}', gold = '{}', edited = '{}', deleted = '{}' WHERE comment_id = '{}'".format(
                str(comment.ups),
                str(comment.controversiality),
                str(comment.gilded),
                cedit,
                comDel,
                str(comment.id))
        else:
            query = "UPDATE comments SET " + \
            "body = '{}', upvotes = '{}', controversiality = '{}', gold = '{}', edited = '{}', deleted = '{}' WHERE comment_id = '{}'".format(
                self.addquote(comment.body),
                str(comment.ups),
                str(comment.controversiality),
                str(comment.gilded),
                cedit,
                comDel,
                str(comment.id))
        return query

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


class Features(object):
    """
    This object create feature sets that will be used to train classifiers.
    Body must be of a list of tuples.
    Each tuple will be a string of text of any length and a label
    Example:
        [("this is an example", Internet),
         ("strings can be threads or comments!", Housing)]

    This method can create bodies if given a SQL statement with the form:
    SELECT c.body, s.label
    FROM comments as c, submissions as s
    """
    def __init__(self, SQL_query=None, SQL_db=None, body=None):
        self.body = body
        self.SQL_query = SQL_query
        self.SQL_db = SQL_db
        if self.body is None and SQL_query is not None:
            self.query_body()

    def query_body(self):
        db = sqlite3.connect(self.SQL_db)
        cur = db.cursor()
        cur.execute(self.SQL_query)
        body = [(c[0], c[1]) for c in cur]
        db.close()
        self.body = body

    def make_featureset(self):
        token_body = [(word_tokenize(b),l) for (b,l) in self.body]
        random.shuffle(token_body)
        all_words = []
        for c in token_body:
            for w in c[0]:
                word = w
                if word[:2] != "//":
                    if '*' in word:
                        word = word.replace('*','')
                    all_words.append(word.lower())
        all_words = FreqDist(all_words)
        word_features = list(all_words.keys())[:3000]
        featuresets = []
        for (words, label) in token_body:
            featuresets.append((self.find_features(words,word_features), label))
        return featuresets

    @staticmethod
    def find_features(body, feature_list):
        words = set(body)
        features = {}
        for w in feature_list:
            features[w] = (w in words)
        return features


class Threads(object):
    '''
    Object to create and transfer threads with
    '''
    def __init__(self,SQL_db=None):
        self.SQL_db = SQL_db

    def search_roots(self,cursor,p_id,thread_file):
        cursor.execute('SELECT body, comment_id FROM comments WHERE parent_id = ?',(p_id,))
        children = cursor.fetchall()
        for c in children:
            thread_file.write(c[0] + '\n')
            self.search_roots(cursor,c[1], thread_file)

    def create_threads(self,submission,folder):
        db = sqlite3.connect(self.SQL_db)
        cur = db.cursor()
        cur.execute('''
        SELECT c.comment_id, c.body
        FROM comments as c, submissions as s
        WHERE c.submission_id = s.submission_id
        AND c.parent_id = ?
        ''',(submission,))

        parents = cur.fetchall()
        for p in parents:
            file_name = folder + p[0] + ".txt"
            with open(file_name,"w", encoding='utf-8', newline='') as file:
                file.write(p[1])
                self.search_roots(cur,p[0],file)
                file.close

        db.commit()
        db.close()

    def make_body(self,labels,folder):
        body = []
        for label in labels:
            directory = os.fsencode(folder.encode('utf-8') + label.encode('utf-8') +b'/')
            for file in os.listdir(directory):
                with open(directory + file,'r', encoding='utf-8') as th_file:
                    text = str(th_file.read())
                    body.append((text,label))
        return body
