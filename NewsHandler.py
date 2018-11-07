import sqlite3
from TokenHandler import TokenHandler

class NewsHandler:
    def __init__(self, path):
        self.path = path

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.path)
            return conn
        except ValueError as e:
            print(e)
        return None

    def get_political_news_comment(self):
        conn = self.create_connection()
        with conn:
            cur = conn.cursor()
            sql = "select comment_id, comment from t_comments where comment_id " \
                  "in (select news_id from t_news where news_category = nc2 " \
                  "and news_category = 1)"
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()

            comments = {}
            ctr_cmmnt = 0
            for content in data:
                comment_id = content[0].strip()
                comment = ' '.join(TokenHandler().word_tokenizer(content[1].strip().lower()))
                if comment_id not in comments.keys():
                    comments[comment_id] = []
                    comments[comment_id].append((ctr_cmmnt, comment))
                else:
                    comments[comment_id].append((ctr_cmmnt, comment))
                ctr_cmmnt += 1
            return comments
