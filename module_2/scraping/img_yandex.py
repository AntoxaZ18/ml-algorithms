import requests
import os
from time import sleep
from bs4 import BeautifulSoup as bs4
from concurrent.futures import ThreadPoolExecutor, as_completed

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
    "application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Host": "market.yandex.ru",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/83.0.4103.61 Safari/537.36",
}

# формат:
#key - folder where images would be saved in format 0001.jpg
#value - tuple, first element - base request, second - list of extra words which would be added to base request
dataset = {
    './polar_bear': ('polar bear', ['ice', 'arctic', 'family', 'fishing', 'angry']),
    './brown_bear': ('brown bear', ['forest', 'river', 'family', 'fishing', 'growls', 'angry'])
}


def get_image_links(chrome_driver, query):

    link = f'https://yandex.ru/images/search?text={query}'

    chrome_driver.get(link)

    try:
        # Ожидание загрузки элементов
        WebDriverWait(chrome_driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ImagesContentImage-Image"))
        )
    except TimeoutException:
        print(f"Timeout при загрузке страницы для запроса: {query}")
        return set()


    # Прокрутка страницы для загрузки всех изображений
    last_height = chrome_driver.execute_script("return document.body.scrollHeight")
    while True:
        chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)  # Ждем загрузки новых изображений
        new_height = chrome_driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


    soup = bs4(chrome_driver.page_source, 'html.parser')
    links = soup.find_all(
            "img", class_="ImagesContentImage-Image ImagesContentImage-Image_clickable"
        )

    return set(link['src'] for link in links)



def download_images(links:set, path:str):
    if not os.path.exists(path):
        os.makedirs(path)

    def save_to_file(directory, idx, link_to_download):
        file_path = f'{directory}/{str(idx).zfill(4)}.jpg'

        try:
            response = requests.get(f'https:{link_to_download}', timeout=10)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
        except requests.RequestException as e:
            print(f'Error in downloading link {link_to_download}: {e}')
            raise e
        except Exception as e:
            print(f'Unknown error {link_to_download}: {e}')
            raise e

    
    #speed up loading images with multithreading
    with ThreadPoolExecutor() as pool:
        print('start downloading images')
        futures = [pool.submit(save_to_file, path, idx, link) for idx, link in enumerate(links)]

        errors = 0
        success = 0

        for future in as_completed(futures):
            if future.exception():
                print(future.exception())
                errors += 1
            else:
                success += 1

        print(f'Try to download {len(links)} to {path}')
        print(f'Downloaded successfully: {success}\nWith errors: {errors}')



def get_links(queries, driver, image_count=1000):
    links = set()

    for query in queries:
        links |= get_image_links(driver, query)
        
        print(f'total links: {len(links)}')

        if len(links) >= image_count or len(links) == 0:
            break

    return links


class ChromeDriver:
    def __init__(self, headers: dict) -> None:
        self.headers = headers
        self.driver = None

    def __enter__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        for key, value in self.headers.items():
            options.add_argument( f'{key}={value}')

        self.driver = webdriver.Chrome(options=options)

        return self.driver

    def __exit__(self, exc_type, exc_value, trace):
        if self.driver:
            self.driver.quit()
        if exc_type is not None:
            print(f"Exception: {exc_type.__name__}, {exc_value}")
    
    
if __name__ == '__main__':
    with ChromeDriver(HEADERS) as driver:

        for path, (base_query, extra) in dataset.items():
            queries = ['%20'.join(base_query.split())]  #формируем базовый запрос
            #добавляем доп слова для запроса чтобы увеличить число картинок
            queries += ['%20'.join([*base_query.split(), *extra_query.split()]) for extra_query in extra]  
            links = get_links(queries, driver)
            download_images(links, path)
        
