import os
import time
import requests

from telegram import Bot
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from PIL import Image

load_dotenv()


URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


def parse_page():
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    all_wins = soup.find_all(class_='match-card win')
    all_wins += soup.find_all(class_='match-card even win')
    stats = []
    for data in all_wins:
        for name in data.find_all('a', class_='name'):
            name_text = name.text
        for kda in data.find_all('div', class_='kda'):
            kda_text = kda.text
        for items in data.find(
            'div',
            class_="grid-item grid-item-champion-items"
        ):
            item_pic_urls = []
            all_items = items.find_all('div', class_='item-image')
            for item in all_items:
                item_pic = item.find('img')
                if item_pic is not None:
                    item_pic_url = item_pic['src']
                    item_pic_urls.append(item_pic_url)
        stats.append([name_text, kda_text, item_pic_urls])
    return stats


def compare_and_cache(cache, stats):
    new_stats = []
    if not cache:
        cache = stats
        new_stats = stats
        return cache, new_stats
    if len(cache) > 20:
        cache.pop()
    for stat in stats:
        if stat not in cache:
            cache.append(stat)
            new_stats.append(stat)
    return cache, new_stats


def build_image(stat):
    new_img = Image.new('RGB', (64*len(stat[2]), 64))
    img_ulrs = stat[2]
    for url in img_ulrs:
        img_data = requests.get(url).content
        with open('temp.jpg', 'wb') as handler:
            handler.write(img_data)
        img = Image.open('temp.jpg')
        new_img.paste(img, (64*img_ulrs.index(url), 0))
    new_img.save('out.jpg')


def main():
    cache = []
    bot = Bot(TOKEN)
    while True:
        cache, new_stats = compare_and_cache(cache, parse_page())
        for stat in new_stats:
            caption = f'{stat[0]}, {stat[1]}'
            build_image(stat)
            photo = open('out.jpg', 'rb')
            bot.send_photo(chat_id=CHAT_ID, caption=caption, photo=photo)
        time.sleep(600)


if __name__ == '__main__':
    main()
