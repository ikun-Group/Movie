import pymysql
import os
import uuid


class MovieResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
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
    def get_all():
        sql = "SELECT * FROM movies_databases.movie_table"
        conn = MovieResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()
        return result

    @staticmethod
    def get_by_template(field_list, template, limit=None, offset=None):
        sql = "select " \
              + ",".join(field_list) \
              + " from movies_databases.movie_table where " \
              + " and ".join(["%s = '%s'" % (key, val) if not type(val) == int
                              else "%s = %s" % (key, val)
                              for (key, val) in template.items()])
        if not limit and not offset:
            pass
        else:
            sql += " limit " + str(limit) + " offset " + str(offset)

        conn = MovieResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()
        # print(cur.mogrify(sql))
        return result

    @staticmethod
    def create_movie(name, category, year, rating):
        guid = str(uuid.uuid4())
        sql = "INSERT INTO movies_databases.movie_table(name, category, year, rating, guid) VALUES(%s,%s,%s,%s,%s) "
        conn = MovieResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (name, category, year, rating, guid))
        result = cur.fetchone()
        print('This is result',str(result))
        return result

    @staticmethod
    def update_movie(guid, name, category, year, rating):
        sql = "UPDATE movies_databases.movie_table SET name=%s, category=%s, year=%s, rating=%s WHERE guid=%s"
        conn = MovieResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (name, category, year, rating, guid))
        result = cur.fetchone()
        return result

    @staticmethod
    def delete_movie(guid):
        sql = "DELETE FROM movies_databases.movie_table WHERE guid=%s "
        conn = MovieResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, guid)
        result = cur.fetchone()
        return result
