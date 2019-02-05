# -*- coding: utf-8 -*-

# (определение функций)
import simple_draw as sd


# Написать функцию отрисовки смайлика в произвольной точке экрана
# Форма рожицы-смайлика на ваше усмотрение
# Параметры функции: кордината X, координата Y, цвет.
# Вывести 10 смайликов в произвольных точках экрана.

def draw_smile(size, center=sd.random_point(), color=sd.random_color()):
    x = center.x
    y = center.y
    width = 1
    left_eye = sd.get_point(x - size / 2.5, y + size / 3)
    right_eye = sd.get_point(x + size / 2.5, y + size / 3)

    sd.circle(center, size, color, width)
    sd.circle(left_eye, size // 10, color, width)
    sd.circle(right_eye, size // 10, color, width)
    sd.circle(center, size // 6, sd.COLOR_RED, 0)

    points = [sd.get_point(x - size / 2, y - size // 3), sd.get_point(x - size // 4, y - size / 2),
              sd.get_point(x + size // 4, y - size / 2), sd.get_point(x + size / 2, y - size // 3)]

    sd.lines(points, color, False, 2)

    points = [sd.get_point(x - size // 4, y - size / 2), sd.get_point(x, y - size / 1.5),
              sd.get_point(x + size // 4, y - size / 2)]

    sd.lines(points, color, True, 2)


for i in range(0, 10):
    draw_smile(50, sd.random_point())

sd.pause()

# зачет!
