# -*- coding: utf-8 -*-

from random import randint
from termcolor import cprint, colored


# Доработать практическую часть урока lesson_007/python_snippets/08_practice.py

# Необходимо создать класс кота. У кота есть аттрибуты - сытость и дом (в котором он живет).
# Кот живет с человеком в доме.
# Для кота дом характеризируется - миской для еды и грязью.
# Изначально в доме нет еды для кота и нет грязи.

# Доработать класс человека, добавив методы
#   подобрать кота - у кота появляется дом.
#   купить коту еды - кошачья еда в доме увеличивается на 50, деньги уменьшаются на 50.
#   убраться в доме - степень грязи в доме уменьшается на 100, сытость у человека уменьшается на 20.
# Увеличить кол-во зарабатываемых человеком денег до 150 (он выучил пайтон и устроился на хорошую работу :)

# Кот может есть, спать и драть обои - необходимо реализовать соответствующие методы.
# Когда кот спит - сытость уменьшается на 10
# Когда кот ест - сытость увеличивается на 20, кошачья еда в доме уменьшается на 10.
# Когда кот дерет обои - сытость уменьшается на 10, степень грязи в доме увеличивается на 5
# Если степень сытости < 0, кот умирает.
# Так же надо реализовать метод "действуй" для кота, в котором он принимает решение
# что будет делать сегодня

# Человеку и коту надо вместе прожить 365 дней.


class Cat:

    def __init__(self, name):
        self.name = name
        self.fullness = 0
        self.house = None
        self.status = 1

    def settle(self, house):
        self.house = house
        self.fullness += 10
        cprint('{} вселился в дом'.format(self.name), color='cyan')

    def tear_the_wall(self):
        if self.house:
            if self.fullness >= 10:
                self.fullness -= 10
            else:
                self.fullness = 0
            cprint('{} хорошенько поточил когти об стены дома'.format(self.name), color='blue', attrs=['bold'])
            self.house.add_dirt(5)
        else:
            cprint('{} бездомный, он не может царапать стены'.format(self.name), color='red', attrs=['bold'])

    def eat(self):
        if self.house:
            if self.house.get_feed() >= 10:
                self.house.remove_feed(10)
                self.house.add_dirt(1)
                self.fullness += 20
                cprint('{} хорошенько поел.'.format(self.name), color='blue', attrs=['bold'])
                return True
            else:
                cprint('{} не нашел еды!'.format(self.name), color='red', attrs=['bold'])
                return False
        else:
            cprint('{} бездомный, он не может найти еды'.format(self.name), color='red', attrs=['bold'])

    def act(self):
        if not self.status:
            cprint('{} мертв!'.format(self.name), color='white', attrs=['bold'])
            return

        dice = randint(1, 4)

        if self.fullness == 0:
            if not self.eat():
                cprint('{} умер!'.format(self.name), color='red', attrs=['bold'])
                self.status = 0
        elif dice == 1:
            self.tear_the_wall()
        elif dice == 2:
            self.eat()
        else:
            self.sleep()

    def get_name(self):
        return self.name

    def sleep(self):
        if self.fullness >= 10:
            self.fullness -= 10
            cprint('{} весь день спал'.format(self.name), color='blue', attrs=['bold'])
        else:
            cprint('Нет еды для {}. Он спит от истощения.'.format(self.name), color='red', attrs=['bold'])

    def __str__(self):
        if not self.status:
            return colored('{}: мертв'.format(self.name, color='blue', attrs=['bold']))

        return colored('{}: {}, сытость - {} '.format(
            self.name, 'Бездомный' if not self.house else 'Имеет дом', self.fullness), color='blue', attrs=['bold'])


class Man:

    def __init__(self, name):
        self.name = name
        self.fullness = 50
        self.house = None
        self.pets_count = 0

    def __str__(self):
        return colored('{}: {}, сытость {}'.format(
            self.name, 'Имеет дом' if self.house else 'Бездомный', self.fullness), color='magenta', attrs=['bold'])

    def eat(self):
        food_quantity = self.house.get_food()
        if food_quantity >= 10:
            cprint('{} хорошенько поел'.format(self.name), color='yellow')
            self.fullness += 10
            self.house.remove_food(10)
            self.house.add_dirt(10)
        elif food_quantity == 0:
            cprint('{} остался голодным. В доме нет еды!'.format(self.name), color='red')
        else:
            cprint('{} слегка перекусил'.format(self.name), color='yellow')
            self.fullness += 5
            self.house.remove_food(food_quantity)
            self.house.add_dirt(5)

    def get_the_pet(self, pet):
        if self.house:
            self.buy_feed()
            pet.settle(self.house)
            self.pets_count += 1
        else:
            cprint('У {} нет дома, он не может взять {}!'.format(
                self.name, pet.get_name()), color='red', attrs=['bold'])

    def work(self):
        cprint('{} сходил на работу'.format(self.name), color='blue')
        self.house.add_money(150)
        self.fullness -= 10

    def watch_mtv(self):
        cprint('{} смотрел MTV целый день'.format(self.name), color='green')
        self.fullness -= 10

    def buy_feed(self, quantity=50):
        if self.house.get_money() >= 50:
            self.house.remove_money(50)
            self.house.add_feed(quantity)
            cprint('{} сходил в магазин за кормом'.format(self.name), color='magenta')
        else:
            cprint('Деньги кончились! {} не может купить корм!'.format(self.name), color='red')

    def shopping(self):
        if self.house.get_money() >= 50:
            cprint('{} сходил в магазин за едой'.format(self.name), color='magenta')
            self.house.remove_money(50)
            self.house.add_food(50)
            if self.house.get_feed() <= 20:
                self.buy_feed()
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red')

    def go_to_the_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint('{} въехал в дом'.format(self.name), color='cyan')

    def clean_the_house(self):
        if self.house:
            dirt = self.house.get_dirt()
            if dirt >= 100:
                cprint('{} убрался в доме'.format(self.name), color='cyan', attrs=['bold'])
                self.house.remove_dirt(100)
            else:
                cprint('{} убрался в доме'.format(self.name), color='cyan', attrs=['bold'])
                self.house.remove_dirt(dirt)
            self.fullness -= 20
            return True
        else:
            return False

    def act(self):
        if self.fullness == 0:
            cprint('{} умер...'.format(self.name), color='red')
            return False

        self.house.add_dirt(1)

        dice = randint(1, 6)
        if self.fullness <= 20:
            self.eat()
        elif self.house.get_money() < 50:
            self.work()
        elif self.house.get_food() <= 20:
            self.shopping()
        elif self.house.get_feed() <= self.pets_count*20:  # Учитываем количество животных, чтобы никто не умер
            self.buy_feed()
        elif self.house.get_dirt() >= 100:
            self.clean_the_house()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        elif dice == 3:
            self.clean_the_house()
        elif dice == 4:
            self.buy_feed()
        else:
            self.watch_mtv()

        return True


class House:

    def __init__(self):
        self.food = 50
        self.money = 0
        self.feed = 0
        self.dirt = 0

    def __str__(self):

        result = colored('В доме осталось:\n', color='blue', attrs=['bold'])
        result += colored('\tЕды - {}\n'.format(self.food), color='cyan')
        result += colored('\tДенег - {}\n'.format(self.money), color='cyan')
        result += colored('\tКорм для животных - {}\n'.format(self.feed), color='cyan')
        result += colored('\tГрязи в доме - {}\n'.format(self.dirt), color='cyan')

        return result

    def add_food(self, quantity):
        self.food += quantity

    def get_food(self):
        return self.food

    def remove_food(self, quantity):
        if self.food > quantity:
            self.food -= quantity
        else:
            self.food = 0

    def add_feed(self, quantity):
        self.feed += quantity

    def get_feed(self):
        return self.feed

    def remove_feed(self, quantity):
        if self.feed > quantity:
            self.feed -= quantity
        else:
            self.feed = 0

    def get_dirt(self):
        return self.dirt

    def add_dirt(self, quantity):
        self.dirt += quantity

    def remove_dirt(self, quantity):
        if self.dirt >= quantity:
            self.dirt -= quantity
        else:
            self.dirt = 0

    def add_money(self, quantity):
        self.money += quantity

    def get_money(self):
        return self.money

    def remove_money(self, quantity):
        if self.money >= quantity:
            self.money -= quantity
        else:
            self.money = 0


cats = []
my_home = House()

person = Man('Вася Пупкин')
person.go_to_the_house(my_home)
person.work()

cats.append(Cat('Васька'))
cats.append(Cat('Петька'))
cats.append(Cat('Борька'))
cats.append(Cat('Кузька'))
cats.append(Cat('Федька'))

for cat in cats:
    person.get_the_pet(cat)

for i in range(1, 366):
    if person.act():
        for cat in cats:
            cat.act()

        print('===================== День {} ====================='.format(i))
        print(my_home)
        cprint('Жители дома:', color='grey', attrs=['bold', 'dark', 'underline'])
        print(person)
        for cat in cats:
            print(cat)
        print('===================================================')
    else:
        break

# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)
# Можно увеличивать количество котов до 5-ти штук (чаще всего все выживают), но грязи в доме становится ...
