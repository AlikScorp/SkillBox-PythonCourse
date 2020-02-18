"""
    Скрипт для тестирования ЭхоБота
"""
from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch, Mock, ANY

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
        'first_name': 'Альберт',
        'last_name': 'Ишмухамедов',
        'nickname': 'AlikScorp',
        'city_title': 'Ашхабад',
    }

    INPUTS = [
        'Hi!',
        'А когда?',
        'Где будет конференция?',
        'Зарегистрироваться',
        'Альберт',
        'alikscorp@mailru',
        'alikscorp@mail.ru',
    ]

    EXPECTED_OUTPUTS = [
        settings.DEFAULT_ANSWER,
        settings.INTENTS[0]['answer'],
        settings.INTENTS[1]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['failure_text'],
        settings.SCENARIOS['registration']['steps']['step3']['text'].format(name='Альберт', email='alikscorp@mail.ru')
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
                bot.get_group_title = Mock(return_value='Python-разработчик с нуля - Курсовой проект')
                bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []

        for call in send_mock.call_args_list:
            args, kwars = call
            real_outputs.append(kwars['message'])

        assert real_outputs == self.EXPECTED_OUTPUTS
