import praw
from datetime import datetime
from pytz import timezone
from nltk.tokenize import word_tokenize


class Label_maker(object):
    """
    Label are used in machine learning in conjunction with features.
    The point of the Label_maker class is to create labels for submissions.
    Label are based off the title of submission as well as the domain of link
    There is a hierarchy to label. For example, while housing is part of the economy,
    if a submission is specific to the housing market it will focus on that part.
    Labels are based on recognized key words, that are stored in the global constants below.
    This is not machine learning, in fact it's the opposite
    It is a form of feature engineering in which I am trying to make a label.

    - Label_maker is a function that takes in the title and domain of a submission and returns a label that relates to it
    - This is not a form of machine learning, but is a manual feature engineering
    - Supervised learning as there must be some indication of how submissions will differ from one another.
    """
    # Labels:
    politics = "Politics"
    terrorism = "Terrorism"
    climate = "Climate"
    economy = "Economy"
    marijuana = "Marijuana"
    health = "Health"
    housing = "Housing"
    internet = "Internet"
    fluff = "Fluff"
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
    terrorism_list = ["islam", "muslism", "mosque", "allah", "sharia", "syria", "syrian",
                      "gun", "attack", "attacker", "attacks", "terrorism",
                      "archibald"]
    climate_list = ["climate", "paris"]
    economy_list = ["wage", "job",
                    "economy", "economic", "gdp",
                    "investors", "financial"]
    marijuana_list = ["pot", "weed", "marijuana", "legalization", "cannabis"]
    health_list = ["junk-food",
                   "mdma", "cocaine", "fentanyl", "heroin", "drugs",
                   "cancer"]
    housing_list = ["house","housing", "home",
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
                    "en.wikipedia.org", "junobeach.org"]
    self_domain = ["self.canada"]

    @staticmethod
    def make_label(name, domain):
        title = word_tokenize(name)
        label = ""
        for w in title:
            word = w.lower()
            # Terrorism
            if word in Label_maker.terrorism_list:
                label = Label_maker.terrorism
            # Climate
            elif word in Label_maker.climate_list \
                    and label != Label_maker.marijuana:
                label = Label_maker.climate
            # Pot
            elif word in Label_maker.marijuana_list:
                label = Label_maker.marijuana
            # Housing
            elif word in Label_maker.housing_list \
                    and label != Label_maker.marijuana:
                label = Label_maker.housing
            # Internet
            elif word in Label_maker.internet_list \
                    and label != Label_maker.marijuana:
                label = Label_maker.internet
            # Health
            elif word in Label_maker.health_list \
                    and label != Label_maker.marijuana:
                label = Label_maker.health
            # Economy
            elif word in Label_maker.economy_list \
                    and label != Label_maker.internet \
                    and label != Label_maker.housing \
                    and label != Label_maker.marijuana \
                    and label != Label_maker.climate \
                    and label != Label_maker.health:
                label = Label_maker.economy
            # Politics
            elif word in Label_maker.politics_list \
                    and label != Label_maker.internet \
                    and label != Label_maker.terrorism \
                    and label != Label_maker.marijuana \
                    and label != Label_maker.climate \
                    and label != Label_maker.health:
                label = Label_maker.politics
        if label == "":
            if domain in Label_maker.news_domain:
                label = Label_maker.news
            elif domain in Label_maker.economy_domain:
                label = Label_maker.economy
            elif domain in Label_maker.fluff_domain:
                label = Label_maker.fluff
            elif domain in Label_maker.self_domain:
                label = Label_maker.self_post
            else:
                label = Label_maker.other
        return label


class Transform(Label_maker):
    """
    This class is used as a way to connect reddit to a SQLite server.
    This code is specific to a particular SQL schema
    It assumes that all scripts containing this class will also be using the praw class,
    as most of the arguements given to the staticmethods use objects from that module.
    """
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

    @staticmethod
    def make_submission_query(submis, insert=True):
        if submis.author is None:
            sauth = 'None'
        else:
            sauth = submis.author.name
        s_created = datetime.fromtimestamp(
            submis.created,
            tz=timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")
        if insert:
            submis_title = Transform.addquote(submis.title)
            submis_label = Label_maker.make_label(submis_title, str(submis.domain))
            query = "INSERT INTO submissions VALUES ('" + \
                submis.id + "', '" + \
                sauth + "', '" + \
                submis.subreddit_name_prefixed[2:] + "', '" + \
                submis_title + "', '" + \
                str(submis.ups) + "', '" + \
                str(submis.upvote_ratio) + "', '" + \
                str(submis.score) + "', '" + \
                str(submis.num_comments) + "', '" + \
                str(submis.num_reports) + "', '" + \
                str(submis.permalink) + "', '" + \
                str(submis.domain) + "', '" + \
                str(submis.locked) + "', '" + \
                s_created + "', '" + \
                submis_label + "')"
        else:
            query = "UPDATE submissions SET" + \
                    " upvotes = '" + str(submis.ups) + \
                    "', ratio = '" + str(submis.upvote_ratio) + \
                    "', score = '" + str(submis.score) + \
                    "', comments = '" + str(submis.num_comments) + \
                    "', reports = '" + str(submis.num_reports) + \
                    "', locked = '" + str(submis.locked) + \
                    "' WHERE submission_id = '" + submis.id + "'"
        return query

    @staticmethod
    def make_comment_query(comment, insert=True):
        if comment.author is None:
            cauth = 'None'
        else:
            cauth = comment.author.name
        if not comment.edited:
            cedit = 'NULL'
        else:
            cedit = datetime.fromtimestamp(
                comment.edited,
                tz=timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")
        comCreated = datetime.fromtimestamp(
            comment.created,
            tz=timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")
        if insert:
            query = "INSERT INTO comments VALUES ('" + \
                comment.id + "', '" + \
                str(comment._submission) + "', '" + \
                cauth + "', '" + \
                str(comment.author_flair_css_class) + "', '" + \
                str(comment.ups) + "', '" + \
                str(comment.controversiality) + "', '" + \
                str(comment.gilded) + "', '" + \
                str(comment.depth) + "', '" + \
                comment.parent_id[3:] + "', '" + \
                comCreated + "', '" + \
                cedit + "', '" + \
                Transform.addquote(comment.body) + \
                "', '0')"
        elif comment.body == '[removed]' or comment.body == '[deleted]':
            query = "UPDATE comments SET" + \
                " upvotes = '" + str(comment.ups) + \
                "', controversiality = '" + str(comment.controversiality) +\
                "', gold = '" + str(comment.gilded) + \
                "', edited = '" + cedit + \
                "', deleted = '" + str(1) + \
                "' WHERE comment_id = '" + str(comment.id) + "'"
        else:
            query = "UPDATE comments SET" + \
                " upvotes = '" + str(comment.ups) + \
                "', controversiality = '" + str(comment.controversiality) + \
                "', gold = '" + str(comment.gilded) + \
                "', edited = '" + cedit + \
                "' WHERE comment_id = '" + str(comment.id) + "'"
        return query

    @staticmethod
    def make_user_query(entry, insert=False):
        if type(entry) == praw.models.reddit.submission.Submission:
            auth = entry.author.name
            if insert:
                query = "INSERT INTO users VALUES('" + \
                    auth + "','None', 0, 1, 0, " + \
                    str(entry.score) + ")"
            elif not insert:
                if entry.author_flair_text is None:
                    fl = 'None'
                else:
                    fl = entry.author_flair_text
                query = "UPDATE users SET " + \
                    "flair = '" + fl + "'," + \
                    "num_of_submissions = num_of_submissions + 1," + \
                    "total_sub_score = total_sub_score + " + str(entry.score) + \
                    " WHERE user_id = '" + auth + "'"
        elif type(entry) == praw.models.reddit.comment.Comment:
            auth = entry.author.name
            if insert:
                query = "INSERT INTO users VALUES('" + \
                    auth + "','None', 1, 0, " + \
                    str(entry.ups) + ", 0)"
            elif not insert:
                if entry.author_flair_text is None:
                    fl = 'None'
                else:
                    fl = entry.author_flair_text
                query = "UPDATE users SET " + \
                    "flair = '" + fl + "'," + \
                    "num_of_comments = num_of_comments + 1," + \
                    "total_com_score = total_com_score + " + str(entry.ups) + \
                    " WHERE user_id = '" + auth + "'"
        return query


class Load(Transform):
    """docstring for Load"""
    pass
