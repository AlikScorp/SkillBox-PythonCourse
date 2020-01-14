"""
    Скрипт для тестирования ЭхоБота
"""

from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from vk_api.bot_longpoll import VkBotMessageEvent

from bot import EchoBot


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
        event = VkBotMessageEvent(raw=self.RAW_EVENT)
        send_mock = Mock()
        get_user_info = Mock()

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll'):
                bot = EchoBot('', '')
                bot.api = Mock()
                bot.get_user_info = Mock(return_value=self.SENDER_INFO)
                bot.api.users.get = get_user_info
                bot.api.messages.send = send_mock

                message = bot.get_greetings(user=self.SENDER_INFO)
                message = message + f"К сожалению, на ваше сообщение \"{self.RAW_EVENT['object']['text']}\" " \
                                    f"мне пока нечего ответить."

                bot.on_event(event=event)

                send_mock.assert_called_once_with(
                    message=message,
                    random_id=ANY,
                    peer_id=self.RAW_EVENT['object']['peer_id']
                )
