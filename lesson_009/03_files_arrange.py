# -*- coding: utf-8 -*-
import datetime
import os
import time
import shutil
import zipfile

from termcolor import cprint

# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени создания файла.
# Обработчик файлов делать в обьектном стиле - на классах.
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.


class FileSorter:
    """
        Абстрактный класс для сортировки файлов из переданного ему источника.
        Источник определяется в методе _sort.

        Папки назначения создаются на основании даты создания файлов в источнике.
    """

    def __init__(self, source, destination):

        self.source = source
        self.destination = destination

    def _check_destination(self):

        if os.path.isdir(self.destination):
            cprint(f'Папка назначения "{self.destination}" найдена.', color='yellow')
        else:
            cprint(f'Папка назначения "{self.destination}" не найдена. Создаем папку...', color='yellow')
            os.makedirs(self.destination)

    def _sort(self):
        pass

    def start(self):
        self._sort()

# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Основная функция должна брать параметром имя zip-файла и имя целевой папки.
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828


class FileSorterFromDir(FileSorter):
    """
        Класс "раскидывает" по папкам файлы из переданного ему источника.
        Источником является папка с файлами.

        Папки назначения создаются на основании даты создания файлов в источнике.
    """

    def _sort(self):

        if os.path.isdir(self.source):
            cprint(f'Исходящая папка "{self.source}" найдена', color='yellow')
        else:
            cprint(f'Исходящая папка "{self.source}" не найдена. Продолжение работы невозможно.', color='red')
            return

        self._check_destination()

        cprint(f'Копируем файлы из папки "{self.source}" в папку "{self.destination}":', color='yellow')
        counter = 0

        for dir_path, dir_names, file_names in os.walk(self.source):
            for file in file_names:
                path_to_file = os.path.join(dir_path, file)
                timestamp = os.path.getmtime(path_to_file)
                date = time.gmtime(timestamp)
                destination = os.path.join(self.destination, str(date[0]), str(date[1]), str(date[2]))

                os.makedirs(destination, exist_ok=True)

                # Выводим индикатор выполнения, чтобы небыло скучно ждать :-)
                if counter == 10:
                    print('X', end='')
                    counter = 0
                else:
                    counter += 1

                shutil.copy2(path_to_file, destination)

        print()
        cprint('Все готово!', color='yellow')


class FileSorterFromZip(FileSorter):
    """
        Класс "раскидывает" по папкам файлы из переданного ему источника.
        Источником является ZIP-архив. Файлы обрабатываются без предварительной распаковки архива.

        Папки назначения создаются на основании даты создания файлов в источнике.
        Поскольку при "раскидывании" файлы, оноименные заархивированным, создаются заново - оригинальные метаданные
        не сохраняются :-(
    """

    def _sort(self):

        if os.path.exists(self.source):
            cprint(f'Файл "{self.source}" найден.', color='yellow')
        else:
            cprint(f'Файл "{self.source}" не найден. Продолжение невозможно.', color='red')
            return

        self._check_destination()

        cprint(f'Копируем файлы из архива "{self.source}" в папку "{self.destination}":', color='yellow')
        counter = 0

        if zipfile.is_zipfile(self.source):
            with zipfile.ZipFile(self.source) as zip_file:
                for file in zip_file.namelist():
                    file_info = zip_file.getinfo(file)
                    if not file_info.is_dir():
                        path_to_file, filename = os.path.split(file)
                        date_time = file_info.date_time
                        path = os.path.join(self.destination, str(date_time[0]), str(date_time[1]), str(date_time[2]))

                        result = zip_file.open(file)  # Открываем файл из архива
                        os.makedirs(path, exist_ok=True)  # создаем все необходимые папки
                        file_name = os.path.join(path, filename)  # Определяем полный путь к файлу

                        with open(file_name, 'wb') as outfile:
                            shutil.copyfileobj(result, outfile)  # Записываем данные из архива в файл

                        file_datetime = datetime.datetime(*date_time)  # Создаем объект для хранения метаданных
                        file_meta_data = file_datetime.timestamp()  # Конвертируем в timestamp
                        os.utime(file_name, (file_meta_data, file_meta_data))  # Записываем метаданные в файл.

                    # Вышенаписанное - какоето жонглирование данными. :-(

                    # Выводим индикатор выполнения, чтобы небыло скучно ждать :-)
                    if counter == 10:
                        print('X', end='')
                        counter = 0
                    else:
                        counter += 1
        else:
            cprint(f'Входящий файл "{self.source}" не является ZIP-архивом. Продолжение невозможно.', color='red')
            return

        print()
        cprint('Все готово!', color='yellow')


if __name__ == '__main__':

    sorter = FileSorterFromDir('icons', 'icons_by_year')
    sorter.start()
