# -*- coding: utf-8 -*-

import simple_draw as sd
from lesson_006.snowfall import create_snowflakes, draw_flakes, move_flakes, check_fallen, remove_fallen

quantity = 50

# На основе кода из lesson_004/05_snowfall.py
# сделать модуль snowfall.py в котором реализовать следующие функции
#  создать_снежинки(N) - создает N снежинок
#  нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color
#  сдвинуть_снежинки() - сдвигает снежинки на один шаг
#  номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана
#  удалить_снежинки(номера) - удаляет снежинки с номерами из списка
#
# В текущем модуле реализовать главный цикл падения снежинок,
# обращаясь ТОЛЬКО к функциям модуля snowfall

# создать_снежинки(N)
create_snowflakes(quantity=quantity)
sd.caption = 'Snowfall'

while True:
    #  нарисовать_снежинки_цветом(color=sd.background_color)
    #  сдвинуть_снежинки()
    #  нарисовать_снежинки_цветом(color)
    #  если есть номера_достигших_низа_экрана() то
    #       удалить_снежинки(номера)
    #       создать_снежинки(count)
    draw_flakes(color=sd.background_color)
    move_flakes()
    draw_flakes()
    fallen = check_fallen()
    if fallen:
        remove_fallen(fallen)
        create_snowflakes(len(fallen))

    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()

# зачет!
