"""
    Модуль предназначен для парсинга сайта 'https://yandex.ru/pogoda/' на придмет получения прогноза погоды.
    Для парсинга сайта используем библиотеки requests и BeautifulSoup
"""
import datetime
import requests
import bs4
import os
from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, Tuple, List, Type
import cv2
import numpy
from playhouse.db_url import connect, DatabaseProxy
from termcolor import cprint
import peewee as pw

# clear — ясно.
# partly-cloudy — малооблачно.
# cloudy — облачно с прояснениями.
# overcast — пасмурно.
# partly-cloudy-and-light-rain — небольшой дождь.
# partly-cloudy-and-rain — дождь.
# overcast-and-rain — сильный дождь.
# overcast-thunderstorms-with-rain — сильный дождь, гроза.
# cloudy-and-light-rain — небольшой дождь.
# overcast-and-light-rain — небольшой дождь.
# cloudy-and-rain — дождь.
# overcast-and-wet-snow — дождь со снегом.
# partly-cloudy-and-light-snow — небольшой снег.
# partly-cloudy-and-snow — снег.
# overcast-and-snow — снегопад.
# cloudy-and-light-snow — небольшой снег.
# overcast-and-light-snow — небольшой снег.
# cloudy-and-snow — снег.

# ovc - Облачно
# bkn - Переменная облачность
# skc - Ясно
# bl - Метель
# fg - Туман
# sn - Снег (+/-) - (сильный, небольшой)
# ra - Дождь (+/-) - (сильный, небольшой)
# ts - Гроза

# 's'=>'↑ ю','n'=>'↓ с','w'=>'→ з','e'=>'← в','sw'=>'↗ юз','se'=>'↖ юв','nw'=>'↘ сз','ne'=>'↙ св'

CONDITIONS: dict = {
    'ovc': 'Cloudy',
    'bkn': 'Partly cloudy',
    'skc': 'Clear',
    'bl': 'Blizzard',
    'fg': 'Fog',
    'sn': 'Snow',
    '-sn': 'Light snow',
    '+sn': 'Snowfall',
    'ra': 'Rain',
    '-ra': 'Small rain',
    '+ra': 'Heavy rain',
    'ts': 'Storm',
}

MONTHS: dict = {
    'января': ['Jun', 1, '01'],
    'февраля': ['Feb', 2, '02'],
    'марта': ['Mar', 3, '03'],
    'апреля': ['Apr', 4, '04'],
    'мая': ['May', 5, '05'],
    'июня': ['Jun', 6, '06'],
    'июля': ['Jul', 7, '07'],
    'августа': ['Aug', 8, '08'],
    'сентября': ['Sep', 9, '09'],
    'октября': ['Oct', 10, '10'],
    'ноября': ['Nov', 11, '11'],
    'декабря': ['Dec', 12, '12']
}

CV_WIDTH = 1
CV_HEIGHT = 0


class ImageFillerState(IntEnum):
    """
        Класс содержит целочисленные перечислимые константы для класса ImageFiller
    """
    IMAGE_NOT_LOADED = 0
    IMAGE_LOADED = 1
    IMAGE_READY = 2


@dataclass
class ImageFillerFont:
    """
        Датакласс для хранения шрифта для ImageFillerPlaceholder
        _font_face - начертание шрифта
        _font_scale - Размер шрифта,
        _font_color -  цвет шрифта в формате (Blue, Green, Red),
                      где Blue, Green, Red принемают значения от 0 до 255
        _font_thickness - толщина шрифта
    """
    # Доступные для использоваия шрифты
    # cv::FONT_HERSHEY_SIMPLEX = 0,
    # cv::FONT_HERSHEY_PLAIN = 1,
    # cv::FONT_HERSHEY_DUPLEX = 2,
    # cv::FONT_HERSHEY_COMPLEX = 3,
    # cv::FONT_HERSHEY_TRIPLEX = 4,
    # cv::FONT_HERSHEY_COMPLEX_SMALL = 5,
    # cv::FONT_HERSHEY_SCRIPT_SIMPLEX = 6,
    # cv::FONT_HERSHEY_SCRIPT_COMPLEX = 7,
    # cv::FONT_ITALIC = 16

    _font_face: int = cv2.FONT_HERSHEY_PLAIN
    _font_scale: int = 1
    _font_color: tuple = (0, 0, 0)
    _font_thickness: int = 1

    @property
    def font_face(self) -> int:
        """
            Мотод-свойство возвращает текущее начертание шрифта
        :return: int
        """
        return self._font_face

    @font_face.setter
    def font_face(self, font_face):
        self._font_face = font_face

    @property
    def font_scale(self) -> int:
        """
            Метод-свойтво возвращает размер шрифта
        :return: int
        """
        return self._font_scale

    @font_scale.setter
    def font_scale(self, scale):
        self._font_scale = scale

    @property
    def font_color(self) -> tuple:
        """
            Возвращает цвет шрифта
        :return: tuple
        """
        return self._font_color

    @font_color.setter
    def font_color(self, color):
        self._font_color = color

    @property
    def font_thickness(self) -> int:
        """
            Возвращает толщину шрифта
        :return: int
        """
        return self._font_thickness

    @font_thickness.setter
    def font_thickness(self, thickness):
        self._font_thickness = thickness


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
    _font: Optional[ImageFillerFont] = None

    def __post_init__(self):
        if self._font is None:
            self._font = ImageFillerFont()

    @property
    def font(self) -> ImageFillerFont:
        """
            Getter для атрибута _font
        :return:
        """
        return self._font

    @font.setter
    def font(self, font: ImageFillerFont) -> None:
        """
            Setter для атрибута _font
        :param font: Экземпляр класса ImageFont
        :return:
        """
        if isinstance(font, ImageFillerFont):
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
            self.template = cv2.imread(path)
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

            for placeholder in self._placeholders.values():
                if placeholder.type == 'text':
                    cv2.putText(self.template,
                                placeholder.value,
                                placeholder.place,
                                placeholder.font.font_face,
                                placeholder.font.font_scale,
                                placeholder.font.font_color,
                                placeholder.font.font_thickness
                                )
                else:
                    if os.path.isfile(placeholder.value):
                        image_to_paste = cv2.imread(placeholder.value)
                        self.paste_image(image_to_paste, placeholder.place)
                    else:
                        raise ValueError(f'Cannot open image-file by the following file-name {placeholder.value}')

            self.status = ImageFillerState.IMAGE_READY
            return True

    def linear_gradient(self, color_start: tuple, color_end: tuple, direction: int) -> None:
        """
            Функция градиентом заливает холст
        :param color_start: Начальный цвет
        :param color_end: Конечный цвет
        :param direction: Режим заливки (top_to_bottom, bottom_to_top, right_to_left, left_to_right)
        :return: None
        """

        if direction == GradientDirections.TOP_TO_BOTTOM:  # заливка сверху вниз
            for y in range(0, self.template.shape[0]):
                for x in range(0, self.template.shape[1]):
                    self.template[y, x, 0] = color_start[0] - int(
                        abs(color_start[0] - color_end[0]) * y / self.template.shape[0])
                    self.template[y, x, 1] = color_start[1] - int(
                        abs(color_start[1] - color_end[1]) * y / self.template.shape[0])
                    self.template[y, x, 2] = color_start[2] - int(
                        abs(color_start[2] - color_end[2]) * y / self.template.shape[0])
        elif direction == GradientDirections.BOTTOM_TO_TOP:  # заливка снизу вверх
            for y in range(0, self.template.shape[0]):
                for x in range(0, self.template.shape[1]):
                    self.template[y, x, 0] = color_end[0] + int(
                        abs(color_start[0] - color_end[0]) * y / self.template.shape[0])
                    self.template[y, x, 1] = color_end[1] + int(
                        abs(color_start[1] - color_end[1]) * y / self.template.shape[0])
                    self.template[y, x, 2] = color_end[2] + int(
                        abs(color_start[2] - color_end[2]) * y / self.template.shape[0])
        elif direction == GradientDirections.LEFT_TO_RIGHT:  # заливка слева направо
            for x in range(0, self.template.shape[1]):
                for y in range(0, self.template.shape[0]):
                    self.template[y, x, 0] = color_start[0] - int(
                        abs(color_start[0] - color_end[0]) * x / self.template.shape[1])
                    self.template[y, x, 1] = color_start[1] - int(
                        abs(color_start[1] - color_end[1]) * x / self.template.shape[1])
                    self.template[y, x, 2] = color_start[2] - int(
                        abs(color_start[2] - color_end[2]) * x / self.template.shape[1])
        elif direction == GradientDirections.RIGHT_TO_LEFT:  # заливка справа налево
            for x in range(0, self.template.shape[1]):
                for y in range(0, self.template.shape[0]):
                    self.template[y, x, 0] = color_end[0] + int(
                        abs(color_end[0] - color_start[0]) * x / self.template.shape[1])
                    self.template[y, x, 1] = color_end[1] + int(
                        abs(color_end[1] - color_start[1]) * x / self.template.shape[1])
                    self.template[y, x, 2] = color_end[2] + int(
                        abs(color_end[2] - color_start[2]) * x / self.template.shape[1])
        else:
            raise ValueError(f'Unknown direction {direction}')

    def paste_image(self, image_to_paste: numpy.ndarray, coordinates: tuple):
        """
            Функция вставляет изображение (image_to_paste) в исходное изображение.
        :param image_to_paste: Изображение которое вставляем
        :param coordinates: Координаты в которые надо поместить изображение (левый верхний угол) (x,y)
        :return: None
        """

        x = coordinates[0]
        y = coordinates[1]

        source_width, source_height = image_to_paste.shape[:2]
        region = self.template[x:source_width + x, y:source_height + y]

        grayscale_image = cv2.cvtColor(image_to_paste, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(grayscale_image, 240, 255, cv2.THRESH_BINARY_INV)
        mask_inv = cv2.bitwise_not(mask)
        source_foreground = cv2.bitwise_and(image_to_paste, image_to_paste, mask=mask)

        destination_background = cv2.bitwise_and(region, region, mask=mask_inv)

        self.template[x:source_width + x, y:source_height + y] = \
            cv2.add(source_foreground, destination_background)

    def display(self, name_of_window: str = 'Image') -> None:
        """
            Выводит изображение на экран
        :return: None
        """
        cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name_of_window, int(self.template.shape[CV_WIDTH]), int(self.template.shape[CV_HEIGHT]))
        cv2.imshow(name_of_window, self.template)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_to(self, path: str) -> bool:
        """
            Записывает готовое изображение в файл
        :param path: Имя файла
        :return: True в случае успеха и False в противном случае
        """
        cv2.imwrite(path+'.jpg', self.template)

        return True


class GradientDirections(IntEnum):
    """
        Класс содержит константы для обозначаения направления заливки для класса WeatherInformer
    """
    TOP_TO_BOTTOM = 1
    BOTTOM_TO_TOP = 2
    LEFT_TO_RIGHT = 3
    RIGHT_TO_LEFT = 4


class Gradient:
    """
        Класс хранит информацию о начальном и конечном цвете для заливки
    """
    _start: tuple
    _finish: tuple
    _direction: int

    def __init__(self, start: tuple = None,
                 finish: tuple = None,
                 direction: int = None):

        self.start = start if start is not None else (255, 255, 255)
        self.finish = finish if finish is not None else (255, 255, 255)
        self.direction = direction if direction is not None else GradientDirections.TOP_TO_BOTTOM

    @property
    def start(self):
        """
            Возвращает начальный цвет градиента
        :return: self._start
        """
        return self._start

    @start.setter
    def start(self, color: tuple):
        if isinstance(color, tuple) and len(color) == 3 and all(isinstance(element, int) for element in color):
            self._start = color
        else:
            raise ValueError(
                'Wrong type of "color" or wrong elements of "color". It should be tuple(int, int, int)')

    @property
    def finish(self):
        """
            Возвращает конечный цвет градиента
        :return: self._start
        """
        return self._finish

    @finish.setter
    def finish(self, color: tuple):
        if isinstance(color, tuple) and len(color) == 3 and all(isinstance(element, int) for element in color):
            self._finish = color
        else:
            raise ValueError(
                'Wrong type of "color" or wrong elements of "color". It should be tuple(int, int, int)')

    @property
    def direction(self):
        """
            Метод возвращает направление заливки
        :return:
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        list_of_directions = list(map(int, GradientDirections))
        if direction in list_of_directions:
            self._direction = direction
        else:
            raise ValueError('Wrong direction is received')

    def info(self):
        """
            Возвращает словарь с данными градиента
                {: }
        :return:
        """
        return {'start': self.start, 'finish': self.finish, 'direction': self.direction}


class Palette:
    """
        Класс содержит информацию о цветовой палитре для использования в классе WeatherInformer
    """
    _gradient: Gradient
    _title: Tuple[int, int, int]
    _fields: Tuple[int, int, int]
    _values: Tuple[int, int, int]

    def __init__(self, gradient_info: Gradient = None,
                 title_color: tuple = None,
                 fields_color: tuple = None,
                 values_color: tuple = None):

        self.gradient = Gradient() if gradient_info is None else gradient_info
        self.title = (194, 125, 49) if title_color is None else title_color
        self.fields = (3, 3, 193) if fields_color is None else fields_color
        self.values = (0, 0, 255) if values_color is None else values_color

    @property
    def title(self):
        """
            Возвращает цвет заголовка
        :return: self._title
        """
        return self._title

    @title.setter
    def title(self, color):
        if isinstance(color, tuple) and len(color) == 3 and all(isinstance(element, int) for element in color):
            self._title = color
        else:
            raise ValueError('Wrong type of "color" or wrong elements of "color". It should be tuple(int, int, int)')

    @property
    def fields(self):
        """
            КЛасс возвращает цвет используемый для отображения полей
        :return: self._fields
        """
        return self._fields

    @fields.setter
    def fields(self, color):
        if isinstance(color, tuple) and len(color) == 3 and all(isinstance(element, int) for element in color):
            self._fields = color
        else:
            raise ValueError('Wrong type of "fields" or wrong elements of "fields". It should be tuple(int, int, int)')

    @property
    def values(self):
        """
            Класс возвращает цвет используемый для отображения значения полей
        :return: self._values
        """
        return self._values

    @values.setter
    def values(self, color):
        if isinstance(color, tuple) and len(color) == 3 and all(isinstance(element, int) for element in color):
            self._values = color
        else:
            raise ValueError('Wrong type of "values" or wrong elements of "values". It should be tuple(int, int, int)')

    @property
    def gradient(self):
        """
            Возвращает настройки градиента
        :return: self._gradient
        """
        return self._gradient

    @gradient.setter
    def gradient(self, gradient_info: Gradient):
        if isinstance(gradient_info, Gradient):
            self._gradient = gradient_info
        else:
            raise ValueError('Wrong value for gradient_info. Type of argument should be Gradient.')


class DayWeather:
    """
        Класс содержит информацию о погоде в течении дня.
        Создает словарь следующего типа:
        {
            'date': datetime(),
            'image': '//yastatic.net/weather/i/icons/funky/dark/bkn_d.svg',
            'temp': {'day': '+7', 'night': '+4', 'feels_like': '+3'},
            'pressure': 713,
            'humidity': '59%',
            'wind': {'speed': 4.1, 'direction': 'Ю', 'gust': 5.4}
            'conditions': ['перменная облачность', 'дождь]
        }
    """
    day_weather_info: dict
    day_in_html: bs4.element.ResultSet

    @dataclass
    class Temperature:
        """
            Класс содержит информацию о температуре - дневной, ночной и "ощущается"
        """
        _temp_day: str
        _temp_night: str
        _temp_feels_like: str

        def __str__(self):
            return f'Temperature - ' \
                   f'Day: {self._temp_day}°C; ' \
                   f'Night: {self._temp_night}°C; ' \
                   f'Feels like: {self._temp_feels_like}°C'

        def __repr__(self):
            return f'DayWeather.Temperature(' \
                   f'temp_day="{self._temp_day}", ' \
                   f'temp_night="{self._temp_night}", ' \
                   f'temp_feels_like="{self._temp_feels_like}")'

        def __format__(self, format_spec):
            return f'{self.__str__():{format_spec}}'

        @property
        def info(self):
            """
                Метод записывает данные класса в словарь и возвращает его
            :return: Словарь с данными из класса
            """
            return {'temp_day': self.day, 'temp_night': self.night, 'feels_like': self.feels_like}

        @property
        def day(self):
            """
                Возвращает информацию о температуре днем
            :return: str
            """
            return self._temp_day

        @property
        def night(self):
            """
                Возвращает информацию о температуре днем
            :return: str
            """
            return self._temp_night

        @property
        def feels_like(self):
            """
                Возвращает информацию о температуре днем
            :return: str
            """
            return self._temp_feels_like

    @dataclass
    class Wind:
        """
            Класс содержит информацию о ветре - скорость, направление, порывы
        """
        wind_speed: float
        wind_direction: str
        wind_gust: float

        def __str__(self):
            return f'Wind - ' \
                   f'Speed: {self.wind_speed} m/s; ' \
                   f'Direction: "{self.wind_direction}"; ' \
                   f'Gust: {self.wind_gust} m/s'

        def __repr__(self):
            return f'DayWeather.Wind(' \
                   f'wind_speed={self.wind_speed}, ' \
                   f'wind_direction="{self.wind_direction}", ' \
                   f'wind_gust={self.wind_gust})'

        def __format__(self, format_spec):
            return f'{self.__str__():{format_spec}}'

        @property
        def info(self):
            """
                Метод записывает данные класса в словарь и возвращает его
            :return: Словарь с данными из класса
            """
            return {'wind_speed': self.wind_speed, 'wind_direction': self.wind_direction, 'wind_gust': self.wind_gust}

        @property
        def speed(self):
            """
                Возвращает скрорость ветра
            :return: str
            """
            return self.wind_speed

        @property
        def direction(self):
            """
                Возвращает направление ветра
            :return: str
            """
            return self.wind_direction

        @property
        def gust(self):
            """
                Возвращает порывы ветра
            :return: str
            """
            return self.wind_gust

    def __init__(self, day_in_html: bs4.element.ResultSet = None):
        if day_in_html is not None:
            self.day_in_html = day_in_html
            self.day_weather_info = dict()
            self.__get_info()
        else:
            self.day_weather_info = {'date': datetime.date(2020, 1, 1),
                                     'image': '',
                                     'temp': self.Temperature(_temp_day="+0",
                                                              _temp_night="+0",
                                                              _temp_feels_like="+0"
                                                              ),
                                     'pressure': '749 мм рт. ст.', 'humidity': '68%',
                                     'wind': self.Wind(wind_speed=0, wind_direction="E", wind_gust=0),
                                     'conditions': ['Partly cloudy']
                                     }

    @property
    def date(self):
        """
            Возвращает дату
        :return: datetime.date
        """
        return self.day_weather_info['date']

    @property
    def image(self):
        """
            Возвращает ссылку на картинку
        :return:
        """
        return self.day_weather_info['image']

    @property
    def humidity(self):
        """
            Возвращает влажность
        :return: str
        """
        return self.day_weather_info['humidity']

    @property
    def pressure(self):
        """
            Возвращает давление
        :return: int
        """
        return int(self.day_weather_info['pressure'].split(" ")[0])

    @property
    def conditions(self):
        """
            Возвращает условия
        :return: str
        """
        return ", ".join(self.day_weather_info['conditions'])

    def __get_conditions(self):
        file_name = self.day_weather_info['image'].split('/')[-1].split('.')[0]

        conditions = [CONDITIONS[condition] for condition in file_name.split('_') if condition in CONDITIONS]
        self.day_weather_info['conditions'] = conditions

    def __get_info(self):
        self.__get_date()
        self.__get_image_url()
        self.__get_temperature()
        self.__get_pressure_humidity_wind()
        self.__get_conditions()

    def __get_date(self):
        day, month = self.day_in_html.h6.text.split(",")[0].split(' ')

        date = datetime.date(year=datetime.datetime.now().year, month=MONTHS[month][1], day=int(day))

        self.day_weather_info['date'] = date

    def __get_image_url(self):
        self.day_weather_info['image'] = self.day_in_html.img['src']

    def __get_temperature(self):
        day_temperature_html = self.day_in_html.find('div',
                                                     {'class': 'climate-calendar-day__detailed-basic-temp-day'}
                                                     )
        day_temperature = day_temperature_html.find('span', {'class': 'temp__value'}).text

        night_temperature_html = self.day_in_html.find('div',
                                                       {'class': 'climate-calendar-day__detailed-basic-temp-night'}
                                                       )
        night_temperature = night_temperature_html.find('span', {'class': 'temp__value'}).text

        feels_temperature_html = self.day_in_html.find('div',
                                                       {'class': 'climate-calendar-day__detailed-feels-like'}
                                                       )
        feels_temperature = feels_temperature_html.find('span', {'class': 'temp__value'}).text

        self.day_weather_info['temp'] = self.Temperature(
            _temp_day=day_temperature,
            _temp_night=night_temperature,
            _temp_feels_like=feels_temperature
        )

    def __get_pressure_humidity_wind(self):

        directions = {'Ю': 'S', 'С': 'N', 'З': 'W', 'В': 'E', 'ЮЗ': 'SW', 'ЮВ': 'SE', 'СЗ': 'NW', 'СВ': 'NE'}

        day_pressure_humidity_wind = \
            self.day_in_html.find_all('td', {'class': 'climate-calendar-day__detailed-data-table-cell_value_yes'})

        self.day_weather_info['pressure'] = day_pressure_humidity_wind[0].text
        self.day_weather_info['humidity'] = day_pressure_humidity_wind[1].text

        self.day_weather_info['wind'] = self.Wind(
            wind_speed=float(day_pressure_humidity_wind[2].find('div', {'class': 'wind-speed'}).text),
            wind_direction=directions[day_pressure_humidity_wind[2].find('abbr').text],
            wind_gust=float(day_pressure_humidity_wind[2].find('div', {'class': 'wind-speed'}).text)
        )

    @property
    def temp(self):
        """
            Метод-свойство возвращает элемент по ключу "temp" из словаря day_weather_info
        :return: Экземпляр дата-класса DayWeather.Temperature хранящий значения тепператур в течении дня
                (temp_day, temp_night, temp_feels_like)
        """
        return self.day_weather_info['temp']

    @property
    def wind(self):
        """
            Метод-свойтсво возвращает элемент по ключу "wind" ил словаря day_weather_info
        :return: Экземпляр дата-класса DayWeather.Wind хрянящий данные о ветре (wind_speed, wind_direction, wind_gust)
        """
        return self.day_weather_info['wind']

    @property
    def info(self):
        """
            Метод-свойство возвращает словарь с прогнозом погоды
        :return: Словарь с данными о прогнозе
        """
        return self.day_weather_info

    @property
    def informer(self):
        """
            Метод возвращает информер погоды поданным из класса
        :return: WeatherInformer
        """
        return WeatherInformer(self)


class WeatherInformer:
    """
        Класс создает информер о погоде
    """

    canvas: ImageFiller
    day_info: DayWeather
    path_to_canvas: str
    path_to_sunny_image: str
    path_to_cloudy_image: str
    path_to_rainy_image: str
    path_to_snowy_image: str
    palette: Palette

    SUNNY_PALETTE: Palette = Palette(title_color=(194, 125, 49),
                                     fields_color=(3, 3, 193),
                                     values_color=(0, 0, 255),
                                     gradient_info=Gradient(start=(255, 255, 255), finish=(0, 255, 255),
                                                            direction=GradientDirections.BOTTOM_TO_TOP))

    RAINY_PALETTE: Palette = Palette(title_color=(255, 255, 255),
                                     fields_color=(255, 189, 0),
                                     values_color=(193, 114, 5),
                                     gradient_info=Gradient(start=(255, 255, 255), finish=(101, 57, 24),
                                                            direction=GradientDirections.BOTTOM_TO_TOP))

    CLOUDY_PALETTE: Palette = Palette(title_color=(255, 255, 255),
                                      fields_color=(0, 0, 0),
                                      values_color=(113, 113, 118),
                                      gradient_info=Gradient(start=(255, 255, 255), finish=(127, 127, 127),
                                                             direction=GradientDirections.BOTTOM_TO_TOP))

    SNOWY_PALETTE: Palette = Palette(title_color=(255, 255, 255),
                                     fields_color=(104, 60, 36),
                                     values_color=(192, 112, 0),
                                     gradient_info=Gradient(start=(255, 255, 255), finish=(240, 176, 18),
                                                            direction=GradientDirections.BOTTOM_TO_TOP))

    def __init__(self, day_info: DayWeather = None):
        self.path_to_canvas = 'python_snippets/external_data/probe.jpg'
        self.canvas = ImageFiller(self.path_to_canvas)

        self.path_to_sunny_image = 'python_snippets/external_data/weather_img/sun.jpg'
        self.path_to_cloudy_image = 'python_snippets/external_data/weather_img/cloud.jpg'
        self.path_to_snowy_image = 'python_snippets/external_data/weather_img/snow.jpg'
        self.path_to_rainy_image = 'python_snippets/external_data/weather_img/rain.jpg'

        self.day_info = day_info
        self.palette = Palette()
        self.prepare_placeholders()

    def apply_palette(self):
        """
            Метод применяет палитру
        :return: None
        """
        condition = self.day_info.conditions.lower()

        if condition.find('snow') >= 0:
            self.palette = self.SNOWY_PALETTE
            self.paste_icon(self.path_to_snowy_image)
        elif condition.find('rain') >= 0:
            self.palette = self.RAINY_PALETTE
            self.paste_icon(self.path_to_rainy_image)
        elif condition.find('cloud') >= 0:
            self.palette = self.CLOUDY_PALETTE
            self.paste_icon(self.path_to_cloudy_image)
        else:
            self.palette = self.SUNNY_PALETTE
            self.paste_icon(self.path_to_sunny_image)

    def apply_colors(self):
        """
            Метод меняет цвет у полей, согласно загруженной палитре
        :return: None
        """
        color_fields = self.palette.fields
        color_values = self.palette.values
        color_title = self.palette.title

        self.canvas.placeholder('title').font.font_color = color_title
        self.canvas.placeholder('date').font.font_color = color_values
        self.canvas.placeholder('condition').font.font_color = color_values
        self.canvas.placeholder('pressure_field').font.font_color = color_fields
        self.canvas.placeholder('pressure_value').font.font_color = color_values
        self.canvas.placeholder('wind_field').font.font_color = color_fields
        self.canvas.placeholder('wind_value').font.font_color = color_values
        self.canvas.placeholder('humidity_field').font.font_color = color_fields
        self.canvas.placeholder('humidity_value').font.font_color = color_values
        self.canvas.placeholder('feels_like_field').font.font_color = color_fields
        self.canvas.placeholder('feels_like_value').font.font_color = color_values
        self.canvas.placeholder('at_night_field').font.font_color = color_fields
        self.canvas.placeholder('at_night_value').font.font_color = color_values
        self.canvas.placeholder('day_field').font.font_color = color_values

    def fill_gradient(self):
        """
            Метод заливает холст в зависимости от погодных условий
        :return:
        """
        self.canvas.linear_gradient(self.palette.gradient.start,
                                    self.palette.gradient.finish,
                                    self.palette.gradient.direction,
                                    )

    def paste_icon(self, icon):
        """
            Помещает иконку на холст
        :return:
        """
        icon_placeholder = self.canvas.placeholder('icon')
        icon_placeholder.type = 'image'
        icon_placeholder.value = icon
        icon_placeholder.place = (20, 20)

    def prepare_image(self):
        """
            Метод подготавливает изображение к выводу
        :return: None
        """
        self.apply_palette()
        self.apply_colors()
        self.fill_gradient()
        self.canvas.enhance()

    def show(self):
        """
            Выводит на экран полученный информер
        :return:
        """
        self.prepare_image()
        self.canvas.display('Weather informer!!!')

    def save_to_disk(self):
        """
            Метод записывает информер на диск
        :return: None
        """
        self.prepare_image()
        self.canvas.save_to(self.day_info.date.strftime('%d%m%Y'))

    def prepare_placeholders(self):
        """
            Метод размещает плейсхолдеры на холсте
        :return: None
        """

        self.canvas.placeholder('title').place = (268, 20)
        self.canvas.placeholder('title').value = 'Weather in Ashgabat'
        self.canvas.placeholder('title').font.font_scale = 1.3
        self.canvas.placeholder('title').font.font_thickness = 2

        self.canvas.placeholder('date').place = (20, 145)
        self.canvas.placeholder('date').value = self.day_info.date.strftime("%d %B, %A")
        self.canvas.placeholder('date').font.font_scale = 1.2
        self.canvas.placeholder('date').font.font_thickness = 2

        self.canvas.placeholder('condition').place = (20, 168)
        self.canvas.placeholder('condition').value = self.day_info.conditions
        self.canvas.placeholder('condition').font.font_scale = 1
        self.canvas.placeholder('condition').font.font_thickness = 2

        self.canvas.placeholder('pressure_field').place = (20, 230)
        self.canvas.placeholder('pressure_field').value = 'Pressure:'
        self.canvas.placeholder('pressure_field').font.font_scale = 1
        self.canvas.placeholder('pressure_field').font.font_thickness = 2

        self.canvas.placeholder('pressure_value').place = (105, 230)
        self.canvas.placeholder('pressure_value').value = str(self.day_info.pressure) + ' mmHq'
        self.canvas.placeholder('pressure_value').font.font_scale = 1
        self.canvas.placeholder('pressure_value').font.font_thickness = 2

        self.canvas.placeholder('wind_field').place = (208, 230)
        self.canvas.placeholder('wind_field').value = 'Wind:'
        self.canvas.placeholder('wind_field').font.font_scale = 1
        self.canvas.placeholder('wind_field').font.font_thickness = 2

        wind_str_info = str(self.day_info.wind.speed) + 'm/s, ' + self.day_info.wind.direction

        self.canvas.placeholder('wind_value').place = (255, 230)
        self.canvas.placeholder('wind_value').value = wind_str_info
        self.canvas.placeholder('wind_value').font.font_scale = 1
        self.canvas.placeholder('wind_value').font.font_thickness = 2

        self.canvas.placeholder('humidity_field').place = (370, 230)
        self.canvas.placeholder('humidity_field').value = 'Humidity:'
        self.canvas.placeholder('humidity_field').font.font_scale = 1
        self.canvas.placeholder('humidity_field').font.font_thickness = 2

        self.canvas.placeholder('humidity_value').place = (455, 230)
        self.canvas.placeholder('humidity_value').value = self.day_info.humidity
        self.canvas.placeholder('humidity_value').font.font_scale = 1
        self.canvas.placeholder('humidity_value').font.font_thickness = 2

        self.canvas.placeholder('day_field').place = (270, 110)
        self.canvas.placeholder('day_field').value = str(self.day_info.temp.day)
        self.canvas.placeholder('day_field').font.font_scale = 4
        self.canvas.placeholder('day_field').font.font_thickness = 8

        self.canvas.placeholder('feels_like_field').place = (270, 145)
        self.canvas.placeholder('feels_like_field').value = 'Feels like:'
        self.canvas.placeholder('feels_like_field').font.font_scale = 1.3
        self.canvas.placeholder('feels_like_field').font.font_thickness = 2

        self.canvas.placeholder('feels_like_value').place = (385, 145)
        self.canvas.placeholder('feels_like_value').value = str(self.day_info.temp.feels_like)
        self.canvas.placeholder('feels_like_value').font.font_scale = 1.3
        self.canvas.placeholder('feels_like_value').font.font_thickness = 2

        self.canvas.placeholder('at_night_field').place = (282, 170)
        self.canvas.placeholder('at_night_field').value = 'At night:'
        self.canvas.placeholder('at_night_field').font.font_scale = 1.3
        self.canvas.placeholder('at_night_field').font.font_thickness = 2

        self.canvas.placeholder('at_night_value').place = (385, 170)
        self.canvas.placeholder('at_night_value').value = str(self.day_info.temp.night)
        self.canvas.placeholder('at_night_value').font.font_scale = 1.3
        self.canvas.placeholder('at_night_value').font.font_thickness = 2


class WeatherMaker:
    """
        Класс парсит страницу сайта 'https://yandex.ru/pogoda/ashgabat/month/.
        В результате получает прогноз погоды в Ашхабаде на месяц.
    """
    response: requests.models.Response
    html: bs4.BeautifulSoup
    days: Optional[List[DayWeather]]
    _from_day: Optional[int]
    _to_day: Optional[int]
    _index: int

    def __init__(self):
        self._index = 0
        self.response = requests.get('https://yandex.ru/pogoda/ashgabat/month/')
        self.html = bs4.BeautifulSoup(self.response.text, features='html.parser')
        self.days = list()
        self.parse()
        self.from_day = self.days[0].info['date']
        self.to_day = self.days[-1].info['date']

    def parse(self):
        """
            Метод парсит страницу и заполняет список self.days данными.
        :return: None
        """
        if not self.days:
            values = self.html.find_all('div', attrs={'class': 'climate-calendar-day__detailed-container-center'})

            for value in values:
                self.days.append(DayWeather(day_in_html=value))

    @property
    def from_day(self):
        """
            Метод устанавливает стартовыю дату для диапозона дат
        :return: Стартовая дата
        """
        return self._from_day

    @from_day.setter
    def from_day(self, day: datetime.date):
        self._from_day = day.toordinal()

    @property
    def to_day(self):
        """
            Метод устанавливает стартовыю дату для диапозона дат
        :return: Стартовая дата
        """
        return self._to_day

    @to_day.setter
    def to_day(self, day: datetime.date):
        self._to_day = day.toordinal()

    def setup_date_range(self, from_date: datetime.date = None, to_date: datetime.date = None):
        """
            Метод устанавливает диапозон дат для ограничения вывода
            Если начальная и/или конечная дата не заданы то выставляются начальная и конечная даты
            из спарсенного месяца.
        :param from_date: Начальная даа
        :param to_date: Конечная дата
        :return: None
        """

        self.from_day = from_date if from_date else self.days[0].info['date']
        self.to_day = to_date if to_date else self.days[-1].info['date']

        self.days = [day for day in self.days if day.info['date'].toordinal() in range(self.from_day, self.to_day + 1)]

    def display_all_in_range(self):
        """
            Метод выводит информацию о прогнозе погоды.
            Если установлен диапозон дат то вывод ограничевается установленным диапозоном.
        :return: None
        """
        for i, day in enumerate(self.days):
            if day.info['date'].toordinal() in range(self.from_day, self.to_day + 1):
                print(f'{i + 1}. Day info: {day.info}')

    def get_current(self):
        """
            Возвращает текущий (по индексу, не путать с сегодня) день.
        :return: Текущий в списке
        """
        return self.days[self._index]

    @property
    def index(self):
        """
            Метод возвращает индекс
        :return: Текущий индекс
        """
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    def get_all(self):
        """
            Метод возвращает список дней за установленный диапозон дат.
        :return: Список дней
        """
        pass

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.days):
            day = self.days[self.index]
            self.index += 1
            return day

        raise StopIteration


database_proxy = DatabaseProxy()


class DayRecord(pw.Model):
    """
        Модель для работы с таблицей
    """

    Date = pw.DateField(unique=True)
    Image = pw.CharField()
    Temp_day = pw.IntegerField()
    Temp_night = pw.IntegerField()
    Temp_feels_like = pw.IntegerField()
    Pressure = pw.IntegerField()
    Humidity = pw.IntegerField()
    Wind_speed = pw.FloatField()
    Wind_direction = pw.CharField()
    Wind_gust = pw.CharField()
    Conditions = pw.CharField()

    class Meta:
        """
            Мета-класс
        """
        database = database_proxy


class DatabaseUpdater:
    """
        Класс проводит операции с базой данных
    """
    model: Type[DayRecord]
    db: pw.SqliteDatabase

    def __init__(self, url: str):
        self.db = connect(url)
        database_proxy.initialize(self.db)
        self.db.create_tables([DayRecord])
        self.model = DayRecord

    def select(self, start: datetime.date, finish: datetime.date) -> pw.ModelSelect:
        """
            Метод возвращает модель с записями на указанные даты
        :return: pw.ModelSelect
        """
        return self.model.select().where(self.model.Date.between(start, finish))

    def insert(self, day_record: DayWeather) -> tuple:
        """
            Метод вставляет запись в базу данных
        :return: tuple - (DayRecord, created: bool)
        """
        return self.model.get_or_create(Date=day_record.date,
                                        defaults={'Image': day_record.image,
                                                  'Temp_day': day_record.temp.day,
                                                  'Temp_night': day_record.temp.night,
                                                  'Temp_feels_like': day_record.temp.feels_like,
                                                  'Pressure': day_record.pressure,
                                                  'Humidity': day_record.humidity,
                                                  'Wind_speed': day_record.wind.speed,
                                                  'Wind_direction': day_record.wind.direction,
                                                  'Wind_gust': day_record.wind.gust,
                                                  'Conditions': day_record.conditions
                                                  }
                                        )

    def update(self, day_record: DayWeather):
        """
            Метод обновляет запись в базе данных
        :return: None
        """
        try:
            record = self.model.get(self.model.Date == day_record.date)

            record.Image = day_record.image
            record.Temp_day, record.Temp_night, record.Temp_feels_like = day_record.temp.info.values()
            record.Pressure = day_record.pressure
            record.Humidity = day_record.humidity
            record.Wind_speed, record.Wind_directions, record.Wind_gust = day_record.wind.info.values()
            record.Conditions = day_record.conditions

            record.save()

        except self.model.DoesNotExist:
            self.insert(day_record)


def main():
    """
        Функция выполняется в случае непосредственого запуска скрипта используется для тестирования
    :return: None
    """
    weather = WeatherMaker()
    today = datetime.date.today()
    to_date = today.toordinal() + 6
    weather.setup_date_range(from_date=today, to_date=datetime.date.fromordinal(to_date))

    print("Выведем данные о погоде на следующие 7 дней начиная с текущего:")
    for day in weather:
        print(f'Дата: {day.date}')
        print(f'{"Температура:":^15}{"Давление:":^15}{"Влажность:":^15}{"Ветер:":^25}{"Условия:":^45}')
        print(f'{"Днем:":>10}'
              f'{day.temp.day:>5}'
              f'{day.pressure:^15}'
              f'{day.humidity:^15}'
              f'{"Скорость:":>15}'
              f'{day.wind.speed:>10}'
              f'{day.conditions:^45}')
        print(f'{"Ночью:":>10}'
              f'{day.temp.night:>5}'
              f'{"":^15}'
              f'{"":^15}'
              f'{"Направление:":>15}'
              f'{day.wind.direction:>10}')
        print(f'{"Ощущается:":>10}'
              f'{day.temp.feels_like:>5}'
              f'{"":^15}'
              f'{"":^15}'
              f'{"Порывы:":>15}'
              f'{day.wind.gust:>10}')


if __name__ == '__main__':
    main()
