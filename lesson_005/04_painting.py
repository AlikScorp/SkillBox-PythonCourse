# -*- coding: utf-8 -*-
# TODO Импортировать все содержимое модуля плохая практика.
from lesson_005.painting.picture import *
# Создать пакет, в котором собрать функции отрисовки из предыдущего урока
#  - радуги
#  - стены
#  - дерева
#  - смайлика
#  - снежинок
# Каждую функцию разместить в своем модуле. Название пакета и модулей - по смыслу.
# Создать модуль с функцией отрисовки кирпичного дома с широким окном и крышей.

# С помощью созданного пакета нарисовать эпохальное полотно "Утро в деревне".
# На картине должны быть:
#  - кирпичный дом, в окошке - смайлик.
#  - слева от дома - сугроб (предположим что это ранняя весна)
#  - справа от дома - дерево (можно несколько)
#  - справа в небе - радуга, слева - солнце (весна же!)
# пример см. lesson_005/results/04_painting.jpg
# Приправить своей фантазией по вкусу (коты? коровы? люди? трактор? что придумается)


sd.resolution = (1200, 800)
sd.caption = 'Morning in a country'

sd.start_drawing()

draw_house()
draw_tree()

draw_sun(sd.get_point(100, 700), angle=30)
draw_cloud(300, 730)
draw_cloud(100, 670)
draw_cloud(500, 650)
draw_cloud(700, 710)

sd.rectangle(sd.get_point(0, 0), sd.get_point(sd.resolution[0], 100), color=(180, 130, 31))

snowdrift(300)
draw_rainbow(sd.get_point(400, -100), 10, 1000)
sd.finish_drawing()

sd.pause()

# Усложненное задание (делать по желанию)
# Анимировать картину.
# Пусть слева идет снегопад, радуга переливается цветами, смайлик моргает, солнце крутит лучами, етс.
# Задержку в анимировании все равно надо ставить, пусть даже 0.01 сек - так библиотека устойчивей работает.
