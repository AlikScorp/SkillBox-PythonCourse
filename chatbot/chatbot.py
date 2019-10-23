# -*- coding: utf-8 -*-
"""
    Эхобот для VK
"""
import random

import vk_api
from _token import token
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class EchoBot:
    """
        Класс представляет собой эхо-бот в который передается id группы и token для работы c API соцсети VK
    """

    def __init__(self, group, token):
        self.group_id = group
        self.group_title = ''
        self.token = token

        self.vk = vk_api.VkApi(token=self.token)
        self.long_poll = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()
        self.group_title = self.get_group_title()

    def run(self):
        """
            Метод осуществляет запуск бота.
            После запуска бот "слушает" события в группе и вызывает обработчик событий в случае их возникновения.
        :return: None
        """

        print('Listen to events...')

        for event in self.long_poll.listen():
            try:
                self.on_event(event=event)
            except SystemExit:
                print("Exiting!!!")
                exit()
            except Exception as exc:
                print(exc)

    def get_group_title(self):
        """
            Метод возвращает title группы по его id
        :return:
        """

        group = self.api.groups.getById(group_id=self.group_id)
        group_title = group[0]['name']

        return group_title

    def get_user_info(self, user_id):
        """
            Метод загружает информацию о пользователе из соцсети VK по его id
        :param user_id:
        :return: Словарь с информацией о пользователе
        """

        sender = self.api.users.get(user_ids=user_id, fields='city,nickname')

        sender_info = {
            'first_name': sender[0]['first_name'],
            'last_name': sender[0]['last_name'],
            'nickname': sender[0]['nickname'],
            'city_title': sender[0]['city']['title'],
        }

        return sender_info

    def reply_on_new_message(self, event):
        """
            Метод отвечает на новые сообщения посланные в сообщество
        :param event:
        :return:
        """

        sender = self.get_user_info(user_id=event.object.from_id)
        message = self.get_greetings(user=sender)
        message = message + f"К сожалению, на ваше сообщение \"{event.object.text}\" мне пока нечего ответить."

        self.api.messages.send(message=message, random_id=random.randint(0, 2 ** 20), peer_id=event.object.peer_id)

    def get_greetings(self, user):
        """
            Метод отсылает приветствие пользователю отправившему сообщение в группу.
        :return: True в случае успеха и False в противном случае
        """
        message = f"Привет, {user['first_name']} {user['last_name']} " \
                  f"({user['nickname']}) из города {user['city_title']}!\n" \
                  f"Я, Архивариус сообщества \"{self.group_title}\".\n"

        return message

    def send_message_to_members(self, message: str = None):
        """
            Метод отправляет сообщение всем членам сообщества.
        :return: Результат выполнения метода send
        """

        members = self.api.groups.getMembers(group_id=self.group_id)

        for member_id in members['items']:
            user_info = self.get_user_info(user_id=member_id)

            message = self.get_greetings(user_info) if message is None else message

            if member_id == 36414847:
                return self.send_message_to_user(message=message, user_id=member_id)

    def send_message_to_user(self, user_id: int, message: str = None):
        """
            Метод посылает сообщение message пользователю с user_id
        :param user_id: ID пользователя
        :param message: Сообщение
        :return: None
        """

        return self.api.messages.send(message=message, random_id=random.randint(0, 2 ** 20), user_id=user_id)

    def send_greetings(self, user_id):
        """
            Посылает привествие новому члену сообщества
        :param user_id:
        :return: Результат выполнения метода send
        """
        message = self.get_greetings(self.get_user_info(user_id=user_id))
        return self.send_message_to_user(message=message, user_id=user_id)

    def send_farewell(self, user_id):
        """
            Послыает сообщение пользователю вышедшему из сообщества
        :param user_id: ID пользователя которому посылается сообщение
        :return:
        """
        user_info = self.get_user_info(user_id)
        message = f"Очень жаль, что {user_info['first_name']} {user_info['last_name']} покинул группу " \
                  f"\"{self.group_title}\".\n" \
                  f"Возвращайтесь, мы всегда будем Вам рады."
        return self.send_message_to_user(message=message, user_id=user_id)

    def on_event(self, event):
        """
            Метод реагирует на события
        :param event:
        :return:
        """
        if event.object.text == "Hasta la vista, baby":
            raise SystemExit

        if event.type == VkBotEventType.MESSAGE_NEW:
            self.reply_on_new_message(event=event)
        elif event.type == VkBotEventType.GROUP_JOIN:
            self.send_greetings(user_id=event.object.user_id)
        elif event.type == VkBotEventType.GROUP_LEAVE:
            self.send_farewell(user_id=event.object.user_id)
        else:
            print(f'Какое-то, пока, неизвестное мне событие {event.type}.\n{event}')


if __name__ == '__main__':
    group_id = 187871287

    bot = EchoBot(group_id, token=token)
    bot.run()
