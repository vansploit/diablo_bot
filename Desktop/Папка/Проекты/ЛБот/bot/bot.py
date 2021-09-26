import os
import vk_api
from loguru import logger
from random import getrandbits
from vk_api.utils import get_random_id
from messageHandler import create_answer
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

class Bot():

    def __init__(self):

        self.version = "5.130"
        self.vk_session = vk_api.VkApi(token=os.getenv('TOKEN'), api_version = self.version)
        self.longpoll = VkBotLongPoll(self.vk_session, 203284091)
        self.vk = self.vk_session.get_api()


    ### Init Logger ###
    def error_only(self, record):
        return record["level"].name == "ERROR"

    def logger_init(self):
        # Настройка Error логов
        logger.add('logs/log_ERROR.log', filter=self.error_only,
                   format="{time:YYYY-MM-DD в HH:mm:ss}|{level}|{message}", retention="3 days")
        # Настройка Info логов
        logger.add('logs/log_INFO.log',
                   format="{time:YYYY-MM-DD at HH:mm:ss}|{level}|{message}", retention="3 days")

        logger.info("Логгер запущен!")
    ### End ###


    # Функция определяет от кого сообщение(пользователь, чат)
    def whereFrom(self, peer_id):

        if peer_id < 0:
            return 'group'

        elif peer_id < 2000000000:
            return 'user', peer_id

        else:
            return 'chat', peer_id - 2000000000


    def send_message(self, peer_id, text):

        self.from_is, self._id = self.whereFrom(peer_id)

        if self.from_is == 'user':
            self.result = self.vk.messages.send(
                        user_id = self._id,
                        message = text,
                        random_id = getrandbits(64)
                        )

        elif from_is == 'chat':
            self.result = self.vk.messages.send(
                        chat_id = self._id,
                        message = text,
                        random_id = getrandbits(64)
                        )

    def run(self):

        self.logger_init()

        logger.info("Запускаю longpoll...")
        for self.event in self.longpoll.listen():

            if self.event.type == VkBotEventType.MESSAGE_NEW and self.event.raw["object"]["message"]:

                # msg_info [0] - id message; [1] - peer id; [2] - message text; [3] - from id
                self.msg_info = [self.event.raw["object"]["message"][i] \
                                 for i in ("id", "peer_id", "text", "from_id")]

                # записываем в логи id, user_id, text
                logger.info(f"message_id: {self.msg_info[0]} | peer_id: {self.msg_info[1]} | text: {self.msg_info[2]}")

                self.message = create_answer(self.msg_info)

                if self.message != 'Error':

                    self.send_result = self.send_message(self.msg_info[1], self.message)
                    logger.info(f'Результат отправки: {self.send_result} | Текст сообщения: {self.message}')

                else:

                    logger.error(f'message прислал error: {self.message}')
                
