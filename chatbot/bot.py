# -*- coding: utf-8 -*-
"""
    Эхобот для VK
"""
import os
import random
import logging
from typing import Optional
import handlers
import requests
import peewee as pw

import vk_api
from playhouse.db_url import connect
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from chatbot.image_filler import ImageFiller, ImageFillerPlaceholder

try:
    from settings import TOKEN, GROUP_ID, SCENARIOS, INTENTS, DEFAULT_ANSWER, DEFAULT_IMAGE
except ImportError:
    TOKEN, GROUP_ID, SCENARIOS, INTENTS, DEFAULT_ANSWER, DEFAULT_IMAGE = '', '', {}, [], '', ''
    exit('Please copy settings.py.default to setting.py and add your token and group_id into it.')


class UserInformation:
    """
        Класс содержит информацию о пользователе
    """
    db: pw.SqliteDatabase
    db_proxy: pw.DatabaseProxy
    record: Optional[pw.Model] = None

    def __init__(self):
        self.db_proxy = pw.DatabaseProxy()
        self.db = connect('sqlite:///vk_bot_users.db')
        self.db_proxy.initialize(self.db)

        class BaseModel(pw.Model):
            """
                Базовая модель
            """
            class Meta:
                """
                    Настройка покдлючения к базе данных
                """
                database = self.db_proxy

        class User(BaseModel):
            """
                Модель для работы с таблицей пользователей
            """
            user_id = pw.IntegerField()
            first_name = pw.CharField()
            last_name = pw.CharField()
            full_name = pw.CharField()
            email = pw.CharField()
            city = pw.CharField()
            photo = pw.CharField()
            scenario_name = pw.CharField()
            step_name = pw.CharField()

        class RegisteredUser(BaseModel):
            """
                Модель для работы с зарегистрированными пользователями
            """
            user_id = pw.IntegerField()
            first_name = pw.CharField()
            last_name = pw.CharField()
            full_name = pw.CharField()
            email = pw.CharField()
            city = pw.CharField()
            photo = pw.CharField()
            ticket = pw.CharField()

        self.db.create_tables([User, RegisteredUser])
        self.model = User
        self.registered_user = RegisteredUser

    def insert(self, user_id: int, user_info: dict, scenario: str = "", step: str = ""):
        """
            Метод вставляет запись в таблицу.
            Возвращает вставленную запись и индикатор новой записи (True если запись новая
            False если запись уже существует)
        :return:
        """
        return self.model.get_or_create(user_id=user_id,
                                        defaults={'first_name': user_info['first_name'],
                                                  'last_name': user_info['last_name'],
                                                  'full_name': "",
                                                  'email': "",
                                                  'city': user_info['city_title'],
                                                  'photo': user_info['photo'],
                                                  'scenario_name': scenario, 'step_name': step
                                                  })

    def select(self, user_id: int):
        """
            Ищет в таблице пользователя с указанным ID
            В случае успеха возвращает его запись
        :param user_id: ID полтзователя
        :return:
        """

        try:
            self.record = self.model.get(user_id=user_id)
            return self.record
        except pw.DoesNotExist:
            return False

    def delete(self, user_id: int):
        """
            Метод удаляет запись из таблицы
        :return:
        """
        query = self.model.delete().where(self.model.user_id == user_id)
        query.execute()

    def update(self):
        """
            Метод обновляет запись в таблице
        :return:
        """
        pass

    def register_user(self, ticket: str):
        """
            Заносит пользователя в таблицу зарегистрированных пользователей
        :return:
        """
        user = self.registered_user()

        user.user_id = self.model.user_id
        user.first_name = self.model.first_name
        user.last_name = self.model.last_name
        user.full_name = self.model.full_name
        user.email = self.model.email
        user.city = self.model.city
        user.photo = self.model.photo
        user.ticket = ticket

        user.save()

    def info(self):
        """
            Возвращает запись ввиде словаря
        :return: dict
        """
        if self.record:
            return {'user_id': self.record.user_id,
                    'first_name': self.record.first_name,
                    'last_name': self.record.last_name,
                    'full_name': self.record.full_name,
                    'email': self.record.email,
                    'city': self.record.city,
                    'photo': self.record.photo,
                    'scenario_name': self.record.scenario_name,
                    'step_name': self.record.step_name,
                    }
        else:
            return False


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
    user_states: UserInformation

    def __init__(self, group, token):
        self.group_id = group
        self.group_title = ''
        self.token = token

        self.vk = vk_api.VkApi(token=self.token)
        self.long_poll = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()
        self.group_title = self.get_group_title()
        self.user_states = UserInformation()

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

        sender = self.api.users.get(user_ids=user_id, fields='city,nickname,photo_200,crop_photo')

        sender_info = {
            'first_name': sender[0]['first_name'],
            'last_name': sender[0]['last_name'],
            'nickname': sender[0]['nickname'],
            'city_title': sender[0]['city']['title'],
            'photo': sender[0]['photo_200'],
            'crop_photo': sender[0]['crop_photo']
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

    def send_message_to_user(self, user_id: int, message: str = None, attachment: str = None):
        """
            Метод посылает сообщение message пользователю с user_id
        :param user_id: ID пользователя
        :param message: Сообщение
        :param attachment: Аттачмент
        :return: None
        """

        return self.api.messages.send(message=message,
                                      random_id=random.randint(0, 2 ** 20),
                                      user_id=user_id,
                                      attachment=attachment)

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

    def upload_image(self, image: str) -> str:
        """
            Загружает изображение на сервер и возвращает ссылку на него.
        :return: str
        """
        attachment = None

        name = image.split('\\')[-1]
        path = os.getcwd()
        file = os.path.join(path, image)
        if os.path.isfile(file):
            file_handler = open(file=file, mode='rb')
            url = self.api.photos.getMessagesUploadServer()['upload_url']
            response = requests.post(url=url, files={'photo': (name, file_handler, f'image/{name.split(".")[-1]}')})
            image_data = self.api.photos.saveMessagesPhoto(**response.json())
            attachment = f'photo{image_data[0]["owner_id"]}_{image_data[0]["id"]}'

        return attachment

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
        attachment: Optional[str] = None

        user_info = self.get_user_info(user_id=user_id)

        record = self.user_states.select(user_id=user_id)

        if record:
            text_to_send = self.continue_scenario(record, text=event.object.text)
        else:
            # Ищем в интентах введенный пользователем текст
            for intent in INTENTS:
                self.logger.debug(f'Проверяем на совпадение с {intent}')
                if any(token in text.lower() for token in intent['tokens']):
                    if intent['answer']:
                        text_to_send = intent['answer'].format(**{'first_name': user_info['first_name'],
                                                                  'last_name': user_info['last_name']})
                    else:
                        text_to_send = self.start_scenario(user_id, user_info, intent['scenario'])

                    if intent['image']:
                        attachment = self.upload_image(image=intent['image'])

                    break
            else:
                text_to_send = DEFAULT_ANSWER
                attachment = self.upload_image(DEFAULT_IMAGE)

        self.send_message_to_user(message=text_to_send, user_id=user_id, attachment=attachment)

    def start_scenario(self, user_id, user_info, scenario_name):
        """
            Start scenario
        :param user_id: Идентификатор пользователя
        :param user_info: Информация о пользователе
        :param scenario_name: Наименование сценария
        :return: Текст для отправки пользователю
        """
        scenario = SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']

        record, _ = self.user_states.insert(user_id=user_id,
                                            user_info=user_info,
                                            scenario=scenario_name,
                                            step=first_step)

        # self.user_states[user_id] = UserState(scenario_name=scenario_name, step_name=first_step)

        return text_to_send.format(**{'first_name': record.first_name, 'last_name': record.last_name})

    def continue_scenario(self, record: pw.Model, text):
        """
            Продолжение сценария
        :param record: ID пользователя
        :param text: Текст полученный от пользователя
        :return: text_to_send - Текст для отправки пользователю
        """
        steps = SCENARIOS[record.scenario_name]['steps']
        step = steps[record.step_name]

        try:
            handler = getattr(handlers, step['handler'])
        except AttributeError as exc:
            self.logger.info(f'Неправильный хандлер при обработке шага {record.step_name}, {exc}')
            return 'Возникла ошибка при обработке входных данных. Приносим свои извинения.'

        if handler(text=text, context=record):
            next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**self.user_states.info())
            if next_step['next_step']:
                record.step_name = step['next_step']
            else:
                self.logger.info('Зарегистрирован пользователь: {full_name} <{email}>'.format(
                    **self.user_states.info()))

                attachment = self.upload_image(self.create_ticket())

                self.send_message_to_user(message='Ваш билет, он же бейджик:',
                                          user_id=self.user_states.info()['user_id'],
                                          attachment=attachment
                                          )
                self.user_states.register_user(attachment)
                self.user_states.delete(user_id=record.user_id)
        else:
            text_to_send = step['failure_text'].format(**self.user_states.info())

        record.save()

        return text_to_send

    def create_ticket(self):
        """
            Метод создает билет для пользователя
        :return:
        """

        name = self.user_states.info()['full_name']
        email = self.user_states.info()['email']

        photo = requests.get(url=self.user_states.info()['photo'])
        with open('photo.jpg', 'wb') as file:
            file.write(photo.content)

        ticket = SkillBoxTicket()
        ticket.values('photo.jpg', name, email)
        ticket.placeholder_replacement()
        ticket.template.enhance()
        filename = f'images\\{self.user_states.info()["user_id"]}.jpg'
        ticket.template.save_to(filename)

        return filename


class SkillBoxTicket:
    """
        Класс создает билет для посещения конференции Skillbox
    """
    template: ImageFiller
    _photo: ImageFillerPlaceholder
    _name: ImageFillerPlaceholder
    _email: ImageFillerPlaceholder

    def __init__(self):
        path_to_template = 'images\\ticket.jpg'
        self.template = ImageFiller(path_to_template)

        self.photo = self.template.placeholder('photo')
        self.photo.type = 'image'

        self.name = self.template.placeholder('first_name')

        self.name.font.font_face = 5
        self.name.font.font_scale = 2
        self.name.font.font_color = (255, 255, 255)
        self.name.font.font_thickness = 2

        self.email = self.template.placeholder('last_name')

        self.email.font.font_face = 5
        self.email.font.font_scale = 1
        self.email.font.font_color = (255, 255, 255)
        self.email.font.font_thickness = 2

    @property
    def photo(self) -> ImageFillerPlaceholder:
        """
            Плейсхолдер для фотографии
        :return: self._photo
        """
        return self._photo

    @photo.setter
    def photo(self, placeholder: ImageFillerPlaceholder):
        self._photo = placeholder

    @property
    def name(self) -> ImageFillerPlaceholder:
        """
            Плейсхолдер для имени
        :return: self._name
        """
        return self._name

    @name.setter
    def name(self, placeholder: ImageFillerPlaceholder):
        self._name = placeholder

    @property
    def email(self) -> ImageFillerPlaceholder:
        """
            Плейсхолдер для фамилии
        :return: self._email
        """
        return self._email

    @email.setter
    def email(self, placeholder: ImageFillerPlaceholder):
        self._email = placeholder

    def values(self, foto: str, name: str, email: str):
        """
            Устанавливает значения плейсхолдеров
        :param foto: Имя файла с картинкой
        :param name: Имя пользователя
        :param email: Фамилия пользователя
        :return: None
        """
        self.photo.value = foto
        self.name.value = name
        self.email.value = email
        self.placeholder_replacement()

    def placeholder_replacement(self):
        """
            Размещает плейсхолдеры с учетом их размеров
        :return:
        """
        self.photo.place = (int(self.template.size()[0]/2-self.photo.size()[0]/2),
                            int(self.template.size()[1]/2-self.photo.size()[1]/2))

        self.name.place = (int(self.template.size()[1]/2-self.name.size()[0][0]/2), 550)

        self.email.place = (int(self.template.size()[1]/2-self.email.size()[0][0]/2), 600)

    def display(self):
        """
            Выводит на экран полученный билет.
        :return:
        """
        self.template.enhance()
        self.template.display()


def main():
    """
        Функция вызывается в случае непосредстевнного запуска скрипта.
    :return:
    """
    bot = EchoBot(GROUP_ID, token=TOKEN)
    bot.run()


if __name__ == '__main__':
    main()
