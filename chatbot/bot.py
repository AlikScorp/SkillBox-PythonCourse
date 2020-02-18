# -*- coding: utf-8 -*-
"""
    Эхобот для VK
"""
import random
import logging
from dataclasses import dataclass, field
import handlers

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

try:
    from settings import TOKEN, GROUP_ID, SCENARIOS, INTENTS, DEFAULT_ANSWER
except ImportError:
    TOKEN, GROUP_ID, SCENARIOS, INTENTS, DEFAULT_ANSWER = '', '', {}, [], ''
    exit('Please copy settings.py.default to setting.py and add your token and group_id into it.')


@dataclass
class UserState:
    """
        Дата-класс, содержит информацию о пользователе.
    """
    scenario_name: str
    step_name: str
    context: dict = field(default_factory=dict)


class EchoBot:
    """
        Класс представляет собой эхо-бот в который передается id группы (group) и token для работы c API соцсети VK
    """

    group_id: str
    group_title: str
    token: str
    vk: vk_api.vk_api.VkApi
    vk_long_pol: vk_api.bot_longpoll.VkBotLongPoll
    api: vk_api.vk_api.VkApiMethod
    logger: logging.Logger
    user_states: dict

    def __init__(self, group, token):
        self.group_id = group
        self.group_title = ''
        self.token = token

        self.vk = vk_api.VkApi(token=self.token)
        self.long_poll = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()
        self.group_title = self.get_group_title()
        self.user_states = {}

        self.__logger_customizer()

    def __logger_customizer(self):
        """
            Метод настравиает logging.Logger
        :return: None
        """
        self.logger = logging.getLogger('bot')

        datetime_format = '%d.%m.%Y %H:%M:%S'

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s",
                                                      datefmt=datetime_format))
        stream_handler.setLevel(logging.INFO)

        file_handler = logging.FileHandler('bot.log', encoding='utf8', delay=True)
        file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s", datefmt=datetime_format))
        file_handler.setLevel(logging.DEBUG)

        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.DEBUG)

    def run(self):
        """
            Метод осуществляет запуск бота.
            После запуска бот "слушает" события в группе и вызывает обработчик событий в случае их возникновения.
        :return: None
        """

        self.logger.info('Listen to events...')

        for event in self.long_poll.listen():
            try:
                self.on_event(event=event)
            except SystemExit:
                self.logger.info(f'Exiting!!!')
                exit()
            except Exception as exc:
                self.logger.exception(f'Случилось что-то непредвиденное: {exc}')

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

        if int(event.object.from_id) < 0:
            return

        sender = self.get_user_info(user_id=event.object.from_id)
        sender_full_name = sender['first_name'] + ' ' + sender['last_name']
        message = self.get_greetings(user=sender)
        message = message + f"К сожалению, на ваше сообщение \"{event.object.text}\" мне пока нечего ответить."

        self.api.messages.send(message=message, random_id=random.randint(0, 2 ** 20), peer_id=event.object.peer_id)
        self.logger.info(f'Отправили пользователю {sender_full_name} следующее сообщение: "{message}"')

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
            user_full_name = user_info['first_name'] + ' ' + user_info['last_name']

            message = self.get_greetings(user_info) if message is None else message

            if member_id == 36414847:
                self.logger.debug(f'Отправили пользователю {user_full_name} следующее сообщение: "{message}"')
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
            Посылает пприветствие новому члену сообщества
        :param user_id:
        :return: Результат выполнения метода send
        """
        message = self.get_greetings(self.get_user_info(user_id=user_id))
        return self.send_message_to_user(message=message, user_id=user_id)

    def send_farewell(self, user_id):
        """
            Послыает сообщение пользователю вышедшему из сообщества
        :param user_id: ID пользователя которому посылается сообщение
        :return: Результат выполнения метода send
        """
        user_info = self.get_user_info(user_id)
        message = f"Очень жаль, что {user_info['first_name']} {user_info['last_name']} покинул группу " \
                  f"\"{self.group_title}\".\n" \
                  f"Возвращайтесь, мы всегда будем Вам рады."

        self.logger.info(f'Пользователь {user_info["first_name"]} {user_info["last_name"]} '
                         f'покинул группу {self.group_title}')

        return self.send_message_to_user(message=message, user_id=user_id)

    def on_event(self, event):
        """
            Метод реагирует на события
        :param event: VkBotMessageEvent object
        :return: None
        """

        if event.object.text == "Hasta la vista, baby":
            raise SystemExit
        elif event.type != VkBotEventType.MESSAGE_NEW:
            self.logger.debug(f'Какое-то, пока, неизвестное мне событие {event.type}.')
            return

        user_id: int = event.object.peer_id
        text: str = event.object.text

        if user_id in self.user_states:
            text_to_send = self.continue_scenario(user_id, text=event.object.text)
        else:
            # Ищем в интентах введенный пользователем текст
            for intent in INTENTS:
                self.logger.debug(f'Проверяем на совпадение с {intent}')
                if any(token in text.lower() for token in intent['tokens']):
                    if intent['answer']:
                        text_to_send = intent['answer']
                    else:
                        text_to_send = self.start_scenario(user_id, intent['scenario'])

                    break
            else:
                text_to_send = DEFAULT_ANSWER

        self.send_message_to_user(message=text_to_send, user_id=user_id)

    def start_scenario(self, user_id, scenario_name):
        """
            Start scenario
        :param user_id: Идентификатор пользователя
        :param scenario_name: Наименование сценария
        :return: Текст для отправки пользователю
        """
        scenario = SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']

        self.user_states[user_id] = UserState(scenario_name=scenario_name, step_name=first_step)

        return text_to_send

    def continue_scenario(self, user_id, text):
        """
            Продолжение сценария
        :param user_id: ID пользователя
        :param text: Текст полученный от пользователя
        :return: text_to_send - Текст для отправки пользователю
        """
        state = self.user_states[user_id]
        steps = SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]

        try:
            handler = getattr(handlers, step['handler'])
        except AttributeError as exc:
            self.logger.info(f'Неправильный хандлер при обработке шага {state.step_name}, {exc}')
            return 'Возникла ошибка при обработке входных данных. Приносим свои извинения.'

        if handler(text=text, context=state.context):
            next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**state.context)
            if next_step['next_step']:
                state.step_name = step['next_step']
            else:
                self.logger.info('Зарегистрирован пользователь: {name} <{email}>'.format(**state.context))
                self.user_states.pop(user_id)
        else:
            text_to_send = step['failure_text'].format(**state.context)

        return text_to_send


def main():
    """
        Функция вызывается в случае непосредстевнного запуска скрипта.
    :return:
    """
    bot = EchoBot(GROUP_ID, token=TOKEN)
    bot.run()


if __name__ == '__main__':
    main()
