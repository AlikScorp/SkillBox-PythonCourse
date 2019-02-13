# -*- coding: utf-8 -*-

import simple_draw as sd

# 1) Написать функцию draw_branches, которая должна рисовать две ветви дерева из начальной точки
# Функция должна принимать параметры:
# - точка начала рисования,
# - угол рисования,
# - длина ветвей,
# Отклонение ветвей от угла рисования принять 30 градусов,

# 2) Сделать draw_branches рекурсивной
# - добавить проверку на длину ветвей, если длина меньше 10 - не рисовать
# - вызывать саму себя 2 раза из точек-концов нарисованных ветвей,
#   с углом рисования равным углу ветви,
#   длиной ветви меньшей чем длина ветви с коэффициентом 0.75

# 3) первоначальный вызов:
# root_point = get_point(300, 30)
# draw_bunches(start_point=root_point, angle=90, length=100)

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# Возможный результат решения см lesson_004/results/exercise_04_fractal_01.jpg

# можно поиграть -шрифтами- цветами и углами отклонения


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


# 4) Усложненное задание (делать по желанию)
# - сделать рандомное отклонение угла ветвей в пределах 40% от 30-ти градусов
# - сделать рандомное отклонение длины ветвей в пределах 20% от коэффициента 0.75
# Возможный результат решения см lesson_004/results/exercise_04_fractal_02.jpg

# Пригодятся функции
# sd.random_number()

def draw_branches_1(start_point, angle, length):
    deviation = 30
    if length < 5:
        return

    new_angle = angle+(deviation+deviation*(sd.random_number(-40, 40)/100))
    new_length = length*(0.75+0.75*(sd.random_number(-20, 20)/100))
    branch1 = sd.get_vector(start_point=start_point, angle=new_angle, length=new_length, width=2)
    branch1.draw()

    draw_branches_1(branch1.end_point, angle=new_angle, length=new_length)

    new_angle = angle-(deviation+deviation*(sd.random_number(-40, 40)/100))
    new_length = length*(0.75+0.75*(sd.random_number(-20, 20)/100))
    branch2 = sd.get_vector(start_point=start_point, angle=new_angle, length=new_length, width=2)
    branch2.draw()

    draw_branches_1(branch2.end_point, angle=new_angle, length=new_length)


root_point = sd.get_point(300, 30)
sd.line(sd.get_point(300, 0), root_point, width=2)
draw_branches_1(start_point=root_point, angle=90, length=100)
# draw_branches(start_point=root_point, angle=90, length=100)


sd.pause()

# зачет!
