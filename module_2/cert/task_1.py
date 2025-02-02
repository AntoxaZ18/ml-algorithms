import psycopg2 as ps 
import sys
from string import Template



DB_HOST = 'localhost'
DB_PORT = 5433
DB_USER = 'postgres'
DB_PASSWORD = 'postgres' #bad practice
DB_DATABASE = 'Sakila_Sample_Database'

DATA_PATH = './module_2/cert/data/sqlite-sakila-db'


# connection = sqlite3.connect(f'{DATA_PATH}/sqlite-sakila.sq')

# cursor = connection.cursor()

# cursor.execute('select * from actor')
# users = cursor.fetchall()

# # Выводим результаты
# for user in users:
#     print(user)


# connection.close()


# sys.exit(0)

try:
     conn = ps.connect(
          host = DB_HOST,
          port = DB_PORT,
          user = DB_USER,
          password = DB_PASSWORD,
          database = DB_DATABASE
     )
except Exception as e:
     print(f'Cannot open database exception: {e}')
     sys.exit(1)



def create_trigger(table_name, func):
     
    s = Template('''
CREATE TRIGGER $trig_name AFTER INSERT ON $table
    EXECUTE PROCEDURE $func();

''')

    
    return s.substitute(trig_name = f'{table_name}_trig', table = table_name, func = func)

def create_func(table_name):
     
    s = Template('''
CREATE FUNCTION $func_name() RETURNS trigger AS $$$func_name$$
    BEGIN
        UPDATE $table SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
    END;
$$$func_name$$ LANGUAGE plpgsql;''')

    return s.substitute(func_name = f'{table_name}_trig', table = table_name)


def create_trigger_in_db(table_name: str):

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


# def get_all_tables():

#     try:
#         with conn.cursor() as curs:

#             curs.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
#             return [i[0] for i in curs.fetchall()]

#     except Exception as e:
#         conn.rollback()
#         print(e)

# for table in get_all_tables():
#     create_trigger_in_db(table)



try:
    with conn.cursor() as curs:
        schema = open(f'{DATA_PATH}/sqlite-sakila-schema.sql', 'r', encoding='utf8').read()

        curs.execute(schema)
        conn.commit()

except Exception as e:
    conn.rollback()
    print(e)




try:
    with conn.cursor() as curs:
        insert = open(f'{DATA_PATH}/sqlite-sakila-insert-data.sql', 'r', encoding='utf8').read()

        curs.execute(insert)
        conn.commit()

except Exception as e:
    conn.rollback()
    print(e)


# print(os.getcwd())






