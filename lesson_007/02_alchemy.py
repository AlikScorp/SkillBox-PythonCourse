# -*- coding: utf-8 -*-

# Создать прототип игры Алхимия: при соединении двух элементов получается новый.
# Реализовать следующие элементы: Вода, Воздух, Огонь, Земля, Шторм, Пар, Грязь, Молния, Пыль, Лава.
# Каждый элемент организовать как отдельный класс.
# Таблица преобразований:
#   Вода + Воздух = Шторм
#   Вода + Огонь = Пар
#   Вода + Земля = Грязь
#   Воздух + Огонь = Молния
#   Воздух + Земля = Пыль
#   Огонь + Земля = Лава

# Сложение элементов реализовывать через __add__
# Если результат не определен - то возвращать None
# Вывод элемента на консоль реализовывать через __str__
#
# Примеры преобразований:
#   print(Water(), '+', Air(), '=', Water() + Air())
#   print(Fire(), '+', Air(), '=', Fire() + Air())
from termcolor import colored


class Water:
    def __str__(self):
        return colored("Вода", 'blue')

    def __add__(self, other):
        if isinstance(other, Air):
            return Storm()
        elif isinstance(other, Fire):
            return Steam()
        elif isinstance(other, Earth):
            return Dirt()
        elif isinstance(other, Lava):
            return Obsidian()
        elif isinstance(other, Sand):
            return Clay()
        else:
            return None


class Air:
    def __str__(self):
        return colored("Воздух", 'cyan')

    def __add__(self, other):
        if isinstance(other, Water):
            return Storm()
        elif isinstance(other, Fire):
            return Lightning()
        elif isinstance(other, Earth):
            return Dust()
        elif isinstance(other, Dust):
            return DustStorm()
        else:
            return None


class Fire:
    def __str__(self):
        return colored("Огонь", 'red')

    def __add__(self, other):
        if isinstance(other, Water):
            return Steam()
        elif isinstance(other, Air):
            return Lightning()
        elif isinstance(other, Earth):
            return Lava()
        else:
            return None


class Earth:
    def __str__(self):
        return colored("Земля", color='green')

    def __add__(self, other):
        if isinstance(other, Water):
            return Dirt()
        elif isinstance(other, Air):
            return Dust()
        elif isinstance(other, Fire):
            return Lava()
        else:
            return None


class Sand:
    def __str__(self):
        return colored("Песок", color='yellow')

    def __add__(self, other):
        if isinstance(other, Water):
            return Clay()
        elif isinstance(other, Air):
            return Sandstorm()
        elif isinstance(other, Fire):
            return Glass()
        elif isinstance(other, Lightning):
            return Mica()
        else:
            return None


class Storm:
    def __str__(self):
        return colored("Шторм", color='cyan', attrs=['bold', 'underline'])

    def __add__(self, other):
        return None


class Sandstorm(Storm):
    def __str__(self):
        return colored("Самум", color='yellow', attrs=['bold', 'underline'])


class DustStorm(Storm):
    def __str__(self):
        return colored("Пыльная буря", color='yellow', attrs=['bold', 'underline'])


class Steam:
    def __str__(self):
        return colored("Пар", color="blue", attrs=['bold', 'underline'])

    def __add__(self, other):
        return None


class Dirt:
    def __str__(self):
        return colored("Грязь", color='green', attrs=['bold', 'underline'])

    def __add__(self, other):
        if isinstance(other, Fire):
            return Obsidian()
        return None


class Clay(Dirt):
    def __str__(self):
        return colored("Глина", color='yellow', attrs=['bold', 'concealed'])

    def __add__(self, other):
        if isinstance(other, Fire):
            return Ceramics()
        return None


class Ceramics:
    def __str__(self):
        return colored("Керамика", color='red', attrs=['bold'])

    def __add__(self, other):
        return None


class Lightning:
    def __str__(self):
        return colored("Молния", color='blue', attrs=['bold', 'concealed'])

    def __add__(self, other):
        if isinstance(other, Sand):
            return Mica()
        return None


class Dust:
    def __str__(self):
        return colored("Пыль", color='yellow', attrs=['bold', 'underline'])

    def __add__(self, other):
        if isinstance(other, Air):
            return DustStorm()
        return None


class Lava:
    def __str__(self):
        return colored("Лава", color='red', attrs=['bold', 'underline'])

    def __add__(self, other):
        return None


class Glass:
    def __str__(self):
        return colored("Стекло", color='white', attrs=['bold', 'underline'])

    def __add__(self, other):
        return None


class Mica(Glass):
    def __str__(self):
        return colored("Слюда", color='white', attrs=['bold', 'underline', 'concealed'])


class Obsidian(Glass):
    def __str__(self):
        return colored("Обсидиан", color='blue', attrs=['bold', 'dark', 'underline'])


print("============= Смешение стихий с водяной стихией =================")
print(Water(), '+', Air(), '=', Water() + Air())
print(Water(), '+', Fire(), '=', Water() + Fire())
print(Water(), '+', Earth(), '=', Water() + Earth())
print("============= Смешение стихий с воздушной стихией =================")
print(Air(), '+', Fire(), '=', Air() + Fire())
print(Air(), '+', Earth(), '=', Air() + Earth())
print(Air(), '+', Water(), '=', Air() + Water())
print(Air(), '+', Dust(), '=', Air() + Dust())
print("============= Смешение стихий с земляной стихией =================")
print(Earth(), '+', Fire(), '=', Earth() + Fire())
print(Earth(), '+', Air(), '=', Earth() + Air())
print(Earth(), '+', Water(), '=', Earth() + Water())
print("============= Смешение стихий с песком =================")
print(Sand(), '+', Fire(), '=', Sand() + Fire())
print(Sand(), '+', Water(), '=', Sand() + Water())
print(Sand(), '+', Air(), '=', Sand() + Air())
print(Sand(), '+', Lightning(), '=', Sand() + Lightning())

# Усложненное задание (делать по желанию)
# Добавить еще элемент в игру.
# Придумать что будет при сложении существующих элементов с новым.

print("============= Смешения стихий и их производных =================")
print(Water(), '+', Lava(), '=', Water() + Lava())
print(Water(), '+', Earth(), '+', Fire(), '=', Water() + Earth() + Fire())
print(Water(), '+', Earth(), '+', Fire(), '=', Water(), '+', Lava(), '=', Water() + Lava())
print(Clay(), '+', Fire(), '=', Clay() + Fire())
print(Water(), '+', Sand(), '+', Fire(), '=', Clay(), '+', Fire(), '=', Water() + Sand() + Fire())
print(Earth(), '+', Air(), '+', Air(), '=', Dust(), '+', Air(), '=', Earth() + Air() + Air())

# зачет!
