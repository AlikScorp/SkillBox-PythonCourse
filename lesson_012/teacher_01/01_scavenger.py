# -*- coding: utf-8 -*-


# Задача: проверить битые ссылки у сайта (https://goo.gl/cfJ9ip)
# То есть написать мусорщика, который ищет мусор на сайте.
#
# 1. получить html
# 2. узнать какие _внутренние_ ссылки есть на страничке (ссылка ведет на странцу рассматриваемого сайта)
# 3. пройти по этим ссылкам,
# 3. если ссылка битая (код ответа 404) то занести её в хранилище битых ссылок:
#   на какой странице обнаружена, собственно ссылка
# 4. если ссылка не битая и ведет на html страницу, то получить html и перейти к шагу 2.
# 6. вывести на консоль результаты в виде:
#
# Страница ХХХ, сломанных ссылок - N:
#       собственно ссылка
#       собственно ссылка
#       собственно ссылка
#       собственно ссылка
# Страница YYY, сломанных ссылок - K:
#       собственно ссылка
#       собственно ссылка
#
# Обратите внимание! Надо считать глубину перехода по ссылкам
# и следить что бы наш краулер не сильно заглубился в сайт - не более MAX_DEEP страниц от первоначальной
#
# Желательно вынести в отдельные модули вспомогательные классы и функции
from collections import defaultdict

import requests
from extractor import LinksExtractor
from utils import time_track

# SITE_URL = 'http://museum.moex.com'
SITE_URL = 'http://museum.moex.com/collect/exhibits/mechs/show_exponat/index_id=moneybox_20kop.html'
MAX_DEEP = 3


class Scavenger:
    bad_links = defaultdict(set)
    visited_links = set()
    count = 0

    def __init__(self, url, ref=None, deep=1):
        self.url = url
        self.ref = ref
        self.deep = deep
        Scavenger.count += 1
        self.id = Scavenger.count

    def run(self):
        self._log(f'Go {self.url}...')
        res = requests.head(self.url)
        if res.status_code != 200:
            self._log(f'\tIn {self.url} status_code is {res.status_code}')
            Scavenger.bad_links[self.ref].add(self.url)
            return
        if self.deep + 1 > MAX_DEEP:
            self._log(f'Max deep reached')
            return
        res = requests.get(self.url)
        html_data = res.text
        parser = LinksExtractor(base_url=self.url)
        parser.feed(data=html_data)
        page_links = set(parser.links)
        extra_links = page_links - Scavenger.visited_links
        self._log(f'\tIn {self.url} {len(extra_links)} extra_links')
        for link in extra_links:
            Scavenger.visited_links.add(link)
            scav = Scavenger(url=link, ref=self.url, deep=self.deep + 1)
            scav.run()

    def _log(self, text):
        print(f'{self.id}-{self.deep}: {text}')

@time_track
def main():
    scav = Scavenger(url=SITE_URL)
    scav.run()
    for ref in sorted(Scavenger.bad_links):
        urls = Scavenger.bad_links[ref]
        print(f'Страница {ref}, сломанных ссылок - {len(urls)}')
        for link in sorted(urls):
            print(f'\t{link}')
    with open('links_single.log', 'w', encoding='utf8') as links_log:
        links_log.write('\n'.join(sorted(Scavenger.visited_links)))


if __name__ == '__main__':
    main()
