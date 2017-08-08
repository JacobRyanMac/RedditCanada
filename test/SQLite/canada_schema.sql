BEGIN TRANSACTION;
CREATE TABLE "users" (
	`user_id`	TEXT NOT NULL,
	`flair`	TEXT,
	`num_of_comments`	INTEGER,
	`num_of_submissions`	INTEGER,
	`total_com_score`	INTEGER,
	`total_sub_score`	INTEGER,
	PRIMARY KEY(`user_id`)
);
CREATE TABLE "submissions" (
	`submission_id`	TEXT NOT NULL,
	`user_id`	TEXT,
	`subreddit_id`	TEXT,
	`title`	TEXT,
	`upvotes`	INT,
	`ratio`	DECIMAL(2,3),
	`score`	INT,
	`comments`	INT,
	`reports`	INT,
	`permalink`	TEXT,
	`domain`	TEXT,
	`locked`	BOOLEAN,
	`created`	DATE,
	`label`	TEXT,
	PRIMARY KEY(`submission_id`)
);
CREATE TABLE "comments" (
	`comment_id`	TEXT NOT NULL,
	`submission_id`	TEXT,
	`user_id`	TEXT,
	`user_flair`	TEXT,
	`upvotes`	INT,
	`controversiality`	INT,
	`gold`	INT,
	`depth`	INT,
	`parent_id`	TEXT,
	`created`	DATE,
	`edited`	DATE,
	`body`	TEXT,
	`deleted`	INTEGER,
	PRIMARY KEY(`comment_id`)
);
COMMIT;
