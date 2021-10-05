import sqlalchemy
import pg8000
import psycopg2
import os

class sql_interface():

    @staticmethod
    def open_connection():
        db = sqlalchemy.create_engine(sqlalchemy.engine.url.URL(
            drivername='postgres+pg8000',
            username=os.environ.get('USERNAME'),
            password=os.environ.get('PASSWORD'),
            database=os.environ.get('DATABASE'),
            query={'unix_sock': '/cloudsql/test-project-254608:us-central1:appdata/.s.PGSQL.5432'}))

        con = db.connect()
        return con

    @staticmethod
    def open_local():
        username=os.environ.get('USERNAME'),
        password=os.environ.get('PASSWORD'),
        database=os.environ.get('DATABASE'),
        address = "postgresql+psycopg2://"+ username + password + "@127.0.0.1/" + database
        db = sqlalchemy.create_engine(address, client_encoding='utf8')
        con = db.connect()
        return con

    @staticmethod
    def create_table(con, name, cols, dtype):
        assert isinstance(name, object)
        i = 0
        str = []
        while i < len(cols):
            a = cols[i]
            b = dtype[i]
            if i == 0:
                c = a + " " + b + " PRIMARY KEY"
            else:
                c = a + " " + b
            str.append(c)
            i = i + 1

        fullstr = ", "
        fullstr = fullstr.join(str)
        con.execute(f'CREATE TABLE {name} ({fullstr})')
        return

    @staticmethod
    def insertQ(con, tname, params, vals):
        assert isinstance(tname, object)
        parameters = ", "
        parameters = parameters.join(params)

        for i in range(len(vals)):
            vals[i] = "'{}'".format(str(vals[i]))

        values = ", "
        values = values.join(vals)
        con.execute(f'INSERT INTO {tname} ({parameters}) VALUES ({values})')
        return

    @staticmethod
    def select(con, tname, cols, pattern):
        if isinstance(cols, tuple) or isinstance(cols, list):
            parameters = ", "
            parameters = parameters.join(cols)
        else:
            parameters = cols

        entries = con.execute(f'SELECT {parameters} FROM {tname} WHERE {pattern};').fetchall()
        result = []
        for entry in entries:
            for i in range(len(entry)):
                if isinstance(cols, tuple) or isinstance(cols, list):
                    thisEntry = str(cols[i]) + ':' + str(entry[i])
                    result.append(thisEntry)
                else:
                    thisEntry = str(entry[i])
                    result.append(thisEntry)
        return result

    @staticmethod
    def selectall(con, tname, cols, pattern=''):
        if isinstance(cols, tuple) or isinstance(cols, list):
            parameters = ", "
            parameters = parameters.join(cols)
        else:
            parameters = cols
        entries = con.execute(f'SELECT {parameters} FROM {tname} {pattern};', ).fetchall()
        result = []
        for entry in entries:
            for i in range(len(entry)):
                if isinstance(cols, tuple) or isinstance(cols, list):
                    thisEntry = str(cols[i]) + ':' + str(entry[i])
                    result.append(thisEntry)
                else:
                    thisEntry = str(entry[i])
                    result.append(thisEntry)
        return result

