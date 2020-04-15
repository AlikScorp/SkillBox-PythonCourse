"""
    Скрипт для тестирования ЭхоБота
"""
from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch, Mock

from vk_api.bot_longpoll import VkBotMessageEvent

from bot import EchoBot
import settings


class TestEchoBot(TestCase):
    RAW_EVENT = {'type': 'message_new',
                 'object': {'date': 1578982887, 'from_id': 36414847, 'id': 96, 'out': 0, 'peer_id': 36414847,
                            'text': 'Привет, бот!', 'conversation_message_id': 82, 'fwd_messages': [],
                            'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False},
                 'group_id': 187871287, 'event_id': '0b7784ef8099210da19abfcb1fb4937a8d4282aa'}

    SENDER_INFO = {
        'user_id': 36414847,
        'first_name': 'Альберт',
        'last_name': 'Ишмухамедов',
        'nickname': 'Alik Scorp',
        'city_title': 'Ашхабад',
        'photo': 'https://sun9-63.userapi.com/c623316/v623316847/21bed/669NU2Vc7uQ.jpg?ava=1',
        'crop_photo': 'photo.jpg',
    }

    USER_INFO = {'user_id': 36414847,
                 'first_name': 'Альберт',
                 'last_name': 'Ишмухамедов',
                 'full_name': 'Alik Scorp',
                 'email': 'alikscorp@mail.ru',
                 'city': 'Ашхабад',
                 'photo': 'https://sun9-63.userapi.com/c623316/v623316847/21bed/669NU2Vc7uQ.jpg?ava=1',
                 'scenario_name': 'registration',
                 'step_name': 'step2',
                 }

    USER_INFO_FULL = {'first_name': 'Альберт',
                      'last_name': 'Ишмухамедов',
                      'nickname': 'AlikScorp',
                      'city_title': 'Ашхабад',
                      'photo': 'https://sun9-63.userapi.com/c623316/v623316847/21bed/669NU2Vc7uQ.jpg?ava=1',
                      'crop_photo': {'photo': {'id': 359472328, 'album_id': -6, 'owner_id': 36414847,
                                               'sizes': [
                                                   {'type': 'm',
                                                    'url': 'https://sun9-25.userapi.com/c623316/v623316847/'
                                                           '20ad8/6i_tCKq_Y1U.jpg',
                                                    'width': 73,
                                                    'height': 130
                                                    },
                                                   {'type': 'o',
                                                    'url': 'https://sun9-19.userapi.com/c623316/v623316847/'
                                                           '20adc/kM8G3cfCSwQ.jpg',
                                                    'width': 130,
                                                    'height': 231
                                                    },
                                                   {'type': 'p',
                                                    'url': 'https://sun9-10.userapi.com/c623316/v623316847/'
                                                           '20add/jz2qI5-5s4Y.jpg',
                                                    'width': 200,
                                                    'height': 355
                                                    },
                                                   {'type': 'q',
                                                    'url': 'https://sun9-33.userapi.com/c623316/v623316847/'
                                                           '20ade/VyoxYz7QxX8.jpg',
                                                    'width': 320,
                                                    'height': 569
                                                    },
                                                   {'type': 'r',
                                                    'url': 'https://sun9-27.userapi.com/c623316/v623316847/'
                                                           '20adf/7EBFskMN8KA.jpg',
                                                    'width': 510,
                                                    'height': 900
                                                    },
                                                   {'type': 's',
                                                    'url': 'https://sun9-42.userapi.com/c623316/v623316847/'
                                                           '20ad7/cBo9glVeedU.jpg',
                                                    'width': 42,
                                                    'height': 75},
                                                   {'type': 'x',
                                                    'url': 'https://sun9-30.userapi.com/c623316/v623316847/'
                                                           '20ad9/nt5XKr0Td1E.jpg',
                                                    'width': 340,
                                                    'height': 604},
                                                   {'type': 'y',
                                                    'url': 'https://sun9-9.userapi.com/c623316/v623316847/'
                                                           '20ada/pwSGitVyToY.jpg',
                                                    'width': 454,
                                                    'height': 807},
                                                   {'type': 'z',
                                                    'url': 'https://sun9-53.userapi.com/c623316/v623316847/'
                                                           '20adb/Zk7kVM27iWI.jpg',
                                                    'width': 576,
                                                    'height': 1024}],
                                               'text': '',
                                               'date': 1426496424,
                                               'lat': 37.925982,
                                               'long': 58.399636,
                                               'post_id': 70},
                                     'crop': {'x': 3.82, 'y': 2.15, 'x2': 92.19, 'y2': 95.61},
                                     'rect': {'x': 0.0, 'y': 7.11, 'x2': 100.0, 'y2': 60.29}}
                      }

    INPUTS = [
        'Hi!',
        'А когда?',
        'Где будет конференция?',
        'Зарегистрироваться',
        'Alik Scorp',
        'alikscorp@mailru',
        'alikscorp@mail.ru',
    ]

    EXPECTED_OUTPUTS = [
        settings.DEFAULT_ANSWER,
        settings.INTENTS[0]['answer'],
        settings.INTENTS[1]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'].format(first_name=USER_INFO_FULL['first_name'],
                                                                            last_name=USER_INFO_FULL['last_name']),
        settings.SCENARIOS['registration']['steps']['step2']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['failure_text'],
        'Ваш билет, он же бейджик:',
        settings.SCENARIOS['registration']['steps']['step3']['text'].format(full_name='Alik Scorp',
                                                                            email='alikscorp@mail.ru')
    ]

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = EchoBot('', '')
                bot.on_event = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(event=obj)
                self.assertEqual(bot.on_event.call_count,  count, 'Метод on_event не вызывался нужное количество раз!')

    def test_on_event(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['text'] = input_text
            events.append(VkBotMessageEvent(raw=event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
                bot = EchoBot('', '')
                bot.api = api_mock
                bot.get_user_info = Mock(return_value=self.USER_INFO_FULL)
                bot.upload_image = Mock(return_value=f'{self.USER_INFO["user_id"]}.jpg')
                bot.get_group_title = Mock(return_value='Python-разработчик с нуля - Курсовой проект')
                bot.run()

        assert send_mock.call_count == len(self.INPUTS)+1

        real_outputs = []

        for call in send_mock.call_args_list:
            args, kwars = call
            real_outputs.append(kwars['message'])

        assert real_outputs == self.EXPECTED_OUTPUTS
