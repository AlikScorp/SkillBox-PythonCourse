# -*- coding: utf-8 -*-

from lesson_006.mastermind_engine import generate_number, check_number
from termcolor import colored, cprint
# TODO Неплохое решение, сделать код универсальным для
#  чисел разной длины.
capacity = 4

# Игра «Быки и коровы»
# https://goo.gl/Go2mb9
#
# Правила:
# Компьютер загадывает четырехзначное число, все цифры которого различны
# (первая цифра числа отлична от нуля). Игроку необходимо разгадать задуманное число.
# Игрок вводит четырехзначное число c неповторяющимися цифрами,
# компьютер сообщают о количестве «быков» и «коров» в названном числе
# «бык» — цифра есть в записи задуманного числа и стоит в той же позиции,
#       что и в задуманном числе
# «корова» — цифра есть в записи задуманного числа, но не стоит в той же позиции,
#       что и в задуманном числе
#
# Например, если задумано число 3275 и названо число 1234,
# получаем в названном числе одного «быка» и одну «корову».
# Очевидно, что число отгадано в том случае, если имеем 4 «быка».
#
# Формат ответа компьютера
# > быки - 1, коровы - 1


# Составить отдельный модуль mastermind_engine, реализующий функциональность игры.
# В этом модуле нужно реализовать функции:
#   загадать_число()
#   проверить_число(NN) - возвращает словарь {'bulls': N, 'cows': N}
# Загаданное число хранить в глобальной переменной.
# Обратите внимание, что строки - это список символов.
#
# В текущем модуле (lesson_006/01_mastermind.py) реализовать логику работы с пользователем:
#   модуль движка загадывает число
#   в цикле, пока число не отгадано
#       у пользователя запрашивается вариант числа
#       модуль движка проверяет число и выдает быков/коров
#       результат быков/коров выводится на консоль
#  когда игрок угадал таки число - показать количество ходов и вопрос "Хотите еще партию?"
#
# При написании кода учитывайте, что движок игры никак не должен взаимодействовать с пользователем.
# Все общение с пользователем делать в текущем модуле. Представьте, что движок игры могут использовать
# разные клиенты - веб, чатбот, приложение, етс - они знают как спрашивать и отвечать пользователю.
# Движок игры реализует только саму функциональность игры.
# Это пример применения SOLID принципа (см https://goo.gl/GFMoaI) в архитектуре программ.
# Точнее, в этом случае важен принцип единственной ответственности - https://goo.gl/rYb3hT

generate_number(capacity)
round_number = 1
message = 'Сыграем в "Быка и Корову"? Я загадал число!\n' \
          'Число из {} цифр! Цифры в числе не повторяются и число не начинаться с нуля'.format(capacity)
cprint(message, color='blue')
while True:
    cprint('Раунд {}'.format(round_number), color='red')
    user_number = input(colored('Введите число: ', color='cyan'))
    round_number += 1
    result = check_number(user_number)
    message = '> Быки - {}, Коровы - {}'.format(result['bulls'], result['cows'])
    cprint(message, color='blue')
    if result['bulls'] == 4:
        message = 'Поздравляю! Вы победили! Искомое число - {}'.format(user_number)
        cprint(message, 'red')
        answer = input(colored('Сыграем еще? ', color='blue'))
        # TODO Здесь можно проверять if answer in ['Да', 'да']
        if answer == 'да' or answer == 'Да':
            generate_number(capacity)
            round_number = 1
            continue
        else:
            break

# TODO Можно немного усложнить процесс решения, если запретить водить для проверки
#  одинаковые цифры.
#  Нужно немного структурировать код. Желательно отделить обработку ввода пользователя
#  от его проверки.
#  В целом для первой проверки довольно неплохо.
