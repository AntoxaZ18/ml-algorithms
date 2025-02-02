import psycopg2 as ps
import pandas as pd
from typing import List
from functools import partial

DB_HOST = 'localhost'
DB_PORT = 5433
DB_USER = 'postgres'
DB_PASSWORD = 'postgres' #bad practice
DB_DATABASE = 'Sakila_Sample_Database'

DATA_PATH = './module_2/cert/dataframes/'

CONNECTION_STR = f"host={DB_HOST} port={DB_PORT} dbname={DB_DATABASE} user={DB_USER} password={DB_PASSWORD}"


QUERY = '''
select 
	film.film_id,
	film.title,
	film.description,
	film.release_year,
	film.rental_duration,
	film.rental_rate,
	film.length as duration,
	film.replacement_cost,
	film.rating,
	film.special_features,
	language.name as language,
	category.name as category,
	actor.first_name,
	actor.last_name,
	inventory.store_id,
    inventory.inventory_id 
from film
	join film_actor on film.film_id = film_actor.film_id 
	join language on film.language_id = language.language_id 
	join film_category on film.film_id = film_category.film_id
	join category on film_category.category_id = category.category_id 
	join inventory on film.film_id = inventory.film_id 
	join actor on actor.actor_id = film_actor.actor_id'''

def make_query(query: str, conn_str: str = ''):
    '''Create a query and fetching data from database
    '''
    if not conn_str:
        raise ValueError('no db connection str')

    with ps.connect(CONNECTION_STR) as conn:
        cur = conn.cursor()
        cur.execute(query)
        result = list(cur.fetchall())

    return result

db_fetch = partial(make_query, conn_str = CONNECTION_STR)

def save_to_csv(data: List[tuple], columns, filename: str):
    pd.DataFrame(data, columns=columns).to_csv(DATA_PATH + filename)


result = db_fetch(QUERY)

#replace memoryview with string representation 
ready_result = []   
for row in result:
    ready_result.append([bytes(i) if isinstance(i, memoryview) else i for i in row])


columns = ['film_id', 
           'title',
           'description',
           'release_year',
           'rental_duration',
           'rental_rate',
           'duration',
           'replacement_cost',
           'rating',
           'special_features',
           'language',
           'category',
           'first_name',
           'last_name',
           'store_id',
           'inventory_id']
save_to_csv(ready_result, columns, 'all_columns.csv')



df = pd.read_csv(DATA_PATH + 'all_columns.csv')

df.describe()