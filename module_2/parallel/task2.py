from multiprocessing.pool import Pool
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
import os
from time import time
import zipfile


def read_dig(path: str):
    link = open(f"./module_2/parallel/path/{path}", "r").read()
    return int(open(f"./module_2/parallel/{link}", "r").read())


def test_threads(workers):
    count = 0
    start = time()

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = (
            executor.submit(read_dig, i) for i in os.listdir("./module_2/parallel/path")
        )
        for f in as_completed(futures):
            count += f.result()

    return time() - start


# Небольшое исследование на тему производительности различных вариантов параллельной работы  и влияние распаковки на производительность
if __name__ == "__main__":
    count = 0
    #
    # Базовая реализация без потоков
    count = 0
    start = time()
    for link in [i for i in os.listdir("./module_2/parallel/path")]:
        count += read_dig(link)

    print(f"Базовая реализация без потоков: {(time() - start):.3f}")

    # реализация на multiprocessing.pool с распакованными файлами
    count = 0
    start = time()
    with Pool() as pool:
        for result in pool.map(
            read_dig, [i for i in os.listdir("./module_2/parallel/path")]
        ):
            count += result

    print(f"Время работы функции pool map: {(time() - start):.3f}")

    print(f"Сумма всех чисел: {count}")

    # Задача похожа iobound пробуем ее решить через ThreadPoolExecutor с разным количеством потоков и ищем оптимальное количество от 1 до 50
    res = []
    for i in range(1, 50):
        time_ = test_threads(i)
    res.append((time_, i))

    time_s, optimal_thread = min(res, key=lambda x: x[0])

    print(
        f"ThreadPoolExecutor executor best result: {time_s:.3f} s with {optimal_thread} threads"
    )

    # Проверим скорость работы на нераспакованных файлах с дефолтным размеров пула потоко
    start = time()

    paths = zipfile.ZipFile(f"./module_2/parallel/path_8_8.zip", "r")
    files = zipfile.ZipFile(f"./module_2/parallel/recursive_challenge_8_8.zip", "r")

    count = 0
    links = [paths.read(i).decode().replace("\\", "/") for i in paths.namelist()][1:]

    with ThreadPoolExecutor() as executor:
        futures = (executor.submit(files.read, i) for i in links)
        for future in as_completed(futures):
            count += int(future.result())

    print(
        f"ThreadPoolExecutor with default size on archive {(time() - start):.3f} result: {count}"
    )

    # Вывод наибольшая производительность получилась при использовании 49 потоков (0,213с) незначительный прирост относительно базовой,
    # базовая реализация без потоков (0,251с) на процессах самый медленный вариант (0,309с)
    # с заархивированными файлами 0,586с (небольшая просадка относительно распакованных, хороший вариант чтобы не распаковывать много файлов)
