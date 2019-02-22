# -*- coding: utf-8 -*-

import simple_draw as sd


def draw_branches(start_point, angle, length):
    deviation = 30
    if length < 10:
        return
    branch1 = sd.get_vector(start_point=start_point, angle=angle+deviation, length=length, width=2)
    branch1.draw()
    draw_branches(branch1.end_point, angle=angle+deviation, length=length*0.75)
    branch2 = sd.get_vector(start_point=start_point, angle=angle-deviation, length=length, width=2)
    branch2.draw()
    draw_branches(branch2.end_point, angle=angle-deviation, length=length*0.75)


def draw_branches_1(start_point, angle, length):
    deviation = 30
    if length < 5:
        return
    elif 5 <= length <= 20:
        color = sd.COLOR_GREEN
        width = 1
    elif 20 < length < 40:
        color = sd.COLOR_DARK_GREEN
        width = 2
    else:
        color = (134, 127, 0)
        width = 3

    new_angle = angle+(deviation+deviation*(sd.random_number(-40, 40)/100))
    new_length = length*(0.75+0.75*(sd.random_number(-20, 20)/100))
    branch1 = sd.get_vector(start_point=start_point, angle=new_angle, length=new_length, width=width)
    branch1.draw(color=color)

    draw_branches_1(branch1.end_point, angle=new_angle, length=new_length)

    new_angle = angle-(deviation+deviation*(sd.random_number(-40, 40)/100))
    new_length = length*(0.75+0.75*(sd.random_number(-20, 20)/100))
    branch2 = sd.get_vector(start_point=start_point, angle=new_angle, length=new_length, width=width)
    branch2.draw(color=color)

    draw_branches_1(branch2.end_point, angle=new_angle, length=new_length)


if __name__ == '__main__':
    root_point = sd.get_point(300, 30)
    sd.line(sd.get_point(300, 0), root_point, width=3, color=(134, 127, 0))
    draw_branches_1(start_point=root_point, angle=90, length=100)
    # draw_branches(start_point=root_point, angle=90, length=100)
    sd.pause()
