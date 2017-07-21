import sqlite3
from nltk.tokenize import word_tokenize

# Labels:
politics = "Politics"
terrorism = "terrorism"
economy = "economy"
marijuana = "pot"
health = "health"
housing = "housing"
internet = "internet"
fluff = "fluff"
news = "NEWS"
self_post = "self-post"
other = "other"
# Words:
politics_list = ["trudeau", "trump", "bernier", "couillard", "scheer", "wynne", "obama"
                 "bill", "minister", "mp", "mps", "premier"
                 "tax", "taxes", "hst", "taxpayers",
                 "vote", "voting",
                 "liberals", "NDP", "Conversative",
                 "parliament", "law",
                 "elections"]
terrorism_list = ["islam", "muslism", "mosque", "allah", "sharia", "syria", "syrian",
                  "gun", "attack", "attacker", "attacks", "terrorism"]
economy_list = ["wage", "economy", "economic", "investors", "financial", "gdp"]
housing_list = ["housing", "home", "homeowner", "homeowners", "estate"]
internet_list = ["bell", "rogers", "telus",
                 "telecommunicaions", "telecomm",
                 "cellular", "cell", "phone", "cellphone",
                 "net", "data"]
health_list = ["junk-food", "MDMA", "cancer"]
marijuana_list = ["pot", "weed", "marijuana", "legalization"]
# Domains
news_domain = ["cbc.ca", "canada.ca", "news.nationalpost.com",
               "globalnews.ca", "thestar.com", "statcan.gc.ca",
               "nbcnews.com", "theglobeandmail.com", "macleans.ca",
               "thestar.com", "ctvnews.ca"]
economy_domain = ["business.financialpost.com", "financialpost.com"]
fluff_domain = ["i.redd.it", "i.imgur.com", "en.wikipedia.org"]
self_domain = ["self.canada"]

labels = []
whichDatabase = '/Users/jacobmacdougall/canada/canada.db'
db = sqlite3.connect(whichDatabase)
cur = db.cursor()
cur.execute('select title, domain, submission_id from submissions')
for c in cur:
    title = word_tokenize(c[0])
    cur_label = ""
    for w in title:
        word = w.lower()
        # Terrorism
        if word in terrorism_list:
            cur_label = terrorism
        # Politics
        elif word in politics_list \
                and (cur_label != terrorism) \
                and (cur_label != marijuana):
            cur_label = politics
        # Housing
        elif word in housing_list \
                and cur_label != marijuana:
            cur_label = housing
        # Internet
        elif word in internet_list \
                and cur_label != marijuana:
            cur_label = internet
        # Economy
        elif word in economy_list \
                and cur_label != internet \
                and cur_label != housing \
                and cur_label != marijuana:
            cur_label = economy
        # Pot
        elif word in marijuana_list:
            cur_label = marijuana
        # Health
        elif word in health_list:
            cur_label = health
    domain = c[1]
    if cur_label == "":
        if domain in news_domain:
            cur_label = news
        elif domain in economy_domain:
            cur_label = economy
        elif domain in fluff_domain:
            cur_label = fluff
        elif domain in self_domain:
            cur_label = self_post
        else:
            cur_label = other
    labels.append((cur_label, c[2]))
cur.executemany("Update submissions set label = ? where submission_id = ?", labels)
db.commit()
db.close()
