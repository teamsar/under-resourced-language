import sqlite3


class KBBIOfflineHandler:
    def __init__(self, path):
        self.path = path

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.path)
            return conn
        except ValueError as e:
            print(e)
        return None

    def get_all_datakata(self):
        conn = self.create_connection()
        with conn:
            # get kata from kbbi offline
            cur = conn.cursor()
            sql = "select distinct(trim(lower(katakunci))) " \
                  "as katakunci, polarity from datakata"
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            kms = dict(data)

            # concate indonesian slang words
            f = open('IndonesianSlangWords.txt', 'r')
            for line in f.readlines():
                tokens = line.strip().split('/')
                kms[tokens[0].strip()] = tokens[1].strip()
            return kms

