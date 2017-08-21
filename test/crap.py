import sqlite3

db = sqlite3.connect('canada_subreddit.db')
statement = 'SELECT * FROM submissions WHERE submission_id = ?'
db.execute(statement,('6ppr',))
db.close()
