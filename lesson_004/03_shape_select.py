# -*- coding: utf-8 -*-

import simple_draw as sd
from math import sin, cos, pi

# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg


def polygon(start_point, angle, length, color=sd.COLOR_DARK_GREEN, width=2):
    n = int(360/angle)
    x, y = start_point.x, start_point.y

    for i in range(n-1):
        vector = sd.get_vector(start_point=start_point, angle=angle+i*angle, length=length, width=width)
        vector.draw(color=color)
        start_point = vector.end_point

    sd.line(sd.get_point(x, y), start_point, color=color, width=width)


def draw_polygon(center, angles=3, size=100):
    """
        Более математическая версия. Рисует многоугольник с центром в точке center, с количеством углов angles
        и размером (радиус описанной вокруг многоугольника окружности) size.
    """

    points = list()
    x, y = center.x, center.y

    for i in range(angles):
        x1 = x + size*cos(90+(2*pi*i)/angles)
        y1 = y + size*sin(90+(2*pi*i)/angles)
        points.append(sd.get_point(x1, y1))

    sd.polygon(points, width=2)


shapes = ['треугольник', 'квадрат', 'пятиугольник', 'шестиугольник']
print('Возможные фигуры:')
for i, shape in enumerate(shapes):
    print('\t', i, ':', shape)

shape = input('Введите желаемую фигуру: ')
while int(shape) not in range(4):
    print('Вы ввели некоректный номер!')
    shape = input('Введите желаемую фигуру: ')


center = sd.get_point(sd.resolution[0]/2, sd.resolution[1]/2)
draw_polygon(center=center, angles=int(shape)+3, size=150)

center = sd.get_point(350, 250)
polygon(center, 360/(int(shape)+3), 100)

sd.pause()

# TODO Нужно использовать функции рисования фигур которые вы должны были сделать в  первом задании.
