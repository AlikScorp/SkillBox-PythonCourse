# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

import os.path
from termcolor import cprint


class LogParser:

    def __init__(self, log_name):
        self.results = {}
        if os.path.exists(log_name):
            self.log = log_name
        else:
            cprint(f'Не могу найти файл по указанному пути: "{log_name}".', color='red')
            self.log = ''

    def _count(self):
        if not self.log:
            cprint('Не определен входной файл!', color='red')
            return

        with open(self.log, 'r', encoding='cp1251') as file:
            for line in file:
                date, time, status = line.split(' ')
                if status[:-1] == 'NOK':
                    result = '['+' '.join([date[1:], time[:5]])+']'

                    if result in self.results.keys():
                        self.results[result] += 1
                    else:
                        self.results[result] = 1

    def output(self):
        self._count()

        with open('output.txt', 'w', encoding='cp1251') as file:
            for result in self.results:
                output_string = ' '.join([result, str(self.results[result])])+'\n'
                file.write(output_string)


class LogParserHours(LogParser):

    def _count(self):

        if not self.log:
            cprint('Не определен входной файл!', color='red')
            return

        with open(self.log, 'r', encoding='cp1251') as file:
            for line in file:
                date, time, status = line.split(' ')
                if status[:-1] == 'NOK':
                    result = '['+' '.join([date[1:], time[:2]])+']'

                    if result in self.results.keys():
                        self.results[result] += 1
                    else:
                        self.results[result] = 1


class LogParserMonths(LogParser):

    def _count(self):

        if not self.log:
            cprint('Не определен входной файл!', color='red')
            return

        with open(self.log, 'r', encoding='cp1251') as file:
            for line in file:
                date, time, status = line.split(' ')
                if status[:-1] == 'NOK':
                    result = '['+' '.join([date[1:8]])+']'

                    if result in self.results.keys():
                        self.results[result] += 1
                    else:
                        self.results[result] = 1


class LogParserYears(LogParser):

    def _count(self):

        if not self.log:
            cprint('Не определен входной файл!', color='red')
            return

        with open(self.log, 'r', encoding='cp1251') as file:
            for line in file:
                date, time, status = line.split(' ')
                if status[:-1] == 'NOK':
                    result = '['+' '.join([date[1:5]])+']'

                    if result in self.results.keys():
                        self.results[result] += 1
                    else:
                        self.results[result] = 1


if __name__ == '__main__':
    log_parser = LogParserHours('events.txt')
    log_parser.output()

# После выполнения первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
