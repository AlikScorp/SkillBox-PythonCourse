"""
    Модуль содержит классы для работы с изибражениеми.
    Классы позволяют добавлять в исходные изображения текстовые поля и другие изображения.
"""
import os
from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, Tuple
import cv2
import numpy
from termcolor import cprint


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

    def size(self):
        """
            Возвращает размер плейсхолдера с учетом шрифта
        :return:
        """
        if self.type == 'text':
            return cv2.getTextSize(self.value, self.font.font_face, self.font.font_scale, self.font.font_thickness)
        else:
            return cv2.imread(self.value).shape


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
        cv2.imwrite(path, self.template)

        return True

    def size(self):
        """
            Возвращает размер шаблона
        :return: tuple
        """
        return self.template.shape


class GradientDirections(IntEnum):
    """
        Класс содержит константы для обозначаения направления заливки
    """
    TOP_TO_BOTTOM = 1
    BOTTOM_TO_TOP = 2
    LEFT_TO_RIGHT = 3
    RIGHT_TO_LEFT = 4
