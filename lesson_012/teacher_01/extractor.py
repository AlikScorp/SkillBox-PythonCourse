# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from urllib.parse import urlsplit, urlunsplit, urljoin


class LinksExtractor(HTMLParser):

    def __init__(self, base_url, *args, **kwargs):
        super(LinksExtractor, self).__init__(*args, **kwargs)
        self.links = []
        self._attrs = None
        self.base_url = base_url
        scheme, netloc, path, query, fragment = urlsplit(self.base_url)
        self.netloc = netloc

    def handle_starttag(self, tag, attrs):
        self._attrs = dict(attrs)
        if tag == 'a':
            self._handle_ahref()

    def _handle_ahref(self):
        if 'href' in self._attrs:
            url = self._refine_url(url=self._attrs['href'])
            if url:
                self.links.append(url)

    def _refine_url(self, url):
        scheme, netloc, path, query, fragment = urlsplit(url)
        if scheme and scheme not in ('http', 'https', ):
            return
        if netloc and netloc != self.netloc:
            # внешняя ссылка
            return
        if path.endswith('wmv'):
            # видео не качаем
            return
        url = urljoin(self.base_url, url)
        return url