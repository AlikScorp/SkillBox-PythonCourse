# -*- coding: utf-8 -*-


# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
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
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от средней цены за торговую сессию:
#   средняя цена = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / средняя цена) * 100%
# Например для бумаги №1:
#   average_price = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / average_price) * 100 = 8.7%
# Для бумаги №2:
#   average_price = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / average_price) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
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
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#
# class <Название класса>:
#
#     def __init__(self, <параметры>):
#         <сохранение параметров>
#
#     def run(self):
#         <обработка данных>
import operator
import os


class Storage:
    """
        Данный класс хранит результаты парсинга файлов тикеров с результатами сделок.
        Анализирует словарь с результатами, выводит по три тикера с максимальной и минимальной волатильностью
        и список тикеров с нулевой волатильностью.
    """

    def __init__(self):
        self.storage: dict = {}
        self.ordered_list: list = []
        self.volatility_zero: list = []

    def append(self, ticker_data: tuple):
        """
            Метод принемает кортеж типа {тикер, волатильность} и добавляет полученную информацию в словарь,
            где ключем является тикер, а значением волатильность.
        :param ticker_data: Кортеж с информацией о тикере и его волатильности
        :return: None
        """
        if ticker_data[1] == 0:
            self.volatility_zero.append(ticker_data[0])
            return

        self.storage[ticker_data[0]] = ticker_data[1]

    def sorting(self):
        """
            Метод сортирует имеющийся словарь тикеров.
            В результате создает список с отсортированными (по волатильности) по убыванию тикерами.
        :return: False в случае если словарь пуст и сортировка невозможна. True если сортировка произведена.
        """
        if not self.storage:
            return False

        self.ordered_list = sorted(self.storage.items(), key=operator.itemgetter(1), reverse=True)

        return True

    def display(self):
        """
            Метод выводит информацию о трех тикерах с максимальной волатильностью,
            трех тикеров с минимальной волатильностью и список тикеров с нулевой волатильностью.
        :return: None
        """

        if not self.ordered_list:
            if not self.sorting():
                print('В хранилище пусто!!!')
                return

        print('Максимальная волатильность:')
        for ticker, price in self.ordered_list[:3]:
            print(f'\t{ticker} - {price:3.2f} %')

        print('Минимальная волатильность:')
        for ticker, price in self.ordered_list[-3:]:
            print(f'\t{ticker} - {price:3.2f} %')

        print('Нулевая волатильность:')
        volatility_zero_sorted = sorted(self.volatility_zero)
        vol_zero_string = ', '.join(volatility_zero_sorted)

        print(f'\t{vol_zero_string}')


class VolatilityCounter:
    """
        Класс считает волатильность одного тикера.
        В качестве параметра принемает файл тикера с результатами сделок и экземплят класса Storage для хранения
        данных по подсчету волатильности.
        Результат вычислений заносит в экземляр класса Storage.
    """

    def __init__(self, file_name: str, data_storage: Storage):
        self.file_name: str = file_name
        self.max_price: float = 0
        self.min_price: float = 0
        self.volatility: float = 0
        self.storage = data_storage

    def run(self):
        """
            Метод открывает файл с результатами торгов по одному тикеру, собирает информацию о всех ценах за тикер,
            Определяет минимальную и максимальную цены, высчитывает волатильность и заносит информацию в хранилище
        :return:
        """

        with open(self.file_name, 'r', encoding='utf8') as f:
            f.readline()
            for line in f:
                ticker_id, trade_time, price, quantity = line.split(',')
                price = float(price)

                if self.max_price == 0:
                    self.max_price = price
                else:
                    self.max_price = price if self.max_price < price else self.max_price

                if self.min_price == 0:
                    self.min_price = price
                else:
                    self.min_price = price if self.min_price > price else self.min_price

        self.volatility = 200 * (self.max_price - self.min_price)/(self.max_price + self.min_price)

        self.storage.append((ticker_id, self.volatility, 2))


def main():
    storage = Storage()

    for root, folders, files in os.walk('trades'):
        for file in files:
            path_to_file = os.path.join(os.getcwd(), root, file)
            if os.path.isfile(path_to_file):
                vol = VolatilityCounter(path_to_file, storage)
                vol.run()

    storage.display()


if __name__ == '__main__':
    main()