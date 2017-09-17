from Database import Database
from RedditObjects import Submission

from nltk.tokenize import word_tokenize

class Labels(Database):
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

class LabelMaker(Labels):
    def __init__(self,submis=None):
        self.submis = submis

    def create(self):
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
