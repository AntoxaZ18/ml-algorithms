import psycopg2 as ps 
from typing import List
from functools import partial
import pandas as pd



DB_HOST = 'localhost'
DB_PORT = 5433
DB_USER = 'postgres'
DB_PASSWORD = 'postgres' #bad practice
DB_DATABASE = 'Sakila_Sample_Database'

DATA_PATH = './module_2/cert/dataframes/'

CONNECTION_STR = f"host={DB_HOST} port={DB_PORT} dbname={DB_DATABASE} user={DB_USER} password={DB_PASSWORD}"


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


# Какова доля фильмов в каждой рейтинговой категории(G,PG,PG-13,R ит.д.) в нашем ассортименте?
QUERY_1 = '''SELECT film.rating, COUNT(*) 
             FROM film 
             GROUP BY film.rating'''

result = db_fetch(QUERY_1)
save_to_csv(result, ['rating', 'film_count'], 'query_1.csv')



# print(result)

# total = sum((i[1] for i in result))

# result = [(i[0], i[1] / total) for i in result]

# for rating, proportion in result:
#     print(f'{rating}: {proportion}')

#Какие категории фильмов чаще всего арендуются клиентами?
QUERY_2 = '''SELECT film.rating, COUNT(*) as count
             FROM film 
             GROUP BY film.rating
             ORDER BY count DESC
             '''

result = db_fetch(QUERY_2)
save_to_csv(result, ['rating', 'film_count'], 'query_2.csv')



# Какова средняя продолжительность проката (rental duration) для каждой категории фильмов?
QUERY_3 = '''SELECT 
    film.rating, 
    AVG(EXTRACT(EPOCH FROM (rental.return_date - rental.rental_date))) / 3600 AS average_rental_duration_hours
    FROM rental
    JOIN inventory ON rental.inventory_id = inventory.inventory_id
    JOIN film ON inventory.film_id = film.film_id
    GROUP BY film.rating;
            '''

result = db_fetch(QUERY_3)
save_to_csv(result, ['rating', 'mean_duration'], 'query_3.csv')

# Каковы тенденции в ежемесячном доходе от проката(monthly rental revenue) и продажах (sales) за прошедший год?
QUERY_4 = '''
select 
	count(payment.amount) as sales,
	sum(payment.amount) as revenue,
	EXTRACT(MONTH FROM payment.payment_date) as m,
	EXTRACT(YEAR FROM payment.payment_date) as y
from payment 
group by 
    EXTRACT(MONTH FROM payment.payment_date),
    EXTRACT(YEAR FROM payment.payment_date)'''

result = db_fetch(QUERY_4)
save_to_csv(result, ['sales', 'revenue', 'month', 'year'], 'query_4.csv')


# Как соотносятся показатели продаж в разных магазинах?
QUERY_5 = '''
SELECT count(amount) as sales, sum(amount) as revenue, store_id
from payment  
join customer ON payment.customer_id = customer.customer_id
group by store_id'''

result = db_fetch(QUERY_5)
save_to_csv(result, ['sales', 'revenue', 'store_id'], 'query_5.csv')


# Каковы средние затраты на замену(replacement_cost) фильмов в разных жанрах?
QUERY_6 = '''
select 
	category.name as category, AVG(film.replacement_cost) as avg_cost
from film
join film_category on film.film_id = film_category.film_id
join category on film_category.category_id = category.category_id 
group by category.name
'''
result = db_fetch(QUERY_6)
save_to_csv(result, ['category', 'avg_cost'], 'query_6.csv')

# Какие актеры снимаются в самых разных жанрах фильмов?
QUERY_7 = '''
select 
	actor.actor_id as actor_id, actor.first_name, actor.last_name, count(film_category.category_id) as counter
from actor
join film_actor on film_actor.actor_id = actor.actor_id
join film on film.film_id = film_actor.film_id
join film_category on film_category.film_id = film.film_id
group by actor.actor_id
order by counter desc '''

result = db_fetch(QUERY_7)
save_to_csv(result, ['actor_id', 'first_name', 'last_name', 'genres'], 'query_7.csv')


