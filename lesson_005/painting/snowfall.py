# -*- coding: utf-8 -*-

import simple_draw as sd


def add_snowflake(min_size=10, max_size=30, area=(sd.get_point(0, sd.resolution[1]),
                                                  sd.get_point(sd.resolution[0], sd.resolution[1]*2))):
    """
        Функция генерирует параметры для рисоваия снежинки
    :return: Возвращает параметры снежинки в виде списка (центр снежинки, размер, фактор_а, фактор_а, фактор_с)
    """
    x = sd.random_number(area[0].x, area[1].x)
    y = sd.random_number(area[0].y, area[1].y*2)

    # В следующей строчке можно факторы прописать константными если не нравятся рандомные снежинки :-)
    factor_a, factor_b, factor_c = sd.random_number(1, 10)/10, sd.random_number(1, 10)/10, sd.random_number(1, 179)

    center = sd.get_point(x, y)
    size = sd.random_number(min_size, max_size)
    return center, size, factor_a, factor_b, factor_c


def clear_flake(snowflakes, number):
    """
        Функция стирает ненужную снежинку во время падения
    :param snowflakes: список снежинок
    :param number: номер снижинки, которую надо "стереть"
    :return: None
    """
    sd.snowflake(snowflakes[number][0], snowflakes[number][1], color=sd.background_color,
                 factor_a=snowflakes[number][2], factor_b=snowflakes[number][3], factor_c=snowflakes[number][4])


def draw_flake(snowflakes, number):
    """
        Функция рисует снежинку во время падения
    :param snowflakes: список снежинок
    :param number: номер снижинки, которую надо "нарисовать"
    :return: None
    """
    sd.snowflake(snowflakes[number][0], snowflakes[number][1], color=sd.COLOR_WHITE,
                 factor_a=snowflakes[number][2], factor_b=snowflakes[number][3], factor_c=snowflakes[number][4])


def snowfall(n=50):
    """
    Функция рисует снегопад из n снежинок
    :param n: Количество снежинок в снегопаде
    :return: None
    """
    snowflakes = []

    for i in range(n):
        snowflakes.append(add_snowflake())

    while True:
        sd.start_drawing()
        for i in range(n):
            if snowflakes[i][0].y < 0:
                snowflakes.pop(i)
                snowflakes.append(add_snowflake())
                continue
            else:
                clear_flake(snowflakes, number=i)

            snowflakes[i][0].x += sd.random_number(-1, 1)*5
            snowflakes[i][0].y -= sd.random_number(5, 10)
            draw_flake(snowflakes, i)

        sd.finish_drawing()
        sd.sleep(0.1)
        if sd.user_want_exit():
            break


if __name__ == '__main__':
    snowfall(50)
    sd.pause()
