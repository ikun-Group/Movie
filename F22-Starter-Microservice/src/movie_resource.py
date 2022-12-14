import pymysql

import os
import uuid

class MovieResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        #
        # usr = os.environ.get("DBUSER")
        # pw = os.environ.get("DBPW")
        # h = os.environ.get("DBHOST")

        usr = 'admin'
        pw = 'dbuserdbuser'
        h = 'moviedb.chtcseno515m.us-east-1.rds.amazonaws.com'



        conn = pymysql.connect(
            host=h,
            port=3306,
            user=usr,
            password=pw,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True)
        return conn

    @staticmethod
    def get_by_key(key):
        sql = "SELECT * FROM movies_databases.movie_table where guid=%s";
        conn = MovieResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return result

    @staticmethod
    def get_all():
        sql = "SELECT * FROM movies_databases.movie_table";
        conn = MovieResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()
        return result


    @staticmethod
    def add_movie(name, cagtegory, year, rating):
        guid = str(uuid.uuid4())
        sql = " INSERT INTO movies_databases.movie_table(name, category, year, rating, guid) VALUES(%s,%s,%s,%s,%s) "
        conn = MovieResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (name, cagtegory, year, rating, guid))
        result = cur.fetchone()
        return result

    @staticmethod
    def update_movie(column, new_val):
        sql = "UPDATE movies_databases.movie_table SET %s=%s WHERE %s=%s"
        conn = MovieResource._get_connection()
        cur = conn.cursor()
        result = cur.fetchone()
        return result

    @staticmethod
    def delete_movie(column, condition):
        sql = "DELETE FROM movies_databases.movie_table WHERE %s=%s "
        conn = MovieResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, column, condition)
        result = cur.fetchone()
        return result




