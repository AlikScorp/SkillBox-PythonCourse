# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (600, 600)
# На основе кода из практической части реализовать снегопад:
# - создать списки данных для отрисовки N снежинок
# - нарисовать падение этих N снежинок
# - создать список рандомных длинн лучей снежинок (от 10 до 100) и пусть все снежинки будут разные

N = 50
snowflakes = []

# Пригодятся функции
# sd.get_point()
# sd.snowflake()
# sd.sleep()
# sd.random_number()
# sd.user_want_exit()


def add_snowflake():
    global snowflakes

    x = sd.random_number(0, sd.resolution[0])
    y = sd.random_number(sd.resolution[1], sd.resolution[1]*2)
    center = sd.get_point(x, y)
    size = sd.random_number(10, 30)
    snowflakes.append([center, size])
    return center, size


for i in range(N):
    sd.snowflake(*add_snowflake())

while True:
    sd.start_drawing()
    for i in range(N):
        if snowflakes[i][0].y < 0:
            snowflakes.pop(i)
            sd.snowflake(*add_snowflake())
            continue
        else:
            sd.snowflake(snowflakes[i][0], snowflakes[i][1], color=sd.background_color)

        snowflakes[i][0].x += sd.random_number(-1, 1)*5
        snowflakes[i][0].y -= sd.random_number(5, 10)
        sd.snowflake(snowflakes[i][0], snowflakes[i][1])
    sd.finish_drawing()
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()

# подсказка! для ускорения отрисовки можно
#  - убрать clear_screen()
#  - в начале рисования всех снежинок вызвать sd.start_drawing()
#  - на старом месте снежинки отрисовать её же, но цветом sd.background_color
#  - сдвинуть снежинку
#  - отрисовать её цветом sd.COLOR_WHITE на новом месте
#  - после отрисовки всех снежинок, перед sleep(), вызвать sd.finish_drawing()


# 4) Усложненное задание (делать по желанию)
# - сделать рандомные отклонения вправо/влево при каждом шаге
# - сделать сугоб внизу экрана - если снежинка долетает до низа, оставлять её там,
#   и добавлять новую снежинку
# Результат решения см https://youtu.be/XBx0JtxHiLg
