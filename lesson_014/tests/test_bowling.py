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
        game = Bowling(game_result='55647364282891194628', frames=10)
        self.assertEqual(game.get_score(), 100, 'Не работает подсчет для случая 10/10 бросков')

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
        game = Bowling(game_result='82--5/-67-37x283/X', frames=10)
        self.assertEqual(game.get_score(), 113, 'Не работает подсчет для случая "Смешанные броски"')

    def test_three_frame(self):
        game = Bowling(game_result='82--5/', frames=3)
        self.assertEqual(game.get_score(), 25, 'Не работает подсчет для случая трех фреймов')

    def test_wrong_number_of_frame(self):
        with self.assertRaises(ValueError, msg='Не выбрасывается исключение в случае неправильного количества фреймов'):
            Bowling(game_result='82--5/', frames=10)

    def test_raising_of_exception(self):
        game = Bowling(game_result='82--5/', frames=3)
        with self.assertRaises(ValueError, msg='Не срабатывает исключение если сумма бросков во фрейме больше 10'):
            game.check_frame('98')


if __name__ == '__main__':
    unittest.main()
# TODO На тесте game_result='55XX', frames=3 должна быть ошибка,
#  т.к. в первом фрейме все 10 кеглей сбиты и должно быть /
# TODO game_result='4XXX', frames=3 должна быть ошибка
