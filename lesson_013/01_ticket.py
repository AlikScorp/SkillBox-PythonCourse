# -*- coding: utf-8 -*-
"""
Модуль предназначен для создания графичекого файла авиабилета.
Работает с коммандной строки
"""

# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru
import argparse
import os
from sys import argv
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageColor
from termcolor import cprint


# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля agrparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.


class ImageFiller:
    """
        Класс предназначен для добавления элементов (графических или текстовых) в переданный ему шаблон.
        Принимает, в качестве аргумента, путь к шаблону.
        Использует плейсхолдеры для указания мест размещения данных на шаблоне.
    """
    PH_PLACE: int = 0
    PH_TYPE: int = 1
    PH_VALUE: int = 2

    # TODO Константы, обозначающие статус загруженного изобращения лучше заменить на enum.IntEnum
    #  из стандартной библиотеки.
    IMAGE_NOT_LOADED = 0
    IMAGE_LOADED = 1
    IMAGE_READY = 2

    # TODO Можно не задавать эти аттрибуты на классе, т. к. они заменяются
    #  аттрибутами экземпляра при его инициализации
    _status = IMAGE_NOT_LOADED

    _path_to_template: str
    _placeholders: dict

    def __init__(self, path: str) -> None:

        # TODO Как обрабатывается ситуация, когда передан не файл
        if os.path.isfile(path):
            self.template = Image.open(path)
            self.status = self.IMAGE_LOADED

        self._path_to_template = path
        self._placeholders = dict()
        self.image = None
        self._font = None
        self._color = None

    @property
    def status(self):
        """
            Возвращает статус объекта
        :return: Статус объекта self._status
        """
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @status.deleter
    def status(self):
        self._status = self.IMAGE_NOT_LOADED

    def is_loaded(self):
        """
            Проверяет загружен ли шаблон изображения.
        :return: True если шаблон корректно загружен
        """
        return self.status > 0

    def add_placeholder(self,
                        name_of_placeholder: str,
                        place_on_template: Tuple[int, int],
                        type_of_placeholder: str = "text",
                        value_of_placeholder: Optional[str] = None) -> bool:
        """
            Добавляет плейсхолдер в шаблон
        :param name_of_placeholder: Имя плейсхолдера
        :param type_of_placeholder: Тип плейсхолдера (строковый или картинка)
        :param place_on_template: Место размещения на шаблоне в формате (x, y)
        :param value_of_placeholder: Значение в плейсхолдере (если тип - картинка, то здесь путь до нее)
        :return: True в случае если плейсхолдер добавлен и False в противном случае
        """
        if type_of_placeholder == 'text':
            self._placeholders[name_of_placeholder] = (place_on_template, type_of_placeholder, value_of_placeholder)
        elif type_of_placeholder == 'image':
            if os.path.isfile(value_of_placeholder):
                self._placeholders[name_of_placeholder] = (place_on_template, type_of_placeholder, value_of_placeholder)
            else:
                pass
        else:
            pass

        return True

    def set_font(self, path_to_font: str, size: int) -> bool:
        """
            Устанавливает шрифт для вывода текстовой информации
        :param path_to_font: Путь до файла шрифта
        :param size: Размер шрифта
        :return: True в услучае успеха и False в противном случает
        """
        if os.path.isfile(path_to_font):
            self.font = ImageFont.truetype(path_to_font, size=size)
            return True

        return False

    @property
    def color(self):
        """
            Возвращает цвет выводимого текста
        :return: Цвет
        """
        return self._color if self._color is not None else '#685faa'

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def font(self):
        """
            Возвращает шрифт в виде объекта ImageFont
        :return:
        """
        if self._font is None:
            self._font = ImageFont.truetype(os.path.join('fonts', 'Junegull.ttf'), 15)

        return self._font

    @font.setter
    def font(self, font):
        self._font = font

    def enhance(self) -> bool:
        """
            Размещает плейсхолдеры на шаблоне
        :return: True в случае успеха и False в противном случае
        """
        if self.is_loaded():
            self.image = ImageDraw.Draw(self.template)

            # TODO Похоже, что вы не используете name.
            #  Можно _placeholders.items() заменить на _placeholders.values()
            for name, value in self._placeholders.items():
                if value[self.PH_TYPE] == 'text':
                    # TODO Желательно предусмотреть проверку переданных данных и обрабатывать ошибки,
                    #  которые могут возникнуть.
                    # TODO Использования констант с индексами не самый работы с данными. Обратите внимание
                    #  на именованные кортежи NamedTuple или dataclass, появившиеся в python 3.7
                    self.image.text(value[self.PH_PLACE], value[self.PH_VALUE], self.color, self.font)
                else:
                    # Здесь вставляем картинку
                    image = Image.open(value[self.PH_VALUE])
                    self.template.paste(image, value[self.PH_PLACE], mask=image)

            self.status = self.IMAGE_READY
            return True

        return False

    def display(self) -> None:
        """
            Выводит изображение на экран.
        :return: None
        """
        if self.status == self.IMAGE_READY:
            self.template.show()
        elif self.status == self.IMAGE_LOADED:
            if self.enhance():
                self.template.show()
        else:
            cprint('Шаблон изображения не загружен!', color='red')

    def save_to(self, path) -> bool:
        """
            Записывает готовое изображение в файл
        :param path: Имя файла
        :return: True в случае успеха и False в противном случае
        """
        if self.status == self.IMAGE_READY:
            self.template.save(path)
            return True
        elif self.status == self.IMAGE_LOADED:
            if self.enhance():
                self.template.save(path)
                return True
            else:
                return False
        else:
            cprint(f'Ошибка: Шаблон изображения {self._path_to_template} не загружен!', color='red')
            return False

    def set_text_attributes(self, path_to_font: str, size: int, color: str):
        """
            Выставляет атрибуты вывода текста (шрифт и цвет).
            Метод поочередно вызывает методы self.color и self.set_font
        :param path_to_font: Путь до файла шрифта
        :param size: Размер шрифта
        :param color: Цвет шрифта
        :return:
        """
        self.color = color
        self.set_font(path_to_font=path_to_font, size=size)


class TicketInfoParser(argparse.ArgumentParser):
    """
        Класс потомок ArgumentParser
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_argument('name',
                          metavar="Name",
                          help="Name of passenger. Use quotes when using first and last names. Example: \"John Doe\"")

        self.add_argument('departure',
                          metavar="From",
                          help='Airport of departure. Use quotes when title has spaces. Examples: "San Francisco"')

        self.add_argument('destination',
                          metavar="To",
                          help='Airport of destination. Use quotes when title has spaces. Examples: "Los Angeles"')

        self.add_argument('date', metavar="Date", help='Date of flight. Format - "dd/mm/yyyy"')
        self.add_argument('--save_to', help="path to store the ticket", default='ticket.png')


def make_ticket(name: str, departure: str, destination: str, date: int) -> ImageFiller:
    """
        Функция создает png-файл билета изпользуя переданные ему данные
    :param name: ФИО пассажира
    :param departure: Пункт отправления
    :param destination: Пункт назначения
    :param date: Дата вылета
    :return: True в случае успешного создания, False  в противном случае
    """
    placeholders = {
        'Name': ((50, 125), "text", name),
        'From': ((50, 194), "text", departure),
        'To': ((50, 260), "text", destination),
        'Date': ((290, 260), "text", date),
        'Stamp': ((476, 246), "image", os.path.join("images", "stamp.png")),
    }

    ticket = ImageFiller(os.path.join('images', 'ticket_template.png'))
    # TODO Лучше передавать данные полученные от пользователя отдельно от настроек размещения.
    #  Для настроек можно сделать отдельный класс (предусмотрим возможность типов билетов,
    #  отличающихся расположением элементов). Также можно предусмотреть возможность расширения
    #  настроив один раз билет передавать данные о пассажирах и сохранять
    #  изображения без необходимости инициализировать объект каждый раз заново, т. е.
    #  печатать билеты разным пассажирам по одному шаблону.
    for name, value in placeholders.items():
        ticket.add_placeholder(name,
                               place_on_template=value[ImageFiller.PH_PLACE],
                               type_of_placeholder=value[ImageFiller.PH_TYPE],
                               value_of_placeholder=value[ImageFiller.PH_VALUE],
                               )

    # TODO Очень похоже, что такие настройки стоит задавать при инициализации ImageFiller
    ticket.set_text_attributes(os.path.join('fonts', 'marutya.ttf'), 15, color=ImageColor.colormap['blue'])

    return ticket


def main():
    """
        Функция запускается в случае прямого запуска модуля.
        Отслеживает передачу аргументов с командной строки.
    :return: None
    """

    parser = TicketInfoParser(description='This module is creating air-ticket by received data.')

    if len(argv) > 1:
        args = parser.parse_args()

        ticket = make_ticket(name=args.name, departure=args.departure, destination=args.destination, date=args.date)

        if ticket.save_to(os.path.join('images', args.save_to)):
            ticket.display()
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
