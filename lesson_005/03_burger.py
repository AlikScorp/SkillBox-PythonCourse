# -*- coding: utf-8 -*-
import lesson_005.my_burger as mb
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
mb.add_bun()
mb.add_beef_patty()
mb.add_cheese()
mb.add_beef_patty(1)
mb.add_cheese(1)
mb.add_pickles()
mb.add_onion()
mb.add_ketchup()
mb.add_mustard()
mb.add_bun(1)
mb.is_ready()
print('Но не забывайте - в нём 442Ккал!!! :-)')
input()
print('\nИ мой любимый рецепт - "Чикен Гурмэ Экзотик":')
mb.add_bun()
mb.add_mustard()
mb.add_chicken()
mb.add_tomato()
mb.add_salad()
mb.add_guacamole()
mb.add_bun(1)
mb.is_ready()
print('Но не забывайте -  в нём 621Ккал!!! :-)')

