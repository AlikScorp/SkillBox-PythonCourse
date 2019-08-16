# -*- coding: utf-8 -*-

import simple_draw as sd

# На основе вашего кода из решения lesson_004/01_shapes.py сделать функцию-фабрику,
# которая возвращает функции рисования треугольника, четырехугольника, пятиугольника и т.д.
#
# Функция рисования должна принимать параметры
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Функция-фабрика должна принимать параметр n - количество сторон.


def get_polygon(n):
    """
        Функция-фабрика - создает функцию рисования многоугольников, в качестве пораметра принемает количество углов
    :param n: Количество углов у многоугольника
    :return: Функцию рисования многоугольника с задыным числом углов
    """

    def polygon(sp, angle, side_length, angle_qty=n):
        """
            Фунцкция чертит правильный многоугольник.

            :param sp: Начальная точка
            :param angle Угол под которым отображается фигура
            :param side_length Длина стороны
            :param angle_qty Количество углов фигуры
        """
        start, width = sp, 3
        for side in range(angle_qty - 1):
            vector = sd.get_vector(start_point=sp, angle=angle + side * (360 / angle_qty), length=side_length,
                                   width=width)
            vector.draw()
            sp = vector.end_point

        sd.line(sp, start, width=width)

    return polygon


angle = 13
length = 100

draw_triangle = get_polygon(n=3)
draw_triangle(sp=sd.get_point(150, 150), angle=angle, side_length=length)

draw_square = get_polygon(n=4)
draw_square(sp=sd.get_point(400, 150), angle=angle, side_length=length)

draw_pentagon = get_polygon(n=5)
draw_pentagon(sp=sd.get_point(150, 350), angle=angle, side_length=length)

draw_hexagon = get_polygon(n=6)
draw_hexagon(sp=sd.get_point(400, 350), angle=angle, side_length=length)


sd.pause()

# зачет!
