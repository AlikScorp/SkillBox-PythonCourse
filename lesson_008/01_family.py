# -*- coding: utf-8 -*-

from termcolor import cprint, colored
from random import randint


# ============================================= Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:

    def __init__(self, food=50, money=100):
        self.food = food
        self.money = money
        self.feed = 0
        self.dirt = 0
        self.total_earned = 0
        self.total_eaten = 0

    def __str__(self):

        result = colored('В доме осталось:\n', color='blue', attrs=['bold'])
        result += colored('\tЕды - {}\n'.format(self.food), color='cyan')
        result += colored('\tДенег - {}\n'.format(self.money), color='cyan')
        result += colored('\tКорм для животных - {}\n'.format(self.feed), color='cyan')
        result += colored('\tГрязи в доме - {}\n'.format(self.dirt), color='cyan')

        return result

# TODO Можно оформить функции изменяющие количество продуктов как свойство (property)
#  По ссылке можно посмотреть пример на русском
#  https://pythonz.net/references/named/property/
    def add_food(self, quantity):
        self.food += quantity

    def get_food(self):
        return self.food

    def remove_food(self, quantity):
        if self.food > quantity:
            self.food -= quantity
            self.total_eaten += quantity
        else:
            self.total_eaten += self.food
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
        self.total_earned += quantity

    def get_money(self):
        return self.money

    def remove_money(self, quantity):
        if self.money >= quantity:
            self.money -= quantity
        else:
            self.money = 0


class Human:

    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.house = None
        # TODO Если статус будет использоваться только в двух вариантах жив/мертв, то лучше сделать
        #  его логического типа  (bool: True/False)
        self.status = 1

    def __str__(self):
        if self.status:
            return colored('{}: {}, сытость - {}, счастье - {}'.format(
                self.name, 'Имеет дом' if self.house else 'Не имеет дома', self.fullness, self.happiness),
                color='magenta', attrs=['bold'])
        else:
            return colored('{}: RIP!!!'.format(self.name), color='white', attrs=['bold', 'dark'])

    def go_to_the_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint('{} теперь имеет дом'.format(self.name), color='cyan')

    def eat(self):
        pass

    def get_the_pet(self, pet):
        pass

    def work(self):
        pass

    def buy_feed(self, quantity=50):
        pass

    def shopping(self):
        pass

    def clean_house(self):
        pass

    def act(self):
        pass
# TODO В классе Human нужно оставить только то, что свойственно всем наследникам.
#  Уборку, например, нужно перенести в Wife.
#  А метод eat лучше сделать общим в Human. Для различий в выводимом тексте можно использовать константы
#  в классах мужа и жены.


class Husband(Human):

    def __str__(self):
        return super().__str__()

    def __init__(self, name):
        super().__init__(name=name)

    def eat(self):
        if self.house:
            food = self.house.get_food()
            if food >= 30:
                cprint('{} хорошенько поел!'.format(self.name), color='yellow')
                self.house.remove_food(quantity=30)
                self.fullness += 30
                self.happiness += 10
                self.house.add_dirt(quantity=10)
            elif food != 0:
                cprint('{} немного перекусил!'.format(self.name), color='yellow')
                self.house.remove_food(quantity=food)
                self.fullness += food
                self.happiness += 5
                self.house.add_dirt(quantity=5)
            else:
                cprint('{} не нашёл еды!'.format(self.name), color='yellow')
        else:
            cprint('{} бездомный, у него нет еды!'.format(self.name), color='yellow')

    def act(self):
        if not self.status:
            cprint('{} мертв :-('.format(self.name), color='white', attrs=['dark', 'bold'])
            return

        if self.fullness == 0:
            self.status = 0
            cprint('{} умер от голода! RIP! :-('.format(self.name), color='red')
            return

        if self.happiness < 10:
            self.status = 0
            cprint('{} умер от депрессии! RIP! :-('.format(self.name), color='red')
            return

        if self.house.get_dirt() > 90:
            self.happiness -= 10

        dice = randint(1, 3)

        if self.fullness < 20:
            self.eat()
        elif self.house.get_money() <= 50:
            self.work()
        elif self.happiness <= 10:
            self.gaming()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        else:
            self.gaming()

    def gaming(self):
        cprint('{} Весь день играл в WoT'.format(self.name), color='yellow')
        self.fullness -= 10
        self.happiness += 20

    def work(self):
        self.happiness -= 20
        if self.house:
            cprint('{} сходил на работу'.format(self.name), color='yellow')
            self.house.add_money(150)
            self.fullness -= 10
        else:
            self.fullness -= 10
            cprint('{} сходил на работу, но ему негде хранить деньги. Нужен дом!'.format(self.name, self.name),
                   color='yellow')


class Wife(Human):

    def __init__(self, name):
        super().__init__(name=name)
        self.total_coats = 0

    def __str__(self):
        return super().__str__()

    def eat(self):
        if self.house:
            food = self.house.get_food()
            if food >= 30:
                cprint('{} хорошенько поела!'.format(self.name), color='yellow')
                self.house.remove_food(quantity=30)
                self.fullness += 30
                self.happiness += 10
                self.house.add_dirt(quantity=10)
            elif food != 0:
                cprint('{} немного перекусила!'.format(self.name), color='yellow')
                self.house.remove_food(quantity=food)
                self.fullness += food
                self.happiness += 5
                self.house.add_dirt(quantity=5)
            else:
                cprint('{} не нашла еды!'.format(self.name), color='yellow')
        else:
            cprint('{} бездомная, у неё нет еды!'.format(self.name), color='yellow')

    def act(self):

        if not self.status:
            cprint('{} мертва :-('.format(self.name), color='white', attrs=['dark', 'bold'])
            return

        if self.fullness == 0:
            self.status = 0
            cprint('{} умерла от голода! RIP! :-('.format(self.name), color='red')
            return

        if self.happiness < 10:
            self.status = 0
            cprint('{} умерла от депрессии! RIP! :-('.format(self.name), color='red')
            return

        if self.house.get_dirt() > 90:
            self.happiness -= 10

        dice = randint(1, 3)

        if self.fullness < 20:
            self.eat()
        elif self.house.get_dirt() >= 90:
            self.clean_house()
        elif self.happiness <= 20:
            self.buy_fur_coat()
        elif self.house.get_food() <= 60:
            self.shopping()
        elif dice == 1:
            self.clean_house()
        elif dice == 2:
            self.eat()
        else:
            self.shopping()

    def shopping(self):
        self.fullness -= 10
        self.happiness -= 5
        money = self.house.get_money()
        if money >= 60:
            cprint('{} купила еды'.format(self.name), color='yellow')
            self.house.add_food(quantity=60)
            self.house.remove_money(quantity=60)
        elif money != 0:
            cprint('{} купила немного еды'.format(self.name), color='yellow')
            self.house.add_food(quantity=money)
            self.house.remove_money(quantity=money)
        else:
            cprint('{} не может купить еды. В доме нет денег!'.format(self.name), color='red')

    def buy_fur_coat(self):
        self.fullness -= 10
        money = self.house.get_money()
        if money >= 350:
            cprint('{} купила шубу'.format(self.name), color='yellow')
            self.house.remove_money(350)
            self.happiness += 60
            self.total_coats += 1
        else:
            cprint('{} не может купить шубу! В доме мало денег.'.format(self.name), color='red')

    def clean_house(self):
        self.fullness -= 10
        self.happiness -= 10
        dirt = self.house.get_dirt()
        if dirt <= 100:
            self.house.remove_dirt(quantity=100)
        else:
            self.house.remove_dirt(quantity=dirt)

        cprint('{} убралась в доме'.format(self.name), color='yellow')


if __name__ == "__main__":

    home = House()
    serge = Husband(name='Сережа')
    masha = Wife(name='Маша')

    serge.go_to_the_house(home)
    masha.go_to_the_house(home)

    for day in range(365):
        home.add_dirt(quantity=10)
        cprint('================== День {} =================='.format(day + 1), color='red')
        serge.act()
        masha.act()
        print(serge)
        print(masha)
        print(home)
    # TODO Отформатировал ваш код. Аргументы функций лучше переносить на новую строку.
    #  Так ваш код будет проще читать.
    cprint('За год было съедено {} еды, заработано {} денег и купленно {} шуб'.format(
        home.total_eaten,
        home.total_earned,
        masha.total_coats
    ), color='grey')


# TODO после реализации первой части - отдать на проверку учителю

# =============================================  Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов


class Cat:

    def __init__(self):
        pass

    def act(self):
        pass

    def eat(self):
        pass

    def sleep(self):
        pass

    def soil(self):
        pass


# =============================================  Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)

class Child:

    def __init__(self):
        pass

    def __str__(self):
        return super().__str__()

    def act(self):
        pass

    def eat(self):
        pass

    def sleep(self):
        pass

# TODO после реализации второй части - отдать на проверку учителем две ветки


# ============================================= Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.


# home = House()
# serge = Husband(name='Сережа')
# masha = Wife(name='Маша')
# kolya = Child(name='Коля')
# murzik = Cat(name='Мурзик')
#
# for day in range(365):
#     cprint('================== День {} =================='.format(day), color='red')
#     serge.act()
#     masha.act()
#     kolya.act()
#     murzik.act()
#     cprint(serge, color='cyan')
#     cprint(masha, color='cyan')
#     cprint(kolya, color='cyan')
#     cprint(murzik, color='cyan')
#

# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')
