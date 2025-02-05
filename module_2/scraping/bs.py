from bs4 import BeautifulSoup as bs4


content = open('page.html', 'r', encoding='utf-8').read()


soup = bs4(content, 'html.parser')


links = soup.find_all(
        "img", class_="ImagesContentImage-Image ImagesContentImage-Image_clickable"
    )

for i, link in enumerate(links):
    print(i, link['src'])