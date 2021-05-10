import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def crawl_data():
    seasons = {1: 6, 2: 22, 3: 23, 4: 14, 5: 26, 6: 24, 7: 24, 8: 24, 9: 23}
    dialogs = {}

    def addd(c, d):
        dialogs[c] = [d]

    for season in seasons.keys():
        for episode in tqdm(range(1, seasons[season] + 1)):

            if episode < 10:
                url = f"https://www.officequotes.net/no{season}-0{episode}.php"
            else:
                url = f"https://www.officequotes.net/no{season}-{episode}.php"

            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser', )
            dialogues = soup.find_all('div', class_='quote')

            temp = [[t.split(":</b>")[0], re.sub("([\(\[]).*?([\)\]])", "",
                                                 t.split(":</b>")[1].replace('\xa0', '').replace('\u00e2\u20ac\u2122',
                                                                                                 "'").replace('¦',
                                                                                                              ' ').replace(
                                                     'â\x80', "'").replace('\x99', '').strip()).lstrip().strip()] for d
                    in dialogues for t in \
                    str(d).replace('<div class="quote">', '').replace('</div>', '').replace('\t', '').replace(' <b>',
                                                                                                              '').replace(
                        '<b>', '').strip() \
                        .split('<br/>') if "<u>Deleted Scene" not in t and len(t.split(":</b>")) > 1]

            [dialogs[d[0].lower()].append(d[1]) if d[0].lower() in dialogs.keys() else addd(d[0].lower(), d[1]) for d in
             temp]
    print("Finished crawling the data.")
    return dialogs
