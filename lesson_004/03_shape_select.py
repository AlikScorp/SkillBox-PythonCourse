# -*- coding: utf-8 -*-

import simple_draw as sd

# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg


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


shapes = ['треугольник', 'квадрат', 'пятиугольник', 'шестиугольник']
print('Возможные фигуры:')
for i, shape in enumerate(shapes):
    print('\t', i, ':', shape)

shape = input('Введите желаемую фигуру: ')
while int(shape) not in range(4):
    print('Вы ввели некоректный номер!')
    shape = input('Введите желаемую фигуру: ')

print("Желаемая фигура:", shapes[int(shape)])

shape_number = int(shape)
start_angle = 45
length = 150
x, y = sd.resolution[0]/2, sd.resolution[1]/2-length/2
start_point = sd.get_point(x, y)

if shape_number == 0:
    triangle(start_point, start_angle, length)
elif shape_number == 1:
    square(start_point, start_angle, length)
elif shape_number == 2:
    pentagon(start_point, start_angle, length)
else:
    hexagon(start_point, start_angle, length)

sd.pause()
