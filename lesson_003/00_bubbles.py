# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (1200, 600)

# Нарисовать пузырек - три вложенных окружностей с шагом 5 пикселей
x = 600
y = 300
point = sd.get_point(x, y)

for i in [15, 20, 25]:
    sd.circle(point, i)


# Написать функцию рисования пузырька, принммающую 2 (или более) параметра: точка рисовании и шаг
def draw_bubble(center, radius, step, color=sd.COLOR_YELLOW):
    # Если делаете docstring, описываете значения параметров.
    """
        The function is drawing the bubble with following parameters
    :param center:
    :param radius:
    :param step:
    :param color:
    :return:
    """
    for i in [radius, radius + step, radius + step * 2]:
        sd.circle(center, radius + i, color)


# draw_bubble(point, 15, 15)
# Нарисовать 10 пузырьков в ряд
x, y = 150, 200

for i in range(0, 10):
    point = sd.get_point(x, y)
    draw_bubble(point, 15, 5)
    x = x + 100

# Нарисовать три ряда по 10 пузырьков

x, y = 150, 200

for i in range(0, 3):
    x = 150
    for j in range(0, 10):
        point = sd.get_point(x, y)
        draw_bubble(point, 15, 5)
        x += 100
    y += 100

# Нарисовать 100 пузырьков в произвольных местах экрана случайными цветами
i = 0
radius = 15
step = 5
while i < 100:
    draw_bubble(sd.random_point(), radius, step, sd.random_color())
    i += 1

sd.pause()

# зачет!
