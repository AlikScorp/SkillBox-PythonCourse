# -*- coding: utf-8 -*-

import simple_draw as sd


def draw_wall(start_point=sd.get_point(0, 0), area=(sd.resolution[0], sd.resolution[1])):
    """
        Функция рисует стену размером width x height из стартовой точки start_point
    :return:
    """
    color = sd.COLOR_DARK_CYAN
    max_x, max_y = area[0], area[1]
    size_x, size_y = 20, 10

    sd.rectangle(start_point, sd.get_point(start_point.x+max_x, start_point.y+max_y), color=sd.COLOR_DARK_CYAN, width=2)

    for y in range(start_point.y, start_point.y+max_y, size_y):
        for x in range(start_point.x, start_point.x+max_x, size_x):
            delta = size_x * ((y / size_y) % 2) / 2
            if delta != 0 and x == start_point.x+max_x-size_x:
                break
            sd.line(sd.get_point(x + delta, y), sd.get_point(x + delta + size_x, y), color)
            sd.line(sd.get_point(x + delta + size_x, y), sd.get_point(x + delta + size_x, y + size_y), color)
            sd.line(sd.get_point(x + delta + size_x, y + size_y), sd.get_point(x + delta, y + size_y), color)
            sd.line(sd.get_point(x + delta, y + size_y), sd.get_point(x + delta, y), color)


if __name__ == '__main__':
    sd.start_drawing()
    draw_wall(sd.get_point(100, 200), area=(300, 300))
    sd.finish_drawing()
    sd.pause()

