import ast
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

lists = ast.literal_eval((open('./module_2/parallel/test_list_numbers.txt', 'r').read())) #read list of lists from file


def process_number(lst_id: int, number: int):   #функция принимает индекс массива и число для обработки
    sleep(0.2)
    return lst_id, number * 2


lengths = {lst_id: len(i) for (lst_id, i) in enumerate(lists)}  #словарь где ключ - индекс массива, значение - длина массива 
result_sum = {} #словарь куда сохраняем результаты, ключ - индекс массива, значение - текущая сумма этого массива


def create_process_lst(all_list: list):
    numbers_to_process = [] 

    for lst_id, lst in enumerate(all_list):    #создаем список который состоит из кортежей где второе значение это число которое нужно обработать, первое число - индекс массива которому оно принадлежит
        for number in lst:
            numbers_to_process.append((lst_id, number))

    return numbers_to_process

with ThreadPoolExecutor(max_workers=10) as pool:
    futures = [pool.submit(process_number, idx, i) for idx, i in create_process_lst(lists)]

    for future in as_completed(futures):
        list_id, number = future.result()

        result_sum[list_id] = result_sum.get(list_id, 0) + number   #добавляем к текущей сумме результат работы функции 
        lengths[list_id] = lengths[list_id] - 1 #уменьшаем число обработанных элементов в списке
        if lengths[list_id] == 0:   #если все числа списка обработались выводим результат
            print(f"Сумма чисел в первом обработанном списке: {result_sum[list_id]}")
            break