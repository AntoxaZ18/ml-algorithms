import psycopg2 as ps 
import sys
from string import Template


DB_HOST = 'localhost'
DB_PORT = 5433
DB_USER = 'postgres'
DB_PASSWORD = 'postgres' #bad practice to store password in source
DB_DATABASE = 'Sakila_Sample_Database'

DATA_PATH = './module_2/cert/data/sqlite-sakila-db'

DB_CONNECT_STR = f'host={DB_HOST} port={DB_PORT} dbname={DB_DATABASE} user={DB_USER} password={DB_PASSWORD}'


def create_connection(conect_string):
    try:
        return ps.connect(conect_string)
    except Exception as e:
        print(e)
        return None


def create_trigger(table_name, func):
    '''Функция возвращает sql запрос на создание триггера запуска функции по добавлению данных в таблицу'''
    s = Template('''
CREATE TRIGGER $trig_name AFTER INSERT ON $table
    EXECUTE PROCEDURE $func();
''')    
    return s.substitute(trig_name = f'{table_name}_trig', table = table_name, func = func)


def create_func(table_name):
    '''Функция возвращает sql запрос на создание функции которая добавляет последнее обновление данных'''
    s = Template('''
CREATE FUNCTION $func_name() RETURNS trigger AS $$$func_name$$
    BEGIN
        UPDATE $table SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
    END;
$$$func_name$$ LANGUAGE plpgsql;''')
    return s.substitute(func_name = f'{table_name}_trig', table = table_name)


def create_trigger_in_db(conn, table_name: str):
    '''создает функцию и триггер в заданную таблицу'''
    try:
        with conn.cursor() as curs:
            func = create_func(table_name)
            trigger = create_trigger(table_name, f'{table_name}_trig')
            curs.execute(func)
            curs.execute(trigger)
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)
        raise e


def get_all_tables(conn):

    try:
        with conn.cursor() as curs:

            curs.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            return [i[0] for i in curs.fetchall()]

    except Exception as e:
        conn.rollback()
        print(e)


def create_schema(conn, schema):

    try:
        with conn.cursor() as curs:
            insert = open(schema, 'r', encoding='utf8').read()

            curs.execute(insert)
            conn.commit()

    except Exception as e:
        conn.rollback()
        print(e)


def load_data(conn, insert_sql):

    try:
        with conn.cursor() as curs:
            insert = open(insert_sql, 'r', encoding='utf8').read()

            curs.execute(insert)
            conn.commit()

    except Exception as e:
        conn.rollback()
        print(e)



if __name__ == '__main__':
    conn = create_connection(DB_CONNECT_STR)
    if not conn:
        sys.exit(1)

    #create  schema and load data to db
    create_schema(conn, f'{DATA_PATH}/sqlite-sakila-schema.sql')
    load_data(conn,  f'{DATA_PATH}/sqlite-sakila-insert-data.sql')

    #get tables and create triggers
    tables = get_all_tables(conn)
    for table in tables:
        create_trigger_in_db(conn, table)
