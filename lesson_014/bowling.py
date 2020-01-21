# -*- coding: utf-8 -*-
"""
    Модуль для посчета результатов игры в боулинг
"""
import re
# TODO Неиспользуемый импорт
from collections import Counter
from typing import List, Optional

# TODO Обращайте внимание на предупреждения среды разработки о
#  проблемах в коде или нарушении стандарта PEP 8.
#  Попробуйте найти зеленую галочку справа над полосой прокрутки.
#  Если вместо нее, квадрат красного, желтого или серого цвета,
#  значит в файле есть недостатки оформления или ошибки.

# TODO Лишние пустые строки в конце файла.


class Bowling:
    """
        Класс выполняет подсчет результатов бросков в боулинге.
        Принемает результат игры в виде строки (пример: "81-/5/-67-35X253/X")
    """
    __game_result: str
    __score: List
    __number_of_frames: int
    __frames: Optional[List[str]]
    __result: int

    def __init__(self, game_result: str, frames: int = 10):
        self.__game_result = game_result
        self.__frames = re.findall(r'X|[-\d]{2}|[\d-]/', game_result.upper())
        self.__score = []
        self.__number_of_frames = frames
        self.__result = 0

        self.check_parameters()

    def get_score(self):
        """
            Метод выводит результат игры
        """
        self.parse_result()

        return self.__result

    def parse_result(self):
        """
            Метод парсит полученный результат и подсчитывает очки.
        """
        for frame in self.__frames:
            self.result += self.check_frame(frame)

        return self.result

    @property
    def result(self):
        """
            Метод-свойство возвращает текущее состояние переменной __result
        """
        return self.__result

    @result.setter
    def result(self, result):
        self.__result = result

    def check_frame(self, frame):
        """"
            Преверяет фрайм на соответсвтие паттерну
        """
        result = 0

        if frame == 'X':
            result = 20
        elif '/' in frame:
            result = 15
        else:
            str_frame = frame.replace('-', '0')

            for symbol in str_frame:
                result += int(symbol)

            if result > 10:
                raise ValueError(f'Результат бросков во фрейме не может быть больше 10: "{frame}"')
            elif result == 10:
                raise ValueError(f'Spare бросок записывает в виде <число>/, вместо: "{frame}"')

        self.__score.append([frame, result])

        return result

    def check_parameters(self):
        """
            Метод проверяет входные параметры на валидность.
            В случае невалидности входных параметров вызывает исключения ValueError.
        :return: None
        """

        game_result = ''.join(self.__frames)

        if game_result != self.__game_result:
            raise ValueError(f'Ошибка при вводе результатов игры. Введены неполные или некорректные данные.')

        if self.__number_of_frames != len(self.__frames):
            raise ValueError(f'Неправильное количество фреймов "{self.__number_of_frames}" '
                             f'для указанного результата игры "{self.__game_result}"')



