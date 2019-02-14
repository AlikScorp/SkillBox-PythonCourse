# -*- coding: utf-8 -*-

import simple_draw as sd

# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg


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


# Я бы отформатировал этот словарь так.
shapes = {'0': ['треугольник', triangle],
          '1': ['квадрат', square],
          '2': ['пятиугольник', pentagon],
          '3': ['шестиугольник', hexagon]}

print('Возможные фигуры:')
for key, shape in shapes.items():
    print('\t', key, ':', shape[0])

shape = input('Введите желаемую фигуру: ')
while True:
    if 0 <= int(shape) <= 3:
        break
    else:
        print('Вы ввели некоректный номер!')
        shape = input('Введите желаемую фигуру: ')

print("Желаемая фигура:", shapes[shape][0])

start_angle = 45
length = 150
x, y = sd.resolution[0]/2, sd.resolution[1]/2-length/2
start_point = sd.get_point(x, y)
draw_shape = shapes[shape][1]
draw_shape(start_point, start_angle, length)

sd.pause()

# зачет!
