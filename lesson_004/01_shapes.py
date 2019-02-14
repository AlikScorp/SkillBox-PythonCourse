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


# Раз вы начали документировать ваши функции с помощью docstring,
#  То можно сделать следующий шаг и описать аргументы.
#  Например не всем будет понятно что sp расшифровывается как start_point.
#  По хорошему sp стоит переименовать.
#  Если вы планируете профессионально разрабатывать на современном python,
#  то в качестве внеклассного чтения почитайте о аннотации типов (type annotations).
def polygon(sp, angle, side_length, angle_qty):
    """
        Фунцкция чертит правильный многоугольник.

        :param sp: Начальная точка
        :param angle Угол под которым отображается фигура
        :param side_length Длина стороны
        :param angle_qty Количество углов фигуры
    """
    start, width = sp, 3
    for side in range(angle_qty - 1):
        vector = sd.get_vector(start_point=sp, angle=angle + side * (360 / angle_qty), length=side_length, width=width)
        vector.draw()
        sp = vector.end_point

    sd.line(sp, start, width=width)


def triangle(sp, angle, side_length):
    """
        Фунцкция чертит треугольник посредством вызова универсальной функции polygon
    """
    polygon(sp=sp, angle=angle, side_length=side_length, angle_qty=3)


def square(sp, angle, side_length):
    """
        Фунцкция чертит квадрат. Вызывает функцию polygon и передает ей количество углов равное 4
    """
    polygon(sp=sp, angle=angle, side_length=side_length, angle_qty=4)


def pentagon(sp, angle, side_length):
    """
        Фунцкция чертит пятиуголник. Вызывает функцию polygon и передает ей количество углов равное 5
    """
    polygon(sp=sp, angle=angle, side_length=side_length, angle_qty=5)


def hexagon(sp, angle, side_length):
    """
        Фунцкция чертит шестиугольник. Вызывает функцию polygon и передает ей количество углов равное 6
    """
    polygon(sp=sp, angle=angle, side_length=side_length, angle_qty=6)


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

sd.pause()

# Ура. Докстринги.
# зачет!
