# -*- coding: utf-8 -*-
# TODO Импортировать все содержимое модуля плохая практика.
#  Нужно либо импортировать модуль и ссылаться на него.
#  from lesson_005 import my_burger
#  my_burger.add_bun()
#  Либо перечислять при импорте то, что будете использовать.
#  from lesson_005.my_burger import (add_bun, add_cheese, ...)
from lesson_005.my_burger import *
# Создать модуль my_burger. В нем определить функции добавления инградиентов:
#  - булочки
#  - котлеты
#  - огурчика
#  - помидорчика
#  - майонеза
#  - сыра
# В каждой функции выводить на консоль что-то вроде "А теперь добавим ..."

# В этом модуле создать рецепт двойного чизбургера (https://goo.gl/zA3goZ)
# с помощью фукций из my_burger и вывести на консоль.

# Создать рецепт своего бургера, по вашему вкусу.
# Если не хватает инградиентов - создать соответствующие функции в модуле my_burger

print('Давайте приготовим "Двойной Чизбургер":')
add_bun()
add_beef_patty()
add_cheese()
add_beef_patty(1)
add_cheese(1)
add_pickles()
add_onion()
add_ketchup()
add_mustard()
add_bun(1)
is_ready()
print('Но не забывайте - в нём 442Ккал!!! :-)')

print('\nИ мой любимый рецепт - "Чикен Гурмэ Экзотик":')
add_bun()
add_mustard()
add_chicken()
add_tomato()
add_salad()
add_guacamole()
add_bun(1)
is_ready()
print('Но не забывайте -  в нём 621Ккал!!! :-)')

