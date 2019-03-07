# -*- coding: utf-8 -*-

import simple_draw as sd

snowflakes = []
flake_size = (10, 20)


def add_snowflake(size=flake_size, area=(sd.get_point(0, sd.resolution[1]),
                                         sd.get_point(sd.resolution[0], sd.resolution[1]*2))):
    """
        Функция генерирует параметры для рисоваия снежинки
    :param size: Размер снежинок вида (<минимум>, <максимум>)
    :param area: Область в виде прямоугольника для создания снежинок - (нижний-левый угол, верхний-правый угол)
    :return: Возвращает параметры снежинки в виде списка (центр снежинки, размер, фактор_а, фактор_а, фактор_с)
    """
    x = sd.random_number(area[0].x, area[1].x)
    y = sd.random_number(area[0].y, area[1].y)

    # В следующей строчке можно факторы прописать константными если не нравятся рандомные снежинки :-)
    factor_a, factor_b, factor_c = sd.random_number(1, 10)/10, sd.random_number(1, 10)/10, sd.random_number(1, 179)

    center = sd.get_point(x, y)
    size = sd.random_number(size[0], size[1])
    return center, size, factor_a, factor_b, factor_c


def clear_flake(number):
    """
        Функция (алиас) "стирает" (фактически - перерисовывает цветом sd.background_color) ненужную снежинку во время падения
    :param number: Номер индекса снижинки в списке snowflakes, которую надо "стереть"
    :return: None
    """
    draw_flake(number, color=sd.background_color)


def draw_flake(number, color=sd.COLOR_WHITE):
    """
        Функция рисует снежинку во время падения
    :param number: номер снижинки, которую надо "нарисовать"
    :param color: Указывает каким цветом "нарисовать" снежинку.
    :return: None
    """
    sd.snowflake(snowflakes[number][0], snowflakes[number][1], color=color,
                 factor_a=snowflakes[number][2], factor_b=snowflakes[number][3], factor_c=snowflakes[number][4])


def create_snowflakes(quantity):
    """
        Функция создает снежинки
    :param quantity: Количество создаваемых снежинок
    :return: None
    """
    for _ in range(quantity):
        add_flake()


def move_flake(number):
    """
        Функция двигает снежинку
    :param number: Номер снежинки
    :return: None
    """
    snowflakes[number][0].x += sd.random_number(-1, 1) * 5
    snowflakes[number][0].y -= sd.random_number(5, 10)


def move_flakes():
    """
        Функция сдвигает все снежинки
    :return: None
    """
    for i in range(len(snowflakes)):
        move_flake(i)


def draw_flakes(color=sd.COLOR_WHITE):
    """
        Функция рисует все созданные снежинки
    :param color: Определяет цвет которым будет нарисована снежинка
    :return: None
    """
    sd.start_drawing()
    for i in range(len(snowflakes)):
        draw_flake(i, color=color)
    sd.finish_drawing()


def check_flake(number):
    """
        Проверяем достигла ли снежика "земли" (вышла ли за край экрана)
    :param number: Номер снежинки
    :return: True если достигла, False если нет
    """
    if snowflakes[number][0].y < 0:
        return True
    else:
        return False


def check_fallen():
    """
        Функция ищет упавшие снежинки
    :return: Список упавших снежинок
    """
    fallen_flakes = []

    for i in range(len(snowflakes)):
        if check_flake(i):
            fallen_flakes.append(snowflakes[i])

    return fallen_flakes


def remove_fallen(fallen):
    """
        Удаляем упавшие снежинки
    :param fallen: Список упавших снединок
    :return: None
    """
    # TODO Здесь лучше отсортировать fallen по убыванию.
    #  Если удалять сначала снежинку с меньшим номером,
    #  то их номера уменьшатся и при удалении снежинки с большим номером
    #  вы можете удалить не ту.
    #  Есть еще один вариант:
    #  global snowflakes
    #  snowflakes = [flake for i, flake in enumerate(snowflakes) if i not in fallen]
    if fallen:
        # TODO Здесь лучше сделать
        #  for i in fallen
        #  remove_flake(i)
        for i in range(len(fallen)):
            remove_flake(fallen[i])


def remove_flake(flake):
    """
        Удаляем снежинку
    :param flake: Удаляемая снежика
    :return: None
    """
    snowflakes.remove(flake)


def add_flake():
    """
        Создаем одну снежинку
    :return: None
    """
    snowflakes.append(add_snowflake())


# TODO Не нужно дублировать содержимое основного модуля здесь.
def snowfall(n=50):
    """
    Функция рисует снегопад из n снежинок
    :param n: Количество снежинок в снегопаде
    :return: None
    """

    create_snowflakes(quantity=n)
    while True:
        draw_flakes(color=sd.background_color)
        move_flakes()
        draw_flakes()
        fallen = check_fallen()
        if fallen:
            remove_fallen(fallen=fallen)
            create_snowflakes(quantity=len(fallen))

        sd.sleep(0.1)
        if sd.user_want_exit():
            break


if __name__ == '__main__':
    snowfall(50)
    sd.pause()
