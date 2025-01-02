#Задание 2
DB_CACHE = {}


def cache(db_name: str, expire = 5): 

    def cache_dec(f):
        def wrapper(*args, **kwargs):
            key = f'{db_name}_{f.__name__}'
            if key not in DB_CACHE:
                DB_CACHE[key] = dict()
            thing, *_ = args
            if thing not in DB_CACHE[key] or DB_CACHE[key][thing][1] == 0:
                
                data = f(*args, **kwargs) #make db request here
                DB_CACHE[key][thing] = [data, expire]

                return data + f' from {db_name}, now cached with expire={DB_CACHE[key][thing][1]}'
            else:
                DB_CACHE[key][thing][1] -= 1
                return f'{DB_CACHE[key][thing][0]} cached in {db_name}, expire={DB_CACHE[key][thing][1]}'
                
        return wrapper

    return cache_dec


@cache('sqlite')
def get_info(thing:str):
    return f'Info about: {thing}'

@cache('postgre', expire = 30)
def get_info2(thing:str):
    return f'second Info about: {thing}'

@cache('postgre', expire = 3)
def get_info3(thing:str):
    return f'third Info about: {thing}'

#Делаем запрос к sqlitr
print(get_info('thing_1'))
print(get_info('thing_1'))
print(get_info('thing_1'))
print(get_info('thing_1'))
print(get_info('thing_1'))
print(get_info('thing_1'))
print(get_info('thing_1'))

#Добавляем запрос к другой БД
print('______________________')
print(get_info2('thing_2'))
print(get_info2('thing_2'))
print(get_info2('thing_2'))
print(get_info2('thing_2'))
print(get_info2('thing_2'))
print(get_info2('thing_2'))
print(get_info2('thing_2'))

#Добавляем еще один запрос ко второй бд
print('______________________')
print(get_info3('thing_3'))
print(get_info3('thing_3'))
print(get_info3('thing_3'))
print(get_info3('thing_3'))
print(get_info3('thing_3'))
print(get_info3('thing_3'))

#Проверяем что предыдущий запрос корректно работает после добавления нового
print('______________________')
print(get_info2('thing_2'))
print(get_info2('thing_2'))
print(get_info2('thing_2'))