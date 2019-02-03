# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw as sd

# Нарисовать стену из кирпичей. Размер кирпича - 100х50
# Использовать вложенные циклы for

# sd.resolution = (1200, 600)
# sd.background_color = sd.random_color()
# color = sd.random_color()

color = sd.COLOR_DARK_CYAN
max_x, max_y = sd.resolution[0], sd.resolution[1]
size_x, size_y = 100, 50

for y in range(0, max_y, size_y):
    for x in range(0, max_x, size_x):
        delta = size_x*((y / size_y) % 2)/2
        sd.line(sd.get_point(x - delta, y), sd.get_point(x - delta + size_x, y), color)
        sd.line(sd.get_point(x - delta + size_x, y), sd.get_point(x - delta + size_x, y + size_y), color)
        sd.line(sd.get_point(x - delta + size_x, y + size_y), sd.get_point(x - delta, y + size_y), color)
        sd.line(sd.get_point(x - delta, y + size_y), sd.get_point(x - delta, y), color)

sd.pause()
