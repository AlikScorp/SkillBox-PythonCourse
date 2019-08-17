# -*- coding: utf-8 -*-

# На основе своего кода из lesson_009/02_log_parser.py напишите итератор (или генератор)
# котрый читает исходный файл events.txt и выдает число событий NOK за каждую минуту
# <время> <число повторений>
#
# пример использования:
#
# grouped_events = <создание итератора/генератора>
# for group_time, event_count in grouped_events:
#     print(f'[{group_time}] {event_count}')
#
# на консоли должно появится что-то вроде
#
# [2018-05-17 01:57] 1234
from termcolor import cprint


class LogParser:

    def __init__(self, filename: str):
        self.result, self.count = '', 0
        self.filename = filename

    def __iter__(self):
        self.result = ''
        self.count = 0

        try:
            self.file = open(self.filename, 'r', encoding='utf8')
        except IOError:
            cprint(f"Cannot find the file '{self.filename}'", color='red')
            raise SystemExit  # Вызываем исключение, поднимаемое sys.exit(), для остановки работы интерпретатора.

        return self

    def __next__(self) -> tuple:

        for line in self.file:
            date, time, status = line.split(' ')
            if status[:-1] == 'NOK':
                result = ' '.join([date[1:], time[:5]])

                if self.result == '':
                    self.result = result
                    self.count += 1
                elif self.result == result:
                    self.count += 1
                else:
                    self.result, result = result, self.result
                    count = self.count
                    self.count = 1
                    return result, count
        else:
            self.file.close()
            raise StopIteration  # Вызываем исключение, сигнализирующее, что итератор исчерпал доступные значения.


def log_parser(filename: str) -> tuple:
    """
        Функция-генератор. В качестве параметра принемает имя файла для парсинга.
    :param filename: Имя входного файла
    :return: Возвращает кортеж следующего вида: ("[2018-05-17 01:57", 1234)
    """
    count = 0
    key = ''

    try:
        file = open(filename, 'r', encoding='utf8')
    except IOError:
        cprint(f'Cannot open file {filename}', color='red')
        raise SystemExit  # Вызываем исключение, поднимаемое sys.exit(), для остановки работы интерпретатора.
    else:
        for line in file:
            date, time, status = line.split(' ')
            if status[:-1] == 'NOK':
                result = ' '.join([date[1:], time[:5]])

                if key == '':
                    key = result
                    count += 1
                elif key == result:
                    count += 1
                else:
                    key, result = result, key
                    count, final_count = 1, count
                    yield result, final_count
        else:
            file.close()


if __name__ == '__main__':
    grouped_events = LogParser(filename='events.txt')  # Можно использовать класс-итератор
    # grouped_events = log_parser(filename='events.txt')  # А можно функцию-генератор :-)
    for group_time, event_count in grouped_events:
        print(f'[{group_time}] {event_count}')
