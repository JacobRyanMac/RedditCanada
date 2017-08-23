
class Thread(Body,Query):
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
    pass
