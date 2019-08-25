# -*- coding: utf-8 -*-
import random
import threading
# Реализовать поиск битых ссылок из первого задания в МНОГОПОТОЧНОМ стиле
#
import time
from collections import defaultdict

import requests

from extractor import LinksExtractor
from utils import time_track

# SITE_URL = 'http://museum.moex.com'
SITE_URL = 'http://museum.moex.com/collect/exhibits/mechs/show_exponat/index_id=moneybox_20kop.html'
MAX_DEEP = 3
MAX_CONNECTS = 16


class LinksDepot:

    def __init__(self, first_url):
        self._links_lock = threading.RLock()
        self._next_links = dict()
        self._visited_links = dict()
        self.bad_links = defaultdict(list)
        self.add_link(url=first_url, ref=None, deep=1)

    @property
    def links(self):
        with self._links_lock:
            return set(self._next_links) | set(self._visited_links)

    def add_link(self, url, ref, deep):
        if deep > MAX_DEEP:
            return
        with self._links_lock:
            self._next_links[url] = dict(ref=ref, deep=deep)

    def get_next_link(self):
        with self._links_lock:
            try:
                url, data = self._next_links.popitem()
            except KeyError:
                return None
            self._visited_links[url] = data
        return dict(url=url, ref=data['ref'], deep=data['deep'])

    def set_broken(self, url):
        with self._links_lock:
            if url in self._visited_links:
                ref = self._visited_links[url]['ref']
                self.bad_links[ref].append(url)


class CanLog:
    _id = None
    _id_lock = threading.RLock()

    @property
    def id(self):
        if self._id is None:
            kls = self.__class__
            with self._id_lock:
                if not hasattr(kls, '_ids_counter'):
                    kls._ids_counter = 0
                kls._ids_counter += 1
            self._id = kls._ids_counter
        return self._id

    def _log(self, text):
        print(f'{self.__class__.__name__}-{self.id}: {text}')


class Scavenger(threading.Thread, CanLog):

    def __init__(self, depot, url, ref=None, deep=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.ref = ref
        self.deep = deep
        self.depot = depot
        self.extra_links = None
        self.is_broken = False

    def run(self):
        time.sleep(random.randint(1, 10) / 100)
        self._log(f'Go {self.url}...')
        res = requests.get(self.url)
        if res.status_code != 200:
            self._log(f'\t{self.url} status_code is {res.status_code}')
            self.is_broken = True
            return
        if self.deep + 1 > MAX_DEEP:
            self._log('Max deep reached')
            return
        html_data = res.text
        parser = LinksExtractor(base_url=self.url)
        parser.feed(data=html_data)
        self.extra_links = set(parser.links) - self.depot.links
        self._log(f'\tIn {self.url} {len(self.extra_links)} extra_links')

    def _log(self, text):
        print(f'{self.__class__.__name__}-{self.id} [deep {self.deep}]: {text}')


class Manager(CanLog):

    def __init__(self, depot):
        self.depot = depot
        self.workers = []

    def run(self):
        self.start_workers()
        while self.workers:
            time.sleep(0.01)
            ended = self._get_ended()
            if ended:
                self.take_data(ended)
                self.start_workers()
        with open('links_with_threads.log', 'w', encoding='utf8') as links_log:
            links_log.write('\n'.join(sorted(self.depot.links)))

    def start_workers(self):
        started = 0
        while len(self.workers) < MAX_CONNECTS:
            link = self.depot.get_next_link()
            if not link:
                break
            sc = Scavenger(depot=self.depot, **link)
            sc.start()
            self.workers.append(sc)
            started += 1
        if started:
            self._log(f'started {started} workers')

    def _get_ended(self):
        ended_indexes = []
        for i, scav in enumerate(self.workers):
            if not scav.is_alive():
                ended_indexes.append(i)
        ended = []
        for i in ended_indexes[::-1]:
            scav = self.workers.pop(i)
            ended.append(scav)
        if ended:
            self._log(f'found {len(ended)} ended workers')
        return ended

    def take_data(self, ended):
        for worker in ended:
            if worker.is_broken:
                self.depot.set_broken(worker.url)
            elif worker.extra_links:
                for url in worker.extra_links:
                    self.depot.add_link(url=url, ref=worker.url, deep=worker.deep + 1)


@time_track
def main():
    depot = LinksDepot(first_url=SITE_URL)
    manager = Manager(depot=depot)
    manager.run()
    for ref in sorted(depot.bad_links):
        urls = depot.bad_links[ref]
        print(f'Страница {ref}, сломанных ссылок - {len(urls)}')
        for link in sorted(urls):
            print(f'\t{link}')


if __name__ == '__main__':
    main()
