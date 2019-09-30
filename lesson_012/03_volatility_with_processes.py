# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
#
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
import operator
import os
import multiprocessing


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
        else:
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


class VolatilityCounter(multiprocessing.Process):
    """
        Класс считает волатильность одного тикера.
        В качестве параметра принемает файл тикера с результатами сделок и экземплят класса Storage для хранения
        данных по подсчету волатильности.
        Результат вычислений заносит в экземляр класса Storage.
    """

    def __init__(self, file_name: str, pipe, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_name: str = file_name
        self.max_price: float = 0
        self.min_price: float = 0
        self.volatility: float = 0
        self.ticker_id = ''
        self.pipe = pipe

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

        volatility = 200 * (self.max_price - self.min_price)/(self.max_price + self.min_price)

        self.ticker_id = ticker_id
        self.volatility = volatility

        self.pipe.send((self.ticker_id, self.volatility))
        self.pipe.close()
        print(f'Подсчет волатильности для тикера {self.ticker_id} закончен, '
              f'волатильность равна: {self.volatility:>5.2f}%')


def main():
    storage = Storage()
    processes: list = []
    pipes: list = []

    for root, folders, files in os.walk('trades'):
        for file in files:
            path_to_file = os.path.join(os.getcwd(), root, file)
            if os.path.isfile(path_to_file):
                parent_con, child_con = multiprocessing.Pipe(duplex=False)    # Создаем трубу для получения результатов.
                processes.append(VolatilityCounter(path_to_file, child_con))  # Один конец передаем процессу,
                pipes.append(parent_con)                                      # другой сохраняем в списке

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    for pipe in pipes:                          # После завершения процессов считываем из труб результаты
        storage.append(pipe.recv())             # и заносим их в Storage.

    storage.display()


if __name__ == '__main__':
    main()
