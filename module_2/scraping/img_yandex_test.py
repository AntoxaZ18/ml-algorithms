import requests
import os
from time import sleep
from bs4 import BeautifulSoup as bs4
from concurrent.futures import wait, ThreadPoolExecutor, ALL_COMPLETED

from selenium import webdriver

dataset = {
    './polar_bear': ['polar%20bear', 'polar%20bear%ice', 'polar%20bear%20arctic', 'polar%20bear%20family', 'polar%20bear%20fishing', 'polar%20bear%20angry'],
    './brown_bear': ['brown%20bear', 'brown%20bear%20forest', 'brown%20bear%20river', 'brown%20bear%20family', 'brown%20bear%20fishing', 'brown%20bear%20growls', 'brown%20bear%20angry']
}


def get_image_links(chrome_driver, queries):
    images = set()

    for query in queries:

        link = f'https://yandex.ru/images/search?text={query}'

        chrome_driver.get(link)
        sleep(5)
        chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        soup = bs4(chrome_driver.page_source, 'html.parser')
        links = soup.find_all(
                "img", class_="ImagesContentImage-Image ImagesContentImage-Image_clickable"
            )

        for link in links:
            images.add(link['src'])

        print(f'total len ({len(images)})')
        if len(images) >= 1000:
            return images
        
    return images


def save_images(links:set, path:str):
    if not os.path.exists(path):
        os.makedirs(path)

    def save_to_file(directory, idx, link_to_download):
        file = f'{directory}/{str(idx).zfill(4)}.jpg'
        print(f'save to {file}')
        with open(file, 'wb+') as f: 
            f.write(requests.get(f'https:{link_to_download}').content)
    
    #speed up loading images with multithreading
    with ThreadPoolExecutor() as pool:
        futures = [pool.submit(save_to_file, path, idx, link) for idx, link in enumerate(links)]
        wait(futures, timeout=None, return_when=ALL_COMPLETED)


def set_up():
    headers = {
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

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    for key, value in headers.items():
        chrome_options.add_argument( f'{key}={value}')

    return webdriver.Chrome(options=chrome_options)

def tear_down(driver):
    driver.quit()


def save_category(path, queries, driver):
    print(f'start saving category {path}')
    
    links = get_image_links(driver, queries)
    save_images(links, path)
    print(f'total images downloaded: {len(links)}')

chrome_driver = set_up()
for path, queries in dataset.items():
    save_category(path, queries, chrome_driver)
    
tear_down(chrome_driver)