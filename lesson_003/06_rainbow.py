# -*- coding: utf-8 -*-

# (цикл for)

import simple_draw as sd

rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)

# Нарисовать радугу: 7 линий толщиной 4 с шагом 5 из точки (50, 50) в точку (550, 550)

i = 0
step = 5
width = 4
for color in rainbow_colors:
    sd.line(sd.get_point(50 + step * i, 50), sd.get_point(550 + step * i, 550), color, width)
    i += 1

# Усложненное задание, делать по желанию.
# Нарисовать радугу дугами от окружности (cсм sd.circle) за нижним краем экрана,
# поэкспериментировать с параметрами, что бы было красиво


i = 0
width = 30
for color in rainbow_colors:
    sd.circle(sd.get_point(400, -100), 500+i, color, width)
    i += width

sd.pause()

# зачет!
