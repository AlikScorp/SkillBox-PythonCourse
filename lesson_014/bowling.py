"""
    Модуль для посчета результатов игры в боулинг
"""
import re
from typing import List, Optional


class Bowling:
    """
        Класс выполняет подсчет результатов бросков в боулинге.
        Принемает результат игры в виде строки (пример: "82--5/-67-37x283/X")
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

        # assert self.__number_of_frames == len(self.__frames), 'Количество фреймов не соответствует результатам игры'

        if self.__number_of_frames != len(self.__frames):
            raise ValueError(f'Неправильное количество фреймов "{self.__number_of_frames}" '
                             f'для указанного результата игры "{self.__game_result}"')

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
                raise ValueError(f'Неправильные результаты бросков во фрейме: "{frame}"')

        self.__score.append([frame, result])

        return result



