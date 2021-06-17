import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import json
import os


#  соберу информацию с сайта https://www.shinservice.ru/search/ALL/summer/205-55-R16/
headers = {
    'authority': 'www.shinservice.ru',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'ss_utm_data=%7B%22uid%22%3A%22ea432462-61af-42bb-8c01-71698adc6744%22%2C%22datetime%22%3A%222021-06-15T16%3A29%3A42%2B03%3A00%22%2C%22type%22%3A%22adv%22%2C%22utmData%22%3A%7B%22utm_medium%22%3A%22cpc%22%2C%22utm_source%22%3A%22google%22%2C%22utm_campaign%22%3A%221663883230%22%2C%22utm_content%22%3A%22k50id%7Cpla-833491939434%7Ccid%7C1663883230%7Caid%7C321047133316%7Cgid%7C66781914600%7Cpos%7C%7Csrc%7Cg_%7Cdvc%7Cc%7Creg%7C9047022%7Crin%7C%7C%22%7D%2C%22domainReferral%22%3Anull%2C%22pageReferral%22%3A%22%22%7D; tyre_app=all; avail_is_map=0; season=S; disk_params_info=1; _gcl_aw=GCL.1623763783.CjwKCAjwn6GGBhADEiwAruUcKnXtg47D72uUHzTUjcDdqXyC4fh3vJP3Vjb5PPwip3NMXIWiEigUhBoCP8YQAvD_BwE; _gcl_au=1.1.1571240900.1623763783; _ga=GA1.2.2002026706.1623763783; _gid=GA1.2.610560295.1623763783; _gac_UA-3006239-4=1.1623763783.CjwKCAjwn6GGBhADEiwAruUcKnXtg47D72uUHzTUjcDdqXyC4fh3vJP3Vjb5PPwip3NMXIWiEigUhBoCP8YQAvD_BwE; _ym_uid=1623763784126113583; _ym_d=1623763784; _ym_isad=1; _ym_visorc=w; region_selected=true; profile={%22cars%22:{%22autoparts%22:[]%2C%22shinservice%22:[]}%2C%22search%22:{%22shops%22:[]%2C%22obtainingMethod%22:%22pickup%22%2C%22delivery%22:%220%2C0%22}%2C%22selectedOptions%22:{}%2C%22version%22:%223%22}; table_view_tires=true; tyre_width=205; tyre_pr=55; tyre_rad=R16; goFromSubmit=undefined; runflat=0; _cmg_csstqSDyT=1623765739; _comagic_idqSDyT=4597038547.6954793432.1623765738',
}


def get_data():
    # making requests
    # r = requests.get('https://www.shinservice.ru/search/ALL/summer/205-55-R16/', headers=headers)
    #
    # # create directory
    # if not os.path.exists("data_shin"):
    #     os.mkdir("data_shin")
    #
    # # write file to directory
    # with open("data_shin/index.html", "w") as file:
    #     file.write(r.text)

    # read file
    with open("data_shin/index.html") as file:
        src = file.read()

    # create object BeautifulSoup
    soup = BeautifulSoup(src, "lxml")

    # create variable for data json
    all_data_tyres = []

    # create template for csv
    with open("data_shin/all_data_tyres.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Brand",
                "Size",
                "Price",
                "link"
            )
        )

    all_cards = soup.find("div", class_="searchGoods").find_all("div", class_="goodCard-container_table")
    for card in all_cards:
        try:
            # brand
            card_name = card.find("div", class_="goodCard-topColumn_goToItem").get("title")
        except Exception as ex:
            print(f"Mistake in brand. {ex}")
            card_name = "No data"

        # size
        try:
            card_size = card.find("div", class_="goodCard-summary").text.replace("\n", "-")
        except Exception as ex:
            print(f"Mistake in size. {ex}")
            card_size = "No data"

        # price
        try:
            # price как мне обратиться к div title="Цена" что бы получить 6 980?
            # try methods     есть путь короче, что бы убрать слэш и стоимость за 4 шины???????????
            # card_price = card.find("div", class_="goodCard-price").text.replace("\n", "").replace("\t", "").replace(" ", "").replace("₽", "").split("/", 1)[0]
            card_price = card.find("div", class_="goodCard-price").text.strip().split("/")[0].strip().replace(" ", "")[:-1]

            # card_price = card.find("div", {"title": "Цена"})
            # card_price = card.find("div[title='Цена']").text

        except Exception as ex:
            print(f"Mistake in price. {ex}")
            card_price = "No data"

        # link on card
        try:
            # не получилось в одну строку
            card_link_long = f"https://www.shinservice.ru{card.find('a', class_='goodCard-titleLink_tire').get('href')}"

            # card_link = card.find("a", class_="goodCard-titleLink_tire").get("href")
            # card_link_long = f"https://www.shinservice.ru{card_link}"
        except Exception as ex:
            print(f"Mistake in link. {ex}")
            card_link_long = "No data"

        # write csv file
        with open("data_shin/all_data_tyres.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                 card_name,
                 card_size,
                 card_price,
                 card_link_long
                )
            )

        # write data for json in variable all_data_tyres
        all_data_tyres.append(
            {
                "brand": card_name,
                "size": card_size,
                "price": card_price,
                "link": card_link_long
            }
        )

        print(f"Марка шины: {card_name}\nРазмер шины: {card_size}\nСтоимость: {card_price}\nСсылка на карточку: {card_link_long}\n")

    # write data in json
    with open("data_shin/all_data_tyres.json", "a") as file:
        json.dump(all_data_tyres, file, indent=4, ensure_ascii=False)


def main():
    get_data()

if __name__ == '__main__':
    main()
# странно открывается index