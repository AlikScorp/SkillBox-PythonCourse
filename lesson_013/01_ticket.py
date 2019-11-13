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
import re
from dataclasses import dataclass
from enum import IntEnum
from sys import argv
from typing import Optional, Tuple

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


class ImageFillerState(IntEnum):
    """
        Класс содержит целочисленные перечислимые константы для класса ImageFiller
    """
    IMAGE_NOT_LOADED = 0
    IMAGE_LOADED = 1
    IMAGE_READY = 2


@dataclass
class ImageFillerPlaceholder:
    """
        Placeholder dataclass
        name - имя плейсхолдера
        place - координаты размещения в формате (x,y)
        type - тип плейсхолдера. Возможные варинаты 'text' (по умолчанию) и 'image'.
            в случае если тип плейсхолдера 'image' по переданным координатам будет размещено изображение.
        value - значение, которое будет размещено по переданным координатам.
            В случае если тип плейсхолдера 'image' - value должно содержать путь до файла изображения.
    """
    _place: tuple = (0, 0)
    _type: str = 'text'
    _value: str = ''
    _font: Optional[ImageFont.FreeTypeFont] = None
    _color: Optional[str] = None

    def __post_init__(self):

        if self._font is None:
            self._font = ImageFont.truetype(os.path.join('fonts', 'marutya.ttf'), size=15)

        if self._color is None:
            self._color = ImageColor.colormap['slateblue']

    @property
    def color(self) -> str:
        """
            Getter для атрибута _color
        :return: _color
        """
        return self._color

    @color.setter
    def color(self, color: str) -> None:
        """
            Setter для атрибута _color
        :param color: Цвет шрифта в формате '#000000'
        :return: None
        """
        if len(color) == 7 and re.match("#[a-f0-9A-F]{6}$", color):
            self._color = color
        else:
            cprint('Error: Incorrect color identification. Color left unchanged. ', color='red')

    @property
    def font(self) -> ImageFont.FreeTypeFont:
        """
            Getter для атрибута _font
        :return:
        """
        return self._font

    @font.setter
    def font(self, font: ImageFont.FreeTypeFont) -> None:
        """
            Setter для атрибута _font
        :param font: Экземпляр класса ImageFont
        :return:
        """
        if isinstance(font, ImageFont.FreeTypeFont):
            self._font = font
        else:
            cprint('Error: Incorrect type of font. Please be sure that it is ImageFont.FreeTypeFont. '
                   'Font left unchanged', color='red')

    @property
    def place(self) -> Tuple[int, int]:
        """
            Getter для атрибута _font
        :return: Tuple - Положение плейсхолдера на шаблоне
        """
        return self._place

    @place.setter
    def place(self, place: Tuple[int, int]) -> None:
        """
            Setter для атрибута _place
        :param place:
        :return: None
        """
        if isinstance(place, tuple) and len(place) == 2:
            for element in place:
                if not isinstance(element, int):
                    raise ValueError('The elements of tuple should be integer.')

            self._place = place
        else:
            raise ValueError('Parameter "place" should be a tuple with two elements of type integer.')

    @property
    def type(self) -> str:
        """
            Getter для параметра _type
        :return:
        """
        return self._type

    @type.setter
    def type(self, type_of_element: str) -> None:
        if type_of_element in ('text', 'image'):
            self._type = type_of_element
        else:
            raise ValueError(f'Incorrect type of placeholder - {type_of_element}')

    @property
    def value(self) -> str:
        """
            Getter для параметра _value
        :return: Атрибут _value
        """
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        """
            Setter для параметра _value
        :param value:
        :return: None
        """
        if isinstance(value, str):
            self._value = value
        else:
            raise ValueError('Value of placeholder should be a string')


class ImageFiller:
    """
        Класс предназначен для добавления элементов (графических или текстовых) в переданный ему шаблон.
        Принимает, в качестве аргумента, путь к шаблону.
        Использует плейсхолдеры для указания мест размещения данных на шаблоне.
    """

    _status: int = ImageFillerState.IMAGE_NOT_LOADED
    _path_to_template: str
    _placeholders: dict

    def __init__(self, path: str) -> None:

        if os.path.isfile(path):
            self.template = Image.open(path)
            self.status = ImageFillerState.IMAGE_LOADED
        else:
            raise ValueError(f'Cannot use image by the following path {path}. Please be sure the path is correct')

        self._path_to_template = path
        self._placeholders = dict()
        self.image = None

    @property
    def status(self) -> int:
        """
            Возвращает статус объекта
        :return: Статус объекта self._status
        """
        return self._status

    @status.setter
    def status(self, status) -> None:
        self._status = status

    @status.deleter
    def status(self) -> None:
        self._status = ImageFillerState.IMAGE_NOT_LOADED

    def is_loaded(self) -> bool:
        """
            Проверяет загружен ли шаблон изображения.
        :return: True если шаблон корректно загружен
        """
        return self.status > 0

    def placeholder(self, name: str) -> ImageFillerPlaceholder:
        """
            Добавляет плейсхолдер по умолчанию
        :param name: Имя плейсхолдера для последующего доступа
        :return: Созданный плейсхолдер
        """
        if name not in self._placeholders.keys():
            self._placeholders[name] = ImageFillerPlaceholder()

        return self._placeholders[name]

    def placeholders(self) -> list:
        """
            Возвращает имена добавленных плейсхолдеров
        :return: Список ключей из словаря плейсхолдеров
        """
        return list(self._placeholders.keys())

    def enhance(self) -> bool:
        """
            Размещает плейсхолдеры на шаблоне
        :return: True в случае успеха и False в противном случае
        """
        if self.is_loaded():
            self.image = ImageDraw.Draw(self.template)

            for placeholder in self._placeholders.values():
                if placeholder.type == 'text':

                    self.image.text(
                        xy=placeholder.place,
                        text=placeholder.value,
                        fill=placeholder.color,
                        font=placeholder.font
                    )

                else:
                    if os.path.isfile(placeholder.value):
                        image = Image.open(placeholder.value)
                        self.template.paste(im=image, box=placeholder.place, mask=image)
                    else:
                        raise ValueError(f'Cannot open image-file by the following file-name {placeholder.value}')

            self.status = ImageFillerState.IMAGE_READY
            return True

        return False

    def save_to(self, path: str, display: bool = False) -> bool:
        """
            Записывает готовое изображение в файл
        :param path: Имя файла
        :param display: Логическая переменная, если True то выводит изображение на экран после записи в файл
        :return: True в случае успеха и False в противном случае
        """
        if self.status == ImageFillerState.IMAGE_READY:
            self.template.save(path)
        elif self.status == ImageFillerState.IMAGE_LOADED:
            if self.enhance():
                self.template.save(path)
            else:
                return False
        else:
            raise ValueError(f'Image template {self._path_to_template} isn\'t loaded!')

        if display:
            self.template.show()


class CommandLineParser(argparse.ArgumentParser):
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


class SkillBoxTicket(ImageFiller):
    """
        Класс формирует билет
    """

    def __init__(self):
        super().__init__(os.path.join('images', 'ticket_template.png'))

        self.placeholder('Name').place = (50, 125)
        self.placeholder('Departure').place = (50, 194)
        self.placeholder('Destination').place = (50, 260)
        self.placeholder('Date').place = (290, 260)

        self.placeholder('Stamp').place = (476, 246)
        self.placeholder('Stamp').type = 'image'
        self.placeholder('Stamp').value = os.path.join("images", "stamp.png")

    def values(self, name: str, departure: str, destination: str, date: str):
        """
            Метод добавляет значения плейсхолдеров в билет
        :param name: Имя пасажира
        :param departure: Пункт отправления
        :param destination: Пункт назначения
        :param date: Дата вылета
        :return:
        """

        self.placeholder('Name').value = name
        self.placeholder('Departure').value = departure
        self.placeholder('Destination').value = destination
        self.placeholder('Date').value = date


def make_ticket(name: str, departure: str, destination: str, date: str) -> SkillBoxTicket:
    """
        Функция создает png-файл билета изпользуя переданные ему данные
    :param name: ФИО пассажира
    :param departure: Пункт отправления
    :param destination: Пункт назначения
    :param date: Дата вылета
    :return: Созданный билет в в виде экземпляра класса SkillBoxTicket
    """

    ticket = SkillBoxTicket()
    ticket.values(name=name, departure=departure, destination=destination, date=date)

    return ticket


def main():
    """
        Функция запускается в случае прямого запуска модуля.
        Отслеживает передачу аргументов с командной строки.
    :return: None
    """

    parser = CommandLineParser(description='This module is creating air-ticket by received data.')

    if len(argv) > 1:
        args = parser.parse_args()

        ticket = make_ticket(name=args.name, departure=args.departure, destination=args.destination, date=args.date)
        ticket.save_to(os.path.join('images', args.save_to), display=True)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
