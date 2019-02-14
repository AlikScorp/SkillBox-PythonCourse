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


def polygon(sp, angle, side_length, angle_qty, shape_color=sd.COLOR_YELLOW):
    """
        Фунцкция чертит правильный многоугольник
    """
    start, width = sp, 3
    for side in range(angle_qty - 1):
        vector = sd.get_vector(start_point=sp, angle=angle + side * (360 / angle_qty), length=side_length, width=width)
        vector.draw(color=shape_color)
        sp = vector.end_point

    sd.line(sp, start, color=shape_color, width=width)


def triangle(sp, angle, side_length, shape_color=sd.COLOR_YELLOW):
    """
        Фунцкция чертит треугольник. Вызывает функцию polygon и передает ей количество углов равное 3
    """
    polygon(sp=sp, angle=angle, side_length=side_length, angle_qty=3, shape_color=shape_color)


def square(sp, angle, side_length, shape_color=sd.COLOR_YELLOW):
    """
        Фунцкция чертит квадрат. Вызывает функцию polygon и передает ей количество углов равное 4
    """
    polygon(sp=sp, angle=angle, side_length=side_length, angle_qty=4, shape_color=shape_color)


def pentagon(sp, angle, side_length, shape_color=sd.COLOR_YELLOW):
    """
        Фунцкция чертит пятиуголник. Вызывает функцию polygon и передает ей количество углов равное 5
    """
    polygon(sp=sp, angle=angle, side_length=side_length, angle_qty=5, shape_color=shape_color)


def hexagon(sp, angle, side_length, shape_color=sd.COLOR_YELLOW):
    """
        Фунцкция чертит шестиугольник. Вызывает функцию polygon и передает ей количество углов равное 6
    """
    polygon(sp=sp, angle=angle, side_length=side_length, angle_qty=6, shape_color=shape_color)


colors = {'0': ['red', sd.COLOR_RED], '1': ['orange', sd.COLOR_ORANGE],
          '2': ['yellow', sd.COLOR_YELLOW], '3': ['green', sd.COLOR_GREEN],
          '4': ['cyan', sd.COLOR_CYAN], '5': ['blue', sd.COLOR_BLUE], '6': ['purple', sd.COLOR_PURPLE]}

print("Возможные цвета:")
for key, color in colors.items():
    print(key, ':', color[0])

color = input("Введите желаемый цвет > ")

while True:
    if 0 <= int(color) <= 6:
        break
    else:
        print("Вы ввели некоректный номер!")
        color = input("Введите желаемый цвет > ")

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
