# -*- coding: utf-8 -*-

# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

import operator
import os.path
import zipfile
from abc import abstractmethod

from termcolor import cprint, colored


class ProgressBar:
    """
        Класс выводит на консоль индикатор выполнения (progress bar).
        Наверняка такая вещь уже сдалана, но хотел попробовать сделать сам.

        В качестве параметров передаются значения min-value (по умолчанию 0) и max-value (по умолчанию 100)
        С помощью свойства value передается значение для индикатора
        Свойство symbol меняет символ-заполнитель в индикаторе прогресса (по умолчанию заполнитель "*")
        Метод display отображает индикатор.
    """

    def __init__(self, min_value=0, max_value=100):
        self.min_value = min_value
        self.max_value = max_value
        self._value = 0
        self._symbol = '*'
    # TODO Не обязательно делать property c геттером и сеттером. Обычно достаточно переменной экземпляра или класса.
    #  Делать свойство (функцию с декоратором property нужно только в случаях, когда нужно
    #  как то контролировать значение или обрабатывть факт его изменения.
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @value.deleter
    def value(self):
        self._value = 0

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        self._symbol = value

    @symbol.deleter
    def symbol(self):
        self._symbol = '*'

    def display(self):
        percentage = (self.value * 100) / self.max_value
        bar = int(percentage * 0.2) * self.symbol
        print(end='\r')
        print(f'{percentage:>6.2f}% [{bar:<20}]', end='')


class CharCounter:
    """
        Класс подсчитывает количество букв в текстовом файле.
        Принимает в качестве параметра zip-архив c файлом (файлами)

        Обрабатывает случай получения в качестве аргумента не зазипованного текстового файла.

        Метод output выводит результаты подсчета (результаты не сортированы)
    """

    def __init__(self, filename):
        self.filename = filename
        self.path_to_file = ''
        self.symbols = {}
        self._type_of_sorting = 'Не сортировано.'

    def _find_file(self):
        cprint('Ищем входной файл ...', color='yellow')
        for dir_path, dir_names, file_names in os.walk(os.getcwd()):
            if self.filename in file_names:
                self.path_to_file = os.path.join(dir_path, self.filename)
                cprint(f'Файл "{self.filename}" найден в папке "{dir_path}"', color='green')
            else:
                cprint(f'Файл не найден в папке "{dir_path}"', color='red')
        return True if self.path_to_file else False

    @property
    def type_of_sorting(self):
        return self._type_of_sorting

    @type_of_sorting.setter
    def type_of_sorting(self, type_of_sorting: str):
        self._type_of_sorting = type_of_sorting

    @type_of_sorting.deleter
    def type_of_sorting(self):
        self._type_of_sorting = 'Не сортировано.'

    def _count_in_line(self, data):
        """
            Обрабатываем строку
        """
        line = data.decode("cp1251")
        for char in line:
            if char.isalpha():
                if char in self.symbols.keys():
                    self.symbols[char] += 1
                else:
                    self.symbols[char] = 1
            else:
                continue

    def _count_in_file(self, file, file_name, file_size):
        cprint(f'Считаем количество символов в файле "{file_name}" ...', color='cyan')
        data = file.readline()
        self._count_in_line(data=data)
        progress_bar = ProgressBar(max_value=file_size)
        progress_bar.symbol = 'X'
        while data:
            progress_bar.value += len(data)
            progress_bar.display()
            data = file.readline()
            self._count_in_line(data=data)

    @abstractmethod
    def _sorting(self):
        pass

    def _count(self):

        if not self._find_file():
            return False

        if zipfile.is_zipfile(self.path_to_file):
            with zipfile.ZipFile(self.path_to_file) as zip_file:
                for file_name in zip_file.namelist():
                    file_info = zip_file.getinfo(file_name)  # Получаем информацию о файле
                    with zip_file.open(file_name) as file:
                        self._count_in_file(file, file_name, file_info.file_size)
        else:
            with open(self.path_to_file, 'rb') as file:
                file_size = os.path.getsize(self.path_to_file)  # Получаем информацию о размере файла
                path, file_name = os.path.split(self.path_to_file)  # Получаем информацию об имени файла
                self._count_in_file(file, file_name, file_size)

        cprint('\nВсе подсчитано.', color='cyan')
        return True

    @staticmethod
    def _print_header():
        print('+' + '-' * 10 + '+' + '-' * 10 + '+')
        print(f"|{'Буква':^10}|{'Частота':^10}|")
        print('+' + '-' * 10 + '+' + '-' * 10 + '+')

    @staticmethod
    def _print_footer():
        print('+' + '-' * 10 + '+' + '-' * 10 + '+')

    def output(self):

        if self._count():
            cprint(f'Выводим результаты подсчета (Тип сортировки - {self._type_of_sorting}):', color='yellow')
        else:
            cprint('Не найден входной файл!', color='red')
            return

        # Шапка таблицы
        self._print_header()

        # Содержимое таблицы
        self._sorting()

        # Подвал таблицы
        self._print_footer()


# После выполнения первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828


class CharCounterSortedAlphabet(CharCounter):
    """
        Класс переопределяет метод output из класса CharCounter
        Метод output выводит результаты подсчета отсортированые по алфавиту (по возрастанию)
    """

    def _sorting(self):
        keys = list(self.symbols.keys())  # Создаем лист из ключей словаря self.symbol

        keys.sort()  # Сортируем лист по возрастанию
        for k in keys:
            print(f"|{k:^10}|{self.symbols[k]:>10}|")


class CharCounterSortedAlphabetReverse(CharCounter):
    """
        Класс переопределяет метод output из класса CharCounter
        Метод output выводит результаты подсчета отсортированые по алфавиту (по убыванию)
    """

    def _sorting(self):
        keys = list(self.symbols.keys())  # Создаем лист из ключей словаря self.symbol

        keys.sort(reverse=True)  # Сортируем лист по убыванию
        for k in keys:
            print(f"|{k:^10}|{self.symbols[k]:>10}|")


class CharCounterSortedQuantity(CharCounter):
    """
        Класс переопределяет метод output из класса CharCounter
        Метод output выводит результаты подсчета отсортированые по частоте использования (по возрастанию)
    """

    def _sorting(self):
        items = list(self.symbols.items())  # Создаем лист кортежей типа (key, value) из словаря self.symbol

        items.sort(key=operator.itemgetter(1))  # Сортируем лист (по возрастанию) по второму элементу кортежа
        for k, value in items:
            print(f"|{k:^10}|{value:>10}|")


class CharCounterSortedQuantityReverse(CharCounter):
    """
        Класс переопределяет метод output из класса CharCounter
        Метод output выводит результаты подсчета отсортированые по частоте использования (по убыванию)
    """

    def _sorting(self):
        items = list(self.symbols.items())  # Создаем лист кортежей типа (key, value) из словаря self.symbol

        items.sort(key=operator.itemgetter(1), reverse=True)  # Сортируем лист (по убыванию) по второму элементу кортежа
        for k, value in items:
            print(f"|{k:^10}|{value:>10}|")


if __name__ == '__main__':
    choice = {
              '1': ['Сортировка по алфавиту - по возрастанию', CharCounterSortedAlphabet],
              '2': ['Сортировка по алфавиту - по убыванию', CharCounterSortedAlphabetReverse],
              '3': ['Сортировка по частоте использования - по возрастанию', CharCounterSortedQuantity],
              '4': ['Сортировка по частоте использования - по убыванию', CharCounterSortedQuantityReverse],
              }

    cprint('Варианты сортировки:', color='yellow')

    while True:
        for key, item in choice.items():
            cprint(f'{key}: {item[0]}', color='cyan')
        selected = input(colored('Выберите вариант сортировки: ', color='cyan'))
        if selected in choice.keys():
            break

    counter = choice[selected][1]('voyna-i-mir.txt.zip')
    # TODO Возможно я не совсем понятно доносил до вас этот момент при предыдущих проверках, но
    #  то что сейчас называется type_of_sorting лучше сделать переменной класса. Логика в том,
    #  что название сортировки должно быть одинаково у всех экземпляров этого класса.
    #  Это позволит в choice хранить только ссылку на класс, и при необходимости ее извлекать.
    #  Например, если type_of_sorting заменить на name, то получится:
    #  for key, counter in choice.items():
    #      cprint(f'{key}: {counter.name}', color='cyan')

    counter.type_of_sorting = choice[selected][0]  # А если вот так! :-) - Переименовал свойство и теперь использую.
    counter.output()
