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


def triangle(sp, angle, side_length, shape_color=sd.COLOR_YELLOW):
    """
        Фунцкция чертит треугольник
    """
    n, start, width = 3, sp, 3
    for side in range(n - 1):
        vector = sd.get_vector(start_point=sp, angle=angle+side*(360/n), length=side_length, width=width)
        vector.draw(color=shape_color)
        sp = vector.end_point

    sd.line(sp, start, color=shape_color, width=width)


def square(sp, angle, side_length, shape_color=sd.COLOR_YELLOW):
    """
        Фунцкция чертит квадрат
    """
    n, start, width = 4, sp, 3
    for side in range(n - 1):
        vector = sd.get_vector(start_point=sp, angle=angle+side*(360/n), length=side_length, width=width)
        vector.draw(color=shape_color)
        sp = vector.end_point

    sd.line(sp, start, color=shape_color, width=width)


def pentagon(sp, angle, side_length, shape_color=sd.COLOR_YELLOW):
    """
        Фунцкция чертит пятиуголник
    """
    n, start, width = 5, sp, 3
    for side in range(n - 1):
        vector = sd.get_vector(start_point=sp, angle=angle+side*(360/n), length=side_length, width=width)
        vector.draw(color=shape_color)
        sp = vector.end_point

    sd.line(sp, start, color=shape_color, width=width)


def hexagon(sp, angle, side_length, shape_color=sd.COLOR_YELLOW):
    """
        Фунцкция чертит шестиугольник
    """
    n, start, width = 6, sp, 3
    for side in range(n - 1):
        vector = sd.get_vector(start_point=sp, angle=angle+side*(360/n), length=side_length, width=width)
        vector.draw(color=shape_color)
        sp = vector.end_point

    sd.line(sp, start, color=shape_color, width=width)


colors = {'0': ['red', sd.COLOR_RED], '1': ['orange', sd.COLOR_ORANGE],
          '2': ['yellow', sd.COLOR_YELLOW], '3': ['green', sd.COLOR_GREEN],
          '4': ['cyan', sd.COLOR_CYAN], '5': ['blue', sd.COLOR_BLUE], '6': ['purple', sd.COLOR_PURPLE]}

print("Возможные цвета:")
for key, color in colors.items():
    print(key, ':', color[0])

color = input("Введите желаемый цвет > ")
while int(color) not in range(7):
    print("Вы ввели некоректный номер!")
    color = input("Введите желаемый цвет > ")
# TODO Можно сделать цикл ввода значения кода так:
#  while True:
#      if 0 < color < 7:
#          color = int(input())
#          break

print('Color is:', colors[color][0])

size = 100
start_angle = 45
shapes_color = colors[color][1]

triangle_start_point = sd.get_point(200, 100)
square_start_point = sd.get_point(500, 100)
pentagon_start_point = sd.get_point(200, 400)
hexagon_start_point = sd.get_point(500, 400)

triangle(triangle_start_point, start_angle, size, shape_color=shapes_color)
square(square_start_point, start_angle, size, shape_color=shapes_color)
pentagon(pentagon_start_point, start_angle, size, shape_color=shapes_color)
hexagon(hexagon_start_point, start_angle, size, shape_color=shapes_color)

sd.pause()
# TODO Нужно обновить функции рисования фигур после исправления первого задания.