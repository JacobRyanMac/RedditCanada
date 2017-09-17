from Database import Database,Query

What does it do? mirrors the table in Database
Why would it change? because the database changed
Used to make queries
Do we only need the names associated with the tables in the submission


class SubmissionTable(Database):
	def __init__(self):
		columns={

		}

	submission_id=
	user_id'
	subreddit_id`	TEXT,
	title`	TEXT,
	upvotes`	INT,
	ratio`	DECIMAL(2,3),
	score`	INT,
	comments`	INT,
	reports`	INT,
	permalink`	TEXT,
	domain`	TEXT,
	locked`	BOOLEAN,
	created`	DATE,
	label`	TEXT,
    pass

class CommentTable(Database):
	comment_id`	TEXT NOT NULL,
	submission_id`	TEXT,
	user_id`	TEXT,
	user_flair`	TEXT,
	upvotes`	INT,
	controversiality`	INT,
	gold`	INT,
	depth`	INT,
	parent_id`	TEXT,
	created`	DATE,
    body`	TEXT,
	edited`	DATE,
	deleted`	INTEGER,
    pass

class UserTable(Database):
	user_id`	TEXT NOT NULL,
	flair`	TEXT,
	num_of_comments`	INTEGER,
	num_of_submissions`	INTEGER,
	total_com_score`	INTEGER,
	total_sub_score`	INTEGER,
    pass
