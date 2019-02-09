# -*- coding: utf-8 -*-

import simple_draw as sd
from math import sin, cos, pi

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


length = 100

for i in [3, 4, 5, 6]:
    point = sd.get_point((i-2)*100, (i-2)*100)
    polygon(point, angle=360/i, length=length)
    draw_polygon(point, i, length)

sd.pause()
