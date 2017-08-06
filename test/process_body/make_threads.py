from FeatureSet import Threads

submission_id = "6ehv49"
database = '../canada_subreddit_test.db'
thread_folder = 'threads/'
Threads(database,thread_folder).make_thread(submission_id)

### OLD WAY, moved to FeatureSet

# import sqlite3
#
# submission_id = "6ehv49"
# database = '../canada_subreddit_test.db'
# thread_folder = 'threads/'
#
# def search_roots(p_id, thread_file):
#     cur.execute('SELECT body, comment_id  FROM comments WHERE parent_id = ?',(p_id,))
#     children = cur.fetchall()
#     for c in children:
#         thread_file.write(c[0] + '\n')
#         search_roots(c[1], thread_file)
#
# db = sqlite3.connect(database)
# cur = db.cursor()
# cur.execute('''
# SELECT c.comment_id, c.body, s.label
# FROM comments as c, submissions as s
# WHERE c.submission_id = s.submission_id
# AND c.parent_id = ?
# ''',(submission_id,))
#
# parents = cur.fetchall()
# for p in parents:
#     file_name = thread_folder + p[2] + '_' + p[0] + ".txt"
#     with open(file_name,"w") as file:
#         file.write(p[1] + '\n')
#         search_roots(p[0], file)
#         file.close
