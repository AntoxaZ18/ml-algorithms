from functools import partial

users = [{'name': 'Ivan', 'age': 21}, {'name': 'Mark', 'age': 32}, {'name': 'Lolita', 'age': 25}]


def _sort_users_by_age(user_list: list, reverse: bool):
    return sorted(user_list, reverse=reverse, key=lambda x: x.get('age'))


sort_ascend = partial(_sort_users_by_age, reverse = False)  #сортировка по увеличению возраста
sort_descend = partial(_sort_users_by_age, reverse = True)  #сортировка по убыванию возраста



print(sort_ascend(users))
print(sort_descend(users))

