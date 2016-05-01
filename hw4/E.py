import bs4
from urllib.request import urlopen
import sys


def get_pages(from_page, to_page):
    for i in range(from_page, to_page):
        link = "https://habrahabr.ru/top/alltime/page{number}/".format(number=i)
        with urlopen(link) as conn:
            data = conn.read()
            html = data.decode('utf-8')
            print("Got page: {url}".format(url=link))
            soup = bs4.BeautifulSoup(html, "html.parser")
            for anchor in soup.find_all("a", {"class": "post_title"}):
                yield anchor["href"]


def get_text(url):
    print("Parsing text from {url}".format(url=url))
    with urlopen(url) as conn:
        data = conn.read()
        html = data.decode('utf-8')
        soup = bs4.BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "content"})
        return content.get_text()

if (len(sys.argv) == 3):
    from_page = int(sys.argv[1])
    to_page = int(sys.argv[2])
    with open("habr-top.txt", "a") as f:
        total_words = 0
        for text in map(get_text, get_pages(from_page, to_page)):
            total_words += len(text.split())
            print(total_words)
            f.write(text)
else:
    print("Usage: python E.py from-page-index to-page-index")
