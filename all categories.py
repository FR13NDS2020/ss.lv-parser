import json
from bs4 import BeautifulSoup
import requests


parent_dir = "C:/Users/Administrator/Documents/MY projects/ss.lv/parsed/"

main_json = {}


def writer(data, file_name):
    with open(f"{file_name}.json", "w") as f:
        json.dump(data, f, indent=4)


def reader(file_name):
    with open(f"{file_name}.json", "r") as f:
        return json.load(f)


cache = []


def parse(URL):# prosta parsit kategoriji iz ssilki

    if URL not in cache:

        page_data = {}

        # name = URL.split("/")[-2]
        h = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/108.0.0.0 Safari/537.36",
        }

        req = requests.get(url="https://www.ss.com/" + URL, headers=h)
        src = req.text
        s = BeautifulSoup(src, "lxml")

        first_page = s.findAll("a", {"class": "a_category", "id": True})

        titles = []
        links = []
        for i in first_page:
            title = i.text
            link = i["href"]
            titles.append(title)
            links.append(link)

        class Category:
            t = titles
            l = links

        for j in range(len(titles)):
            page_data[Category.t[j]] = Category.l[j]

        # print(page_data)
        cache.append(URL)
        return Category


##############
url = "https://www.ss.com/en/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 "
                  "Safari/537.36 "
}
req = requests.get(url, headers=headers)
src = req.text
soup = BeautifulSoup(src, "lxml")

##############
# tut jesc vse osnovnije kategoriji
main_categories = soup.findAll("a", {"class": "a1", "title": True})


def new_object(data, name):
    new = {}
    for i in name:
        new[i] = data

    # print(new)


for i in main_categories:
    category_name = i.text
    category_link = i["href"]
    data = parse(category_link)

    new_object(data.l, data.t)


writer(main_json, "main_json")