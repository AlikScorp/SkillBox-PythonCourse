# -*- coding: utf-8 -*-

import simple_draw as sd

# Написать функции рисования равносторонних геометрических фигур:
# - треугольника
# - квадрата
# - пятиугольника
# - шестиугольника
# Все функции должны принимать 3 параметра:
# - точка начала рисования
# - угол наклона
# - длина стороны

# Нарисовать все фигуры
# Выделить общую часть алгоритма рисования в отдельную функцию
# Придумать, как устранить разрыв в начальной точке фигуры

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# sd.line()
# Результат решения см lesson_004/results/exercise_01_shapes.jpg


def polygon(sp, angle, side_length, angle_qty):
    """
        Фунцкция чертит правильный многоугольник
    """
    start, width = sp, 3
    for side in range(angle_qty - 1):
        vector = sd.get_vector(start_point=sp, angle=angle + side * (360 / angle_qty), length=side_length, width=width)
        vector.draw()
        sp = vector.end_point

    sd.line(sp, start, width=width)


def triangle(sp, angle, side_length):
    """
        Фунцкция чертит треугольник
    """
    n, start, width = 3, sp, 3
    for side in range(n - 1):
        vector = sd.get_vector(start_point=sp, angle=angle+side*(360/n), length=side_length, width=width)
        vector.draw()
        sp = vector.end_point

    sd.line(sp, start, width=width)


def square(sp, angle, side_length):
    """
        Фунцкция чертит квадрат
    """
    n, start, width = 4, sp, 3
    for side in range(n - 1):
        vector = sd.get_vector(start_point=sp, angle=angle+side*(360/n), length=side_length, width=width)
        vector.draw()
        sp = vector.end_point

    sd.line(sp, start, width=width)


def pentagon(sp, angle, side_length):
    """
        Фунцкция чертит пятиуголник
    """
    n, start, width = 5, sp, 3
    for side in range(n - 1):
        vector = sd.get_vector(start_point=sp, angle=angle+side*(360/n), length=side_length, width=width)
        vector.draw()
        sp = vector.end_point

    sd.line(sp, start, width=width)


def hexagon(sp, angle, side_length):
    """
        Фунцкция чертит шестиугольник
    """
    n, start, width = 6, sp, 3
    for side in range(n - 1):
        vector = sd.get_vector(start_point=sp, angle=angle+side*(360/n), length=side_length, width=width)
        vector.draw()
        sp = vector.end_point

    sd.line(sp, start, width=width)


length = 100
start_angle = 45

x = sd.resolution[0]/4
y = sd.resolution[1]/4-length/2
start_point = sd.get_point(x, y)

triangle(start_point, start_angle, length)

x = 3*sd.resolution[0]/4
y = sd.resolution[1]/4-length/2
start_point = sd.get_point(x, y)

square(start_point, start_angle, length)

x = 3*sd.resolution[0]/4
y = 3*sd.resolution[1]/4-length
start_point = sd.get_point(x, y)

hexagon(start_point, start_angle, length)

x = sd.resolution[0]/4
y = 3*sd.resolution[1]/4-length
start_point = sd.get_point(x, y)

pentagon(start_point, start_angle, length)


x = sd.resolution[0]/2+length/2
y = sd.resolution[1]/2-length
start_point = sd.get_point(x, y)

polygon(start_point, start_angle, length, 8)

sd.pause()

# Ура. Докстринги.
# TODO Функции вы сделали, но в задании было написано что функции рисования отдельных фигур
#  должны вызывать функцию рисования полигона с нужными параметрами.
