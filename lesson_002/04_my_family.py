#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Создайте списки:

# моя семья (минимум 3 элемента, есть еще дедушки и бабушки, если что)

my_family = ['Отец', 'Мать', 'Старший сын', 'Средний сын', 'Младший сын']
name = 0
height = 1

# список списков приблизителного роста членов вашей семьи
my_family_height = [
    # ['имя', рост],
    ['Альберт', 180], ['Любовь', 165], ['Артемий', 130], ['Арсений', 115], ['Никита', 110]
]

# Выведите на консоль рост отца в формате
#   Рост отца - ХХ см

father_height = my_family_height[my_family.index('Отец')][height]

print("Рост отца -", father_height, "см.")
# Выведите на консоль общий рост вашей семьи как сумму ростов всех членов
#   Общий рост моей семьи - ХХ см

total_height = my_family_height[0][height] + my_family_height[1][height] + my_family_height[2][height] + \
               my_family_height[3][height] + my_family_height[4][height]
print("Общий рост моей семьи -", total_height, "см.")
