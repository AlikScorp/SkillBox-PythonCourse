# -*- coding: utf-8 -*-

# День сурка
#
# Напишите функцию one_day() которая возвращает количество кармы от 1 до 7
# и может выкидывать исключения:
# - IamGodError
# - DrunkError
# - CarCrashError
# - GluttonyError
# - DepressionError
# - SuicideError
# Одно из этих исключений выбрасывается с вероятностью 1 к 13 каждый день
#
# Функцию оберните в бесконечный цикл, выход из которого возможен только при накоплении
# кармы до уровня ENLIGHTENMENT_CARMA_LEVEL. Исключения обработать и записать в лог.
# При создании собственных исключений максимально использовать функциональность
# базовых встроенных исключений.

from random import randint

ENLIGHTENMENT_CARMA_LEVEL = 777


class GroundhogDayError(Exception):
    pass


class IamGodError(GroundhogDayError):
    pass


class DrunkError(GroundhogDayError):
    pass


class CarCrushError(GroundhogDayError):
    pass


class GluttonyError(GroundhogDayError):
    pass


class DepressionError(GroundhogDayError):
    pass


class SuicideError(GroundhogDayError):
    pass


def one_day():
    karma = randint(1, 13)

    if karma <= 7:
        return karma
    elif karma == 8:
        raise IamGodError("I'm a god. I'm not *the* God... I don't think.")
    elif karma == 9:
        raise DrunkError("Drunk is more fun.")
    elif karma == 10:
        raise CarCrushError("I'm betting he's going to swerve first.")
    elif karma == 11:
        raise GluttonyError("Would you like to come to dinner with Larry and me?")
    elif karma == 12:
        raise DepressionError("Well, what if there is no tomorrow? There wasn't one today.")
    else:
        raise SuicideError("I've been stabbed, shocked, poisoned, frozen, hung, electrocuted, and burned.")


total_karma = 0
f = None

try:
    f = open('groundhog_day.log', 'w')
except OSError as exc:
    print(f"The file cannot be opened: {exc}")
else:
    while total_karma < ENLIGHTENMENT_CARMA_LEVEL:
        try:
            total_karma += one_day()
        except GroundhogDayError as exc:
            f.write(f"{exc.__class__} -> {exc}\n")
finally:
    if f is not None:
        f.close()

print(f'The total karma is: {total_karma}')

# https://goo.gl/JnsDqu

# зачет!
