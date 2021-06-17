import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import json
import os


#   тоже соберу информацию с сайта https://www.shinservice.ru/search/ALL/summer/205-55-R16/ но из json
def get_data():
    # making requests
    r = requests.get('https://www.shinservice.ru/api/tires/ALL/summer/205-55-R16/?&obtainingMethod=pickup&page=4')

    print(r.json())
    print(type(r.json()))

    # create directory
    if not os.path.exists("data_api_shin"):
        os.mkdir("data_api_shin")

    # write file to directory in json !!!
    with open("data_api_shin/index_api.json", "w") as file:
        json.dump(r.json(), file, indent=4, ensure_ascii=False)


def extract_data_from_json():
    with open("data_api_shin/index_api.json") as file:
        src = json.load(file)
    # print(src)

    all_data = src["data"]["minPrice"]
    all_items = src["data"]["items"]

    for item in all_items:
        item_name = item["title"]
        item_link = item["modelUri"]
        try:
            item_country = item["params"]["countryImageName"]
        except Exception:
            item_country = "No data"

        print(f"Бренд: {item_name}\nСсылка: {item_link}\nПроизводитель: {item_country}\n")




    # # only keys
    # for k in all_data:
    #     print(f"Ключ: {k}")
    #
    # # only values
    # for v in all_data.values():
    #     print(f"Значение: {v}")
    #
    #
    # for k,v in all_data.items():
    #     print(f"*{k} : {v}")
    #     # for k,v in items.items():
    #     #     print(f"{k}-{v}")
    #

def main():
    # get_data()
    extract_data_from_json()


if __name__ == '__main__':
    main()
