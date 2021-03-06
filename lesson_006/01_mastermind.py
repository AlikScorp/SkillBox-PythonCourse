# -*- coding: utf-8 -*-

from lesson_006.mastermind_engine import generate_number, check_number
from termcolor import colored, cprint

capacity = 4

SUCCESS = 0
DUPLICATION_OF_DIGIT = 1
START_FROM_ZERO = 2
NUMBER_TOO_LONG = 3
NUMBER_TOO_SHORT = 4

error_message = ['Сравниваем с задуманным ...',
                 'Дублирование цифр в числе. В числе не должно быть одинаковых цифр!',
                 'Нуль в начале числа. Число не должно начинаться с нуля!',
                 'Число слишком большое, цифр в числе должно быть {}!'.format(capacity),
                 'Число слишком маленькое, цифр в числе должно быть {}!'.format(capacity)]

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


def check_user_number(number):
    """
        Проверяем что все цифры в числе уникальны и их количество равно capacity
    :param number: Проверяемое число
    :return: True если количество цифр равно capacity и False если нет
    """
    if number[0] == '0':
        return START_FROM_ZERO
    elif len(number) < capacity:
        return NUMBER_TOO_SHORT
    elif len(set(number)) < capacity:
        return DUPLICATION_OF_DIGIT
    elif len(number) > capacity:
        return NUMBER_TOO_LONG
    else:
        return SUCCESS


def get_user_number():
    """
        Получаем от пользователя число разрядностью capacity и проверям его с помощью check_user_number
    :return: Полученное от пользователя число
    """
    number = input(colored('Введите число: ', color='cyan'))
    err_number = check_user_number(number)

    while err_number:
        cprint('Некоректный ввод!', color='red')
        cprint(error_message[err_number], color='red')

        number = input(colored('Введите число: ', color='cyan'))
        err_number = check_user_number(number)

    cprint(error_message[err_number], color='cyan')
    return number


generate_number(capacity)
round_number = 1
message = 'Сыграем в "Быка и Корову"? Я загадал число!\n' \
          'Число из {} цифр! Цифры в числе не повторяются и число не начинаться с нуля'.format(capacity)
cprint(message, color='blue')

while True:
    cprint('Раунд {}'.format(round_number), color='red')
    round_number += 1

    user_number = get_user_number()

    result = check_number(user_number)

    if result['bulls'] == capacity:
        message = 'Поздравляю! Вы победили!\nИскомое число - {}'.format(user_number)
        cprint(message, 'red')
        answer = input(colored('Сыграем еще? ', color='blue'))
        if answer in ['да', 'Да']:
            generate_number(capacity)
            round_number = 1
            continue
        else:
            break
    else:
        message = '> Быки - {}, Коровы - {}'.format(result['bulls'], result['cows'])
        cprint(message, color='blue')

# зачет!
