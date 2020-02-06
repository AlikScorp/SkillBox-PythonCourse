# -*- coding: utf-8 -*-
"""
    Игра "Подземелье и Драконы"
"""

# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
# в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
# где N - это номер локации (целое число), а T (вещественное число) - это время,
# которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
# то он тратит на это 30000 секунд.
# По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
# Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
# которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
# которое потратит игрок для уничтожения данного монстра.
# Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
# Гарантируется, что в начале пути будет только две локации и не будет мобов
# (то есть в коренном json-объекте содержится список, содержащий только два json-объекта и ничего больше).
#
# На прохождение игры игроку дается 123456.0987654321 секунд.
# Цель игры: за отведенное время найти выход ("Hatch")
#
# По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
# в каждую локацию можно попасть только один раз,
# и выйти из нее нельзя (то есть двигаться можно только вперед).
#
# Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
# Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
# готовый к следующей попытке (игра начинается заново).
#
# Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
# При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.
#
# Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
# - текущую локацию
# - текущее количество опыта
# - текущие дату и время (для этого используйте библиотеку datetime)
# После успешного или неуспешного завершения игры вам необходимо записать
# всю собранную информацию в csv файл dungeon.csv.
# Названия столбцов для csv файла: current_location, current_experience, current_date
#
#
# Пример взаимодействия с игроком:
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло времени: 00:00
#
# Внутри вы видите:
# — Вход в локацию: Location_1_tm1040
# — Вход в локацию: Location_2_tm123456
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали переход в локацию Location_2_tm1234567890
#
# Вы находитесь в Location_2_tm1234567890
# У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
# Прошло времени: 20:00
#
# Внутри вы видите:
# — Монстра Mob_exp10_tm10
# — Вход в локацию: Location_3_tm55500
# — Вход в локацию: Location_4_tm66600
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали сражаться с монстром
#
# Вы находитесь в Location_2_tm0
# У вас 10 опыта и осталось -9.9012345679 секунд до наводнения
#
# Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!
#
# У вас темнеет в глазах... прощай, принцесса...
# Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)
# Ну, на этот-то раз у вас все получится! Трепещите, монстры!
# Вы осторожно входите в пещеру... (текст умирания/воскрешения можно придумать свой ;)
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло уже 0:00:00
# Внутри вы видите:
#  ...
#  ...
#
# и так далее...
from __future__ import annotations
import json
import time as tm
import re
from decimal import Decimal
from typing import Optional, List
from termcolor import cprint, colored

remaining_time = '123456.0987654321'
# если изначально не писать число в виде строки - теряется точность!
field_names = ['current_location', 'current_experience', 'current_date']


class Location:
    """
        Класс локации
        Локации могут содержать монстров и другие локации
    """
    __title: str
    __time_to_pass: Decimal
    __monsters: List[Monster]
    __locations: List[Location]
    __parent: Optional[Location]
    __is_exit: bool
    __necessary_experience: int
    __location_json: dict

    def __init__(self, location_json: dict):
        self.__location_json = location_json
        self.__monsters = []
        self.__locations = []
        self.is_exit = False
        self.necessary_experience = 0
        self.__parent = None

        self.parse_json(self.__location_json)

    @property
    def necessary_experience(self):
        """
            Возвращает необходимый опыт героя для прохождения в локацию
        :return: Опыт
        """
        return self.__necessary_experience

    @necessary_experience.setter
    def necessary_experience(self, experience):
        self.__necessary_experience = experience

    @property
    def is_exit(self):
        """
            Определяет является ли локация выходом из подземелья
        :return:
        """
        return self.__is_exit

    @is_exit.setter
    def is_exit(self, status):
        self.__is_exit = status

    def parse_json(self, location_json: dict):
        """
            Метод парсит json в объекты
        :return: None
        """

        for title, content in location_json.items():
            self.__parse_title(title)

            for item in content:
                if isinstance(item, str):
                    self.__add_monster(item)
                elif isinstance(item, dict):
                    for key, value in item.items():
                        if 'Hatch' not in key:
                            child = Location(item)
                            child.parent = self
                            self.__locations.append(child)
                        else:
                            self.__locations.append(DungeonExit(item))
                else:
                    raise ValueError('Неизвестный элемент ')

    def __add_monster(self, monster):
        """
            Метод добавляет монстра (class Monster) в локацию
        :param monster: Описание монстра
        :return: None
        """
        title, exp, time = re.split(r'_exp|_tm', monster)
        self.__monsters.append(Monster(title=title, loot=Decimal(exp), time=Decimal(time)))

    @property
    def monsters(self) -> List[Monster]:
        """
            Возвращает всех монстров в локации
        :return: __monsters
        """
        return self.__monsters

    def alive_monsters(self):
        """
            Возвращает список живых монстров
        :return:
        """
        return [x for x in self.__monsters if not x.is_dead]

    def get_status(self):
        """
            Метод возвращает строку статуса локации ... кол-во монстров и внутренних локаций
        :return: Статус
        """
        status = colored('Вы видите:\n', color='green')

        for monster in self.__monsters:
            status += monster.get_info()

        for location in self.__locations:
            status += location.get_info() + '\n'

        return colored(status, 'grey')

    def get_info(self):
        """
            Возвращает инофрмацию о локации
        :return: Информация в виде строки
        """
        return f'\t— Вход в локацию {self.title}(ttp: {self.time})'

    @property
    def parent(self):
        """
            Возвращает "родительскую" локацию
        :return:
        """
        return self.__parent

    @parent.setter
    def parent(self, location):
        self.__parent = location

    @property
    def locations(self):
        """
            Возвращает список "дочерних" локаций
        :return: Список локаций
        """
        return self.__locations

    @property
    def title(self):
        """
            Метод-свойство, возвращает название локации
        :return: Назавание
        """
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def time(self):
        """
            Метод-свойство, возвращает время необходмое для прохождения локации
        :return: Время
        """
        return self.__time_to_pass

    @time.setter
    def time(self, time: Decimal):
        self.__time_to_pass = time

    def __parse_title(self, title):
        title, time = title.split('_tm')
        self.title, self.time = title, Decimal(time)


class DungeonExit(Location):
    """
        Локация выход из подземелья
    """
    __message: str

    def __init__(self, location_json):
        super().__init__(location_json)

        self.is_exit = True
        self.necessary_experience = 280

    def parse_json(self, location_json: dict):
        """
            Метод переопределяет родительский метод и парсит json
        :param location_json:
        """
        for key, value in location_json.items():
            self.__title, time_to_pass = key.split('_tm')
            self.__time_to_pass = Decimal(time_to_pass)
            self.__message = value

    @property
    def title(self):
        """
            Метод-свойство, возвращает название локации
        :return: Назавание
        """
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def time(self):
        """
            Метод-свойство, возвращает время необходмое для прохождения локации
        :return: Время
        """
        return self.__time_to_pass

    @time.setter
    def time(self, time: Decimal):
        self.__time_to_pass = time


class Hero:
    """
        Класс героя ...
        Обладает следующими свойствами:
            time - Общее время на прохождение подземелья
            experience - Опыт за победу над монстрами
            location - локация в которойнаходится герой

        Методы:
            attack - атакует монстра
            move - двигается в другую локацию

    """
    __experience: Decimal
    __time: Decimal
    __elapsed_time: Decimal
    __location: Location

    def __init__(self, exp: Decimal, time: Decimal):
        self.__experience = exp
        self.__time = time
        self.__elapsed_time = Decimal('0')

    @property
    def experience(self):
        """
            Свойство-метод, возвращает текущий опыт героя
        :return: Опыт
        """
        return self.__experience

    @experience.setter
    def experience(self, exp: Decimal):
        self.__experience = exp

    @property
    def time(self):
        """
            Свойство-метод, возвращает оставшееся количество времени героя
        :return: Время
        """
        return self.__time

    @time.setter
    def time(self, time: Decimal):
        self.__time = time

    @property
    def elapsed_time(self):
        """
            Свойтсво-метод, возвращает оставшееся количество времени героя
        :return: Время
        """
        return self.__elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, time: Decimal):
        self.__elapsed_time = time

    @property
    def location(self):
        """
            Свойство-метод, возвращает текущее метосположение (класс Location) героя
        :return: Местоположение
        """
        return self.__location

    @location.setter
    def location(self, location):
        self.__location = location

    def available_actions(self):
        """
            Метод возвращает список действий героя в текущей локации
        :return: None
        """
        pass


class Monster:
    """
        Класс монстров
        Имею свойства:
            loot (экспа которую дает победа над монстром)
            time (время которое необходимо, чтобы победить монстра)
    """
    __loot: Decimal
    __time: Decimal
    __is_dead: bool
    __title: str

    def __init__(self, title: str, loot: Decimal, time: Decimal):
        self.__title = title
        self.__time = time
        self.__loot = loot
        self.__is_dead = False

    @property
    def title(self):
        """
            Метод-свойство, возвращает название монстра
        :return: Название
        """
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def is_dead(self):
        """
            Метод возвращает состояние монстра жив/мертв
        :return:
        """
        return self.__is_dead

    @is_dead.setter
    def is_dead(self, status: bool):
        self.__is_dead = status

    @property
    def loot(self):
        """
            Опыт за убийство
        :return: Количество опыта
        """
        return self.__loot

    @loot.setter
    def loot(self, loot: Decimal):
        self.__loot = loot

    @property
    def time(self):
        """
            Время на убийство
        :return: Количество времени
        """
        return self.__time

    @time.setter
    def time(self, time: Decimal):
        self.__time = time

    def get_info(self) -> str:
        """
            Возвращает информацию об монстре
        :return: Полная информация об монстре
        """

        info = f'\t— Монстр {self.title} (Опыт за убийство: {self.loot}; Время на убийство: {self.time})'

        if self.is_dead:
            info += colored(' - Мертв\n ', color='red')
        else:
            info += colored(' - Живой\n ', color='yellow')

        return info


class Game:
    """
        Игра в Подземелье и Драконы
    """
    __hero: Hero
    __dungeon: dict

    def __init__(self, dungeon: dict):
        self.__dungeon = dungeon
        self.__hero = Hero(exp=Decimal(0), time=Decimal(remaining_time))
        self.__hero.location = Location(location_json=dungeon)

    @staticmethod
    def __seconds_to_time(elapsed_seconds: Decimal):
        """
            Переводит количество прошедших секунд в удобочитаемый формат типа DD:HH:MM:SS
        :param elapsed_seconds:
        :return: Строку прошедшего времени
        """
        days = elapsed_seconds // 86400
        hours = (elapsed_seconds // 3600) % 24
        minutes = (elapsed_seconds // 60) % 60
        seconds = elapsed_seconds % 60

        return f'{days}:{hours:02}:{minutes:02}:{seconds:02}'

    def restart(self):
        """
            Метод обнуляет прогресс в игре
        :return: None
        """
        self.__hero = Hero(exp=Decimal(0), time=Decimal(remaining_time))
        self.__hero.location = Location(location_json=self.__dungeon)

    def run(self):
        """
            Метод запускает игру
        :return:
        """
        while True:

            if self.__hero.location.is_exit:
                cprint('Поздравляем!!! '
                       'История о Вашем героическом подвиге будет передоваться от поколения к поколению!',
                       color='magenta')
                break

            if self.__hero.time < 0:
                cprint('Ледяная речная вода заполнила подземелье и накрыла вас с головой.', color='red')
                cprint('После тщетных попыток побороть сильное речное течение, '
                       'Вы все-таки решились вдохнуть речную воду.', color='red')
                cprint('Но Вы же не рыба! Результат - известен! Вы - утонули!!!', color='red')
                cprint('Боги, во славу которых вы совершаете все свои подвиги, '
                       'воскрешают Вас возле входа в подземелье.', color='blue')
                cprint('Начните сначала и не допускайте прежних ошибок!!!', color='blue')

                self.restart()
                tm.sleep(5)
                continue

            cprint('*' * 100)
            cprint(f'У вас {self.__hero.experience} опыта и осталось '
                   f'{self.__hero.time} секунд до наводнения.', color="red")

            cprint(f'Прошло времени: {self.__seconds_to_time(self.__hero.elapsed_time)}', color='red')
            cprint(f'Вы находитесь в: {self.__hero.location.title}, время на прохождение локации (ttp): '
                   f'{self.__hero.location.time}', color='green')
            print(self.__hero.location.get_status())

            cprint('Возможные действия:', color='cyan')
            action = self.actions()

            if action == 1:
                self.attack_monsters()
            elif action == 2:
                self.change_location()
            elif action == 3:
                break
            else:
                cprint('Не корректный выбор', color='red')

            tm.sleep(1)

    def change_location(self):
        """
            Метод выполняет функциональность смены локации
        :return: None
        """

        list_of_locations = dict()

        cprint('Ха! А теперь пойдем ... Куда собственно идем?', color='red')

        for number, location in enumerate(self.__hero.location.locations):
            cprint(f'\t{number + 1}. {location.get_info()}', color='cyan')
            list_of_locations[str(number + 1)] = location

        choice = input('Куда пойдем (0 если передумали)? ')

        if choice != '0' and choice in list_of_locations.keys():

            if self.__hero.location.alive_monsters():
                cprint(f'Чтобы не побеспокоить затаившихся в темноте монстров, '
                       f'безшумно направляемся в локацию ', color='blue', end='')
            else:
                cprint(f'Гордой походкой победителя, переступая через поверженных монстров, '
                       f'направляемся в локацию ', color='blue', end='')

            cprint(f'"{list_of_locations[choice].title}"', color='blue')

            if self.__hero.experience >= list_of_locations[choice].necessary_experience:
                self.__hero.location = list_of_locations[choice]
                self.__hero.time -= list_of_locations[choice].time
                self.__hero.elapsed_time += list_of_locations[choice].time
            else:
                cprint('У Вас не достаточно опыта чтобы попасть в указанную локацию', color='red')

        elif choice == '0':
            cprint('Нормальные герои всегда идут в обход!?', color='red')

        elif choice == '':
            cprint('Колебание не к лицу героям ...', color='red')

        else:
            cprint('Хм! ... Такой локации здесь нет. Поищем в другом месте ...', color='red')

    def attack_monsters(self):
        """
            Метод выполняет функциональность атаки монстров
        :return:
        """

        list_of_monsters = dict()
        cprint('Уррррраааааа! В атаку!!!!!! ... Хм! ... А кого собственно атакуем?', color='red')

        for number, monster in enumerate(self.__hero.location.alive_monsters()):
            cprint(f'\t{number + 1}. {monster.get_info()}', color='cyan', end='')
            list_of_monsters[str(number + 1)] = monster

        choice = input('Какого монстра будем атаковать (0 если передумали)? ')

        if choice != '0' and choice in list_of_monsters.keys():
            cprint(f'Атакуем монстра: {list_of_monsters[choice].title}', color='red')
            list_of_monsters[choice].is_dead = True
            self.__hero.time -= list_of_monsters[choice].time
            self.__hero.experience += list_of_monsters[choice].loot

        elif choice == '0':
            cprint('Струсил! Струсил! Струсил! ... Шучу! Осторожность превыше всего.', color='red')

        elif choice == '':
            cprint('Колебание не к лицу героям ...', color='red')

        else:
            cprint('Хм! ... Такого монстра в этой локации нет. Наверняка перебежал в другую.', color='red')

    @staticmethod
    def actions() -> int:
        """
            Метод выводит информацию о возможных действиях героя
        :return: Номер действия
        """
        cprint('\t1. Атаковать монстра', color='cyan')
        cprint('\t2. Перейти в другую локацию', color='cyan')
        cprint('\t3. Сдаться и выйти из игры', color='cyan')

        return int(input(colored("Что будем делать? ", 'cyan')))


def main():
    """
        Функция выполняется в случае непосредственного запуска скрипта
    :return: None
    """
    with open('rpg.json', 'r', encoding='utf8') as file:
        dungeon = json.load(file)

    game = Game(dungeon=dungeon)
    game.run()


if __name__ == '__main__':
    main()

# Учитывая время и опыт, не забывайте о точности вычислений!
