# -*- coding: utf-8 -*-

# Реализовать поиск битых ссылок из первого задания в МНОГОПРОЦЕССНОМ стиле
#
import os
import queue
from collections import defaultdict
from multiprocessing import Process, Queue

import requests

from extractor import LinksExtractor
from utils import time_track

# SITE_URL = 'http://museum.moex.com'
SITE_URL = 'http://museum.moex.com/collect/exhibits/mechs/show_exponat/index_id=moneybox_20kop.html'
MAX_DEEP = 3
MAX_CONNECTS = 16


class Link:

    def __init__(self, url, ref, deep):
        self.url = url
        self.ref = ref
        self.deep = deep
        self.is_broken = False
        self.next_urls = []

    def __str__(self):
        return f'Link {self.deep} {len(self.next_urls)} {self.url}'


class ProcessCanLog:

    def _log(self, text):
        _pid = os.getpid()
        print(f'{self.__class__.__name__}-{_pid}: {text}')


class Scavenger(Process, ProcessCanLog):

    def __init__(self, receiver, link, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.link = link
        self.receiver = receiver

    def run(self):
        self._log(f'Go {self.link.url}...')
        res = requests.head(self.link.url)
        if res.status_code != 200:
            self._log(f'\t{self.link.url} status_code is {res.status_code}')
            self.link.is_broken = True
            self.receiver.put(self.link)
            return
        if self.link.deep + 1 > MAX_DEEP:
            self._log('Max deep reached')
            return
        res = requests.get(self.link.url)
        html_data = res.text
        parser = LinksExtractor(base_url=self.link.url)
        parser.feed(data=html_data)
        self.link.next_urls = parser.links
        self._log(f'\tIn {self.link.url} {len(self.link.next_urls)} links')
        self.receiver.put(self.link)

    def _log(self, text):
        _pid = os.getpid()
        print(f'{self.__class__.__name__}-{_pid}-{self.link.deep}: {text}')


class Manager(ProcessCanLog):

    def __init__(self, start_url):
        self.links = {start_url: Link(url=start_url, ref=None, deep=1)}
        self.visited = dict()
        self.bad_links = defaultdict(list)
        self.queue = Queue()
        self.workers = []

    def run(self):
        self.start_workers()
        while self.workers:
            try:
                link = self.queue.get(timeout=1)
                self._log(f'Getted {link}')
                self.take_data(link)
            except queue.Empty:
                self._log(f'Queue empty')
                pass
            ended = self._get_ended()
            if ended:
                self.start_workers()
        with open('links_with_processes.log', 'w', encoding='utf8') as links_log:
            links_log.write('\n'.join(sorted(self.visited)))

    def start_workers(self):
        started = 0
        while len(self.workers) < MAX_CONNECTS:
            link = self.get_next_link()
            if not link:
                break
            sc = Scavenger(receiver=self.queue, link=link)
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

    def take_data(self, link):
        if link.is_broken:
            self.bad_links[link.ref].append(link.url)
        elif link.deep + 1 > MAX_DEEP:
            return
        elif link.next_urls:
            extra_links = set(link.next_urls) - set(self.links) - set(self.visited)
            self._log(f'found {len(extra_links)} extra_links')
            for url in extra_links:
                new_link = Link(url=url, ref=link.url, deep=link.deep + 1)
                self.links[url] = new_link

    def get_next_link(self):
        try:
            url, link = self.links.popitem()
            self.visited[url] = link
            return link
        except KeyError:
            return None


@time_track
def main():
    manager = Manager(start_url=SITE_URL)
    manager.run()
    for ref in sorted(manager.bad_links):
        urls = manager.bad_links[ref]
        print(f'Страница {ref}, сломанных ссылок - {len(urls)}')
        for link in sorted(urls):
            print(f'\t{link}')


if __name__ == '__main__':
    main()
