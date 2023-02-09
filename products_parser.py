from bs4 import BeautifulSoup
import json
import concurrent.futures
import requests
import tqdm


def write_to_file(data, file_name):
    with open(f"{file_name}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

product_data = []
def parse_data(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/108.0.0.0 Safari/537.36",
    }

    response = requests.get(url=url, headers=headers)
    source = response.text
    soup = BeautifulSoup(source, "lxml")

    columns = soup.find("table", {"id": False, "align": "center", "border": "0", "cellpadding": "2",
                                  "cellspacing": "0", "width": "100%"}).find_all("tr")

    data_names = soup.find("tr", {"id": "head_line"}).find_all("a")

    names = [name.text for name in data_names[1:]]

    for column in columns[1:]:
        cells = column.find_all("td")[3:]
        id = column["id"]
        if len(id) == 11:
            data = {}
            for i in range(len(names)):
                data[names[i]] = cells[i].text if i < len(cells) else None

            region = column.find("div", class_="ads_region")
            link = column.find("a", href=True)

            data["Region"] = region.text if region else None
            data["Link"] = "https://www.ss.com" + link["href"] if link else None
            product_data.append(data)

    return product_data


def get_links(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }
    response = requests.get(url=url, headers=headers)
    source = response.text
    soup = BeautifulSoup(source, "lxml")

    links_count = soup.find("a", {"class": "navi"})
    count = links_count["href"][:-5]
    pages = count.split("page")[1]
    all_links = [f"{url}page{i + 1}.html" for i in range(int(pages))]

    return all_links


def parse_pages(URL):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        links = get_links(URL)

        # Submit tasks to the executor
        tasks = [executor.submit(parse_data, i) for i in links]

        # Use tqdm to display progress bar
        for future in tqdm.tqdm(concurrent.futures.as_completed(tasks), total=len(links)):
            i = future.result()

    # Write the final result to a file
    write_to_file(product_data, "parsedsska")
