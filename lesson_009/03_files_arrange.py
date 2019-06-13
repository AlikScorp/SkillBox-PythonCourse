# -*- coding: utf-8 -*-

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
        Класс "раскидывает" по папкам файлы из переданного ему источника.
        Источником является папка с файлами.

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

        if os.path.isdir(self.source):
            cprint(f'Исходящая папка "{self.source}" найдена', color='yellow')
        else:
            cprint(f'Исходящая папка "{self.source}" не найдена. Продолжение работы невозможно.', color='red')
            return

        self._check_destination()

        cprint(f'Копируем файлы из файла "{self.source}" в папку "{self.destination}":', color='yellow')
        counter = 0

        for dir_path, dir_names, file_names in os.walk(self.source):
            for file in file_names:
                path_to_file = os.path.join(dir_path, file)
                seconds = os.path.getmtime(path_to_file)
                date = time.gmtime(seconds)
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

    def start(self):
        self._sort()

# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Основная функция должна брать параметром имя zip-файла и имя целевой папки.
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828


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
                    path_to_file, filename = os.path.split(file)
                    date_time = file_info.date_time
                    path = os.path.join(self.destination, str(date_time[0]), str(date_time[1]), str(date_time[2]))
                    if not file_info.is_dir():
                        result = zip_file.open(file)
                        os.makedirs(path, exist_ok=True)

                        """
                            Не смог разобраться (гугл тоже не помог) каким образом распаковать файлы из архива с
                            сохранением метаданных (дата и время создания файла).
                            Если использовать метод zip_fil.extract(file, path) файл рапаковывается в нужную папку,
                            с "родными" метаданными но с сохранением путей которые указаны в архиве 
                            (например: "icons/actions"). В результате получаем следующую структуру:
                            "icons_by_year/2017/6/2/icons/actions"
                            
                            Буду счастлив если подскажете куда копать. :-)
                        """

                        with open(os.path.join(path, filename), 'wb') as outfile:
                            shutil.copyfileobj(result, outfile)

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
    sorter = FileSorterFromZip('icons.zip', 'icons_by_year')
    sorter.start()
