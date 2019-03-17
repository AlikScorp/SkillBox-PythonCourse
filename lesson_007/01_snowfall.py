# -*- coding: utf-8 -*-

import simple_draw as sd

N = 50
snowflakes = []


# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку


class Snowflake:
    area = (sd.get_point(0, sd.resolution[1]), sd.get_point(sd.resolution[0], sd.resolution[1] * 2))

    def __init__(self):
        self.x = sd.random_number(self.area[0].x, self.area[1].x)
        self.y = sd.random_number(self.area[0].y, self.area[1].y)
        self.center = sd.get_point(x=self.x, y=self.y)
        self.size = sd.random_number(10, 20)
        self.factor_a, self.factor_b, self.factor_c = (sd.random_number(1, 10) / 10,
                                                       sd.random_number(1, 10) / 10, sd.random_number(1, 179))
        self.flake = [self.center, self.size, self.factor_a, self.factor_b, self.factor_c]

    def clear_previous_picture(self):
        self.draw(color=sd.background_color)

    def move(self):
        self.flake[0].x += sd.random_number(-1, 1) * 5
        self.flake[0].y -= sd.random_number(5, 10)

    def draw(self, color=sd.COLOR_WHITE):
        sd.snowflake(center=self.flake[0], length=self.flake[1], color=color,
                     factor_a=self.flake[2], factor_b=self.flake[3], factor_c=self.flake[4])

    def can_fall(self):
        if self.flake[0].y > 0:
            return True
        else:
            return False


# flake = Snowflake()
#
# while True:
#     flake.clear_previous_picture()
#     flake.move()
#     flake.draw()
#     if not flake.can_fall():
#         break
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break


# шаг 2: создать снегопад - список объектов Снежинка в отдельном списке, обработку примерно так:

def get_flakes(count=50):
    for _ in range(count):
        snowflakes.append(Snowflake())
    return snowflakes


def get_fallen_flakes():
    fallen = []
    for flake in snowflakes:
        if not flake.can_fall():
            fallen.append(flake)
    return fallen


def remove_fallen(fallen):
    global snowflakes
    snowflakes = [flake for flake in snowflakes if flake not in fallen]


get_flakes(count=N)  # создать список снежинок
sd.caption = 'Snowfall'

while True:
    sd.start_drawing()

    for snowflake in snowflakes:
        snowflake.clear_previous_picture()
        snowflake.move()
        snowflake.draw()

    fallen_flakes = get_fallen_flakes()  # подчитать сколько снежинок уже упало

    if fallen_flakes:
        remove_fallen(fallen_flakes)
        get_flakes(count=len(fallen_flakes))  # добавить еще сверху

    sd.finish_drawing()
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()
