# -*- coding: utf-8 -*-
import simple_draw as sd

# Добавить цвет в функции рисования геом. фигур. из упр lesson_004/01_shapes.py
# (код функций скопировать сюда и изменить)
# Запросить у пользователя цвет фигуры посредством выбора из существующих:
#   вывести список всех цветов с номерами и ждать ввода номера желаемого цвета.
# Потом нарисовать все фигуры этим цветом

# Пригодятся функции
# sd.get_point()
# sd.line()
# sd.get_vector()
# и константы COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN, COLOR_BLUE, COLOR_PURPLE
# Результат решения см lesson_004/results/exercise_02_global_color.jpg


def polygon(start_point, angle, length, color=sd.COLOR_DARK_GREEN, width=2):
    n = int(360/angle)
    x, y = start_point.x, start_point.y

    for i in range(n-1):
        vector = sd.get_vector(start_point=start_point, angle=angle+i*angle, length=length, width=width)
        vector.draw(color=color)
        start_point = vector.end_point

    sd.line(sd.get_point(x, y), start_point, color=color, width=width)


colors = [['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple'], [sd.COLOR_RED, sd.COLOR_ORANGE,
          sd.COLOR_YELLOW, sd.COLOR_GREEN, sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE]]

points = [[200, 100], [500, 100], [200, 400], [500, 400]]

print("Возможные цвета:")
for num, color in enumerate(colors[0]):
    print(num, ':', color)

clr = int(input("Введите желаемый цвет > "))
while clr not in range(7):
    print("Вы ввели некоректный номер!")
    clr = int(input("Введите желаемый цвет > "))

clr = colors[1][clr]
size = 100

for i in [3, 4, 5, 6]:
    point = sd.get_point(points[i-3][0], points[i-3][1])
    polygon(point, angle=360/i, color=clr, length=size)


sd.pause()

# TODO Сложновато получилось. Сначалы вы делаете список colors, после этого
#  enumerate(colors[0]). Можно завести словарь, и сохранять название и значение
#  цвета в нем.
