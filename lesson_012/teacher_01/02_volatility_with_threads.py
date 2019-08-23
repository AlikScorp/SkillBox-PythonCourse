# -*- coding: utf-8 -*-


# Описание предметной области: при торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величена изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 2, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от средней цены за торговую сессию:
#   средняя цена = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / средняя цена) * 100%
# Например для бумаги №1:
#   average_price = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / average_price) * 100 = 8.7%
# Для бумаги №2:
#   average_price = (100 + 2) / 2 = 51
#   volatility = ((100 - 2) / average_price) * 100 = 192.16%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
# Волатильности указывать в порядке убывания.
#
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1ZbFS5j67vO9PlDbu0MrnDiOe0fGaxkox/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base_source/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.

import csv
import os
import threading
import time
from pprint import pprint

from utils import time_track

SOURCE_PATH = os.path.join(os.path.dirname(__file__), 'trades')


def files(path):
    for currnt_path, dirs, files in os.walk(path):
        for filename in files:
            full_filename = os.path.join(currnt_path, filename)
            yield full_filename


def get_lines(filename):
    headers = None
    with open(filename, 'r') as ff:
        reader = csv.reader(ff)
        for _line in reader:
            if headers is None:
                headers = _line
                continue
            yield dict(zip(headers, _line))


class Runner(threading.Thread):

    def __init__(self, filename, tickers, tickers_lock):
        super(Runner, self).__init__()
        self.filename = filename
        self.tickers = tickers
        self.tickers_lock = tickers_lock

    def run(self):
        secid, min_val, max_val = None, None, None
        for line in get_lines(self.filename):
            if secid is None:
                secid = line['SECID']
            price = float(line['PRICE'])
            if min_val is None or min_val > price:
                min_val = price
            if max_val is None or max_val < price:
                max_val = price
        if min_val and max_val:
            average_price = (max_val + min_val) / 2
            volatility = ((max_val - min_val) / average_price) * 100
            print(f'{self.ident}', secid, min_val, max_val, average_price, volatility)
            with self.tickers_lock:
                self.tickers.append(
                    [round(volatility, 2), secid]
                )


@time_track
def main():
    tickers = []
    workers = []
    lock = threading.RLock()
    for filename in files(SOURCE_PATH):
        runner = Runner(filename=filename, tickers=tickers, tickers_lock=lock)
        runner.start()
        workers.append(runner)
    alive_workers = [w for w in workers if w.is_alive()]
    while alive_workers:
        print(f'Alive {len(alive_workers)} workers')
        time.sleep(.001)
        alive_workers = [w for w in workers if w.is_alive()]

    tickers.sort()
    zero_volat_tickers = []
    nonzero_index = 0
    for volatility, secid in tickers:
        if volatility != 0:
            break
        nonzero_index += 1
        zero_volat_tickers.append(secid)
    tickers = tickers[nonzero_index:]
    tickers.reverse()

    # pprint(zero_volat_tickers)
    # pprint(tickers)

    print('Максимальная волатильность:')
    for volatility, secid in tickers[:3]:
        print(f'\t{secid} - {volatility}%')

    print('Минимальная волатильность:')
    for volatility, secid in tickers[-3:]:
        print(f'\t{secid} - {volatility}%')

    print('Нулевая волатильность:')
    zero_tickers = ', '.join(zero_volat_tickers)
    print(f'\t{zero_tickers}')


if __name__ == '__main__':
    main()

# Максимальная волатильность:
# 	SiH9 - 24.39%
# 	PDM9 - 23.2%
# 	PDH9 - 22.69%
# Минимальная волатильность:
# 	RNU9 - 0.98%
# 	GOG9 - 0.97%
# 	CHM9 - 0.95%
# Нулевая волатильность:
# 	CLM9, CYH9, EDU9, EuH0, EuZ9, JPM9, MTM9, O4H9, PDU9, PTU9, RIH0, RRG9, TRH9, VIH9
# Функция работала 2.4044 секунд(ы)
