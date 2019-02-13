# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (800, 600)
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
    x = sd.random_number(0, sd.resolution[0])
    y = sd.random_number(sd.resolution[1], sd.resolution[1]*2)

# В следующей строчке можно факторы прописать константными если не нравятся рандомные снежинки :-)
    factor_a, factor_b, factor_c = sd.random_number(1, 10)/10, sd.random_number(1, 10)/10, sd.random_number(1, 179)

    center = sd.get_point(x, y)
    size = sd.random_number(10, 30)
    return center, size, factor_a, factor_b, factor_c


for i in range(N):
    snowflakes.append(add_snowflake())

while True:
    sd.start_drawing()
    for i in range(N):
        if snowflakes[i][0].y < 0:
            snowflakes.pop(i)
            snowflakes.append(add_snowflake())
            continue
        else:
            sd.snowflake(snowflakes[i][0], snowflakes[i][1], color=sd.background_color,
                         factor_a=snowflakes[i][2], factor_b=snowflakes[i][3], factor_c=snowflakes[i][4])

        snowflakes[i][0].x += sd.random_number(-1, 1)*5
        snowflakes[i][0].y -= sd.random_number(5, 10)
        sd.snowflake(snowflakes[i][0], snowflakes[i][1], color=sd.COLOR_WHITE,
                     factor_a=snowflakes[i][2], factor_b=snowflakes[i][3], factor_c=snowflakes[i][4])
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
