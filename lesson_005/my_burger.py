# В данном модуле содержаться функции для добавления ингредиентов при "сборке" бургеров


def add_bun(number=0):
    """
        Добавляем булочку
    """
    if number == 0:
        print('\tКладем карамелизованную булочку')
    else:
        print('\tНакрываем это еще одной булочкой с румяной корочкой')


def add_beef_patty(number=0):
    """
       Добавляем бифштекс
    """
    if number == 0:
        print('\tКладем сочный рубленый бифштекс из натуральной цельной говядины')
    else:
        print('\tЕще один сочный рубленый бифштекс')


def add_onion():
    """
        Добавляем лук
    """
    print('\tДобавим мелконарезанного лучка')


def add_cheese(number=0):
    """
        Добавим сыра
    """
    if number == 0:
        print('\tКладем вкуснейший кусочек сыра «Чеддер»')
    else:
        print('\tДобавим еще один кусочек сыра')


def add_pickles():
    """
        Добавим соленых огурчиков
    """
    print('\tДобавим пару кусочков маринованного огурчика')


def add_chicken():
    """
        Добавим курицу
    """
    print('\tДобавим сочное филе цельной куриной грудки')


def add_salad():
    """
        Добавим листья салата
    """
    print('\tДобавим свежайший лист салата')


def add_tomato():
    """
        Добавим томатов
    """
    print('\tДобавим несколько ломтиков свежайшего спелого помидора')


def add_guacamole():
    """
        Добавляем соус
    """
    print('\tДобавим соус гуакамоле и карри с добавлением фруктов и кайенского перца')


def add_ketchup():
    """
        Добавляем кетчуп
    """
    print('\tДобавим немного кетчупа для пикантности')


def add_mustard():
    """
       Добавляем горчицу
    """
    print('\tИ немного горчички для остроты')


def is_ready():
    """
        Подаем бургер
    """
    print('\nВаш бургер готов!!! Приятного аппетита!!!')


def get_double_cheeseburger():
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


def get_chicken_gurme_exotic():
    add_bun()
    add_mustard()
    add_chicken()
    add_tomato()
    add_salad()
    add_guacamole()
    add_bun(1)
    is_ready()
    print('Но не забывайте -  в нём 621Ккал!!! :-)')
