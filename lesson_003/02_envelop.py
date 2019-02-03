# -*- coding: utf-8 -*-

# (if/elif/else)

# Заданы размеры envelop_x, envelop_y - размеры конверта и paper_x, paper_y листа бумаги (все размеры
# могут быть в диапазоне от 1 до 1000)
#
# Определить, поместится ли бумага в конверте (стороны листа параллельны сторонам конверта)
#
# Результат проверки вывести на консоль (ДА/НЕТ)
# Использовать только операторы if/elif/else, можно вложенные


envelop_x, envelop_y = 10, 7
# paper_x, paper_y = 8, 9
# проверить для
# paper_x, paper_y = 9, 8
paper_x, paper_y = 6, 8
# paper_x, paper_y = 8, 6
# paper_x, paper_y = 3, 4
# paper_x, paper_y = 11, 9
# paper_x, paper_y = 9, 11
# (просто раскоментировать нужную строку и проверить свой код)

# TODO здесь ваш код

if paper_x <= envelop_x:
    if paper_y <= envelop_y:
        print('Да')
    else:
        print('Переворачиваем ...')
        if paper_y <= envelop_x:
            if paper_x <= envelop_y:
                print('Да (если перевернем))')
            else:
                print('Нет (даже если перевернуть)')
        else:
            print('Нет (даже если перевернуть)')
else:
    print('Переворачиваем...')
    if paper_y <= envelop_x:
        if paper_x <= envelop_y:
            print('Да (если перевернем)')
        else:
            print('Нет (даже если перевернуть)')
    else:
        print('Нет')

# Усложненное задание, решать по желанию.
# Заданы размеры hole_x, hole_y прямоугольного отверстия и размеры brick_х, brick_у, brick_z кирпича (все размеры
# могут быть в диапазоне от 1 до 1000)
#
# Определить, пройдет ли кирпич через отверстие (грани кирпича параллельны сторонам отверстия)

hole_x, hole_y = 8, 9
# brick_x, brick_y, brick_z = 11, 10, 2
# brick_x, brick_y, brick_z = 11, 2, 10
# brick_x, brick_y, brick_z = 10, 11, 2
# brick_x, brick_y, brick_z = 10, 2, 11
# brick_x, brick_y, brick_z = 2, 10, 11
# brick_x, brick_y, brick_z = 2, 11, 10
# brick_x, brick_y, brick_z = 3, 5, 6
# brick_x, brick_y, brick_z = 3, 6, 5
# brick_x, brick_y, brick_z = 6, 3, 5
# brick_x, brick_y, brick_z = 6, 5, 3
# brick_x, brick_y, brick_z = 5, 6, 3
# brick_x, brick_y, brick_z = 5, 3, 6
# brick_x, brick_y, brick_z = 11, 3, 6
# brick_x, brick_y, brick_z = 11, 6, 3
# brick_x, brick_y, brick_z = 6, 11, 3
# brick_x, brick_y, brick_z = 6, 3, 11
# brick_x, brick_y, brick_z = 3, 6, 11
brick_x, brick_y, brick_z = 3, 11, 6
# (просто раскоментировать нужную строку и проверить свой код)

# TODO здесь ваш код

print('Размер отверстия -', hole_x, 'X', hole_y)
print('Размер кирпича - ', brick_x, 'X', brick_y, 'X', brick_z)
if brick_x <= hole_x:
    if brick_y <= hole_y:
        print('Ура! Поместился по сторонам x и y!')
    elif brick_z <= hole_y:
        print('Ура! Поместился по сторонам x и z!')
    else:
        print('Не помещается')
elif brick_y <= hole_x:
    print('Переворачиваем...')
    if brick_x <= hole_y:
        print('Ура! Поместился по сторонам y и x')
    elif brick_z <= hole_y:
        print('Ура! Поместился по сторонам y и z')
    else:
        print('Не помещается')
elif brick_z <= hole_x:
    print('Переворачиваем...')
    if brick_x <= hole_y:
        print('Поместился по сторонам z и x')
    elif brick_y <= hole_y:
        print('Поместился по сторонам z и y')
    else:
        print('Не помещается!')
else:
    print('Не помещается!')

