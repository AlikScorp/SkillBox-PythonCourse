# -*- coding: utf-8 -*-
"""
    Модуль тестирования класса Bowling
"""
import unittest
from ..bowling import Bowling


class BowlingTests(unittest.TestCase):

    def test_strikes(self):
        game = Bowling(game_result='XXXXXXXXXX', frames=10)
        self.assertEqual(game.get_score(), 200, 'Не работает подсчет для случая 10 Strike бросков')

    def test_spare(self):
        game = Bowling(game_result='5/6/7/6/2/2/9/1/4/2/', frames=10)
        self.assertEqual(game.get_score(), 150, 'Не работает подсчет для случая 10 Spare бросков')

    def test_all_ten(self):
        game = Bowling(game_result='5463716127259-184523', frames=10)
        self.assertEqual(game.get_score(), 81, 'Не работает подсчет для случая 10/10 бросков')

    def test_all_missed(self):
        game = Bowling(game_result='--------------------', frames=10)
        self.assertEqual(game.get_score(), 0, 'Не работает подсчет для случая "Все броски мимо"')

    def test_first_missed(self):
        game = Bowling(game_result='-1-2-3-4-5-6-7-8-9-1', frames=10)
        self.assertEqual(game.get_score(), 46, 'Не работает подсчет для случая "Первые броски мимо"')

    def test_second_missed(self):
        game = Bowling(game_result='1-2-3-4-5-6-7-8-9-1-', frames=10)
        self.assertEqual(game.get_score(), 46, 'Не работает подсчет для случая "Вторые броски мимо"')

    def test_mixed(self):
        game = Bowling(game_result='81--5/-67-36X273/X', frames=10)
        self.assertEqual(game.get_score(), 110, 'Не работает подсчет для случая "Смешанные броски"')

    def test_three_frame(self):
        game = Bowling(game_result='81--5/', frames=3)
        self.assertEqual(game.get_score(), 24, 'Не работает подсчет для случая трех фреймов')

    def test_wrong_number_of_frame(self):
        with self.assertRaises(ValueError, msg='Не выбрасывается исключение в случае неправильного количества фреймов'):
            Bowling(game_result='82--5/', frames=10)

    def test_raising_of_exception(self):
        game = Bowling(game_result='83--5/', frames=3)
        with self.assertRaises(ValueError, msg='Не срабатывает исключение если сумма бросков во фрейме больше 10'):
            game.check_frame('95')

    def test_raising_of_exception_incorrect_data(self):
        with self.assertRaises(ValueError, msg='Не срабатывает исключение если введены неполные/некорректные данные'):
            Bowling(game_result='4XXX', frames=3)

    def test_raising_of_exception_result_equal_ten(self):
        with self.assertRaises(ValueError, msg='Не срабатывает исключение если результат бросков равен 10'):
            game = Bowling(game_result='55XX', frames=3)
            game.get_score()


if __name__ == '__main__':
    unittest.main()
