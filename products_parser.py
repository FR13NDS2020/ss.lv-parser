from bs4 import BeautifulSoup
import json
import concurrent.futures
import requests
import tqdm

product_data = []


def writer(data, file_name):
    with open(f"{file_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def parse(URL):
    h = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/108.0.0.0 Safari/537.36",
    }

    req = requests.get(url=URL, headers=h)
    src = req.text
    soup = BeautifulSoup(src, "lxml")

    column = soup.find("table", {"id": False, "align": "center", "border": "0", "cellpadding": "2", "cellspacing": "0", "width": "100%"}).findAll("tr")

    # names for ccategories

    data_names = soup.find("tr", {"id": "head_line"}).findAll("a")

    names = []
    for i in data_names[1:]:
        names.append(i.text)

    # getting data

    for j in column[1:]:
        data = j.findAll("td")[3:]
        ids = j["id"]
        if len(ids) == 11:
            da = {}
            for l in range(len(names)):
                da[names[l]] = data[l].text if l < len(data) else None
            region = j.find("div", class_="ads_region")
            link = j.find("a", href=True)
            if region is not None:
                da["Region"] = region.text if region else None
            da["Link"] = "https://www.ss.com" + link["href"] if link else None
            product_data.append(da)


def gettinglinks(URL):
    h = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }
    req = requests.get(url=URL, headers=h)
    src = req.text
    soup = BeautifulSoup(src, "lxml")

    links_count = soup.find("a", {"class": "navi"})
    count = links_count["href"][:-5]
    pages = count.split("page")[1]
    all_links = []
    for i in range(int(pages)):
        all_links.append(URL + f"page{i+1}.html")

    return all_links


def parse_pages(URL):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        links = gettinglinks(URL)
        futures = [executor.submit(parse, i) for i in links]
        for f in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(links)):
            i = f.result()

    writer(product_data, "parsedsska")