"""
    Handlers are here
"""
import re

re_name = re.compile(r'^[\w\-\s]{3,40}$')
re_email = re.compile(r'(^\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)\b')


def handle_name(text: str, context: dict):
    """
        Handle для проверки имени
    :param text: Текст сообщения от пользователя
    :param context:
    :return: True/False
    """

    match = re.match(re_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False


def handle_email(text: str, context: dict):
    """
        Handle длф проверки адреса электронной почты
    :param text: Текст сообщения от пользователя
    :param context: Информация о пользователе
    :return: True/False
    """
    matches = re.findall(re_email, text)
    if len(matches) > 0:
        context['email'] = matches[0]
        return True
    else:
        return False


def handle_error(text: str, context: dict):
    """
        Хандлер вызывается в случае если не обнаружен нужный хандлер.
    :param text: Текст полученный от пользователя
    :param context: Информация о пользователе
    :return: True/False
    """

    return True
