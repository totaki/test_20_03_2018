import asyncio
from unittest import TestCase

from aiomysql.sa import create_engine, Engine
from preprocess import words_dict_encrypt_and_hashed, words_dict_decrypt
from managers import WordsManager
from crypto import Crypto
from config import get_connection


TEST_WORDS = {
    'word': 2,
    'python': 5,
    'develop': 6
}


async def get_engine(loop):
    return await create_engine(loop=loop, autocommit=True, **get_connection())


async def delete_records(engine: Engine):
    async with engine.acquire() as conn:
        await conn.execute('DELETE FROM words;')


class WordsManagerTest(TestCase):

    __manager: WordsManager
    __engine: Engine

    @classmethod
    def __run(cls, coro):
        return cls.__loop.run_until_complete(coro)

    @classmethod
    def setUpClass(cls):
        cls.__crypto = Crypto()
        cls.__loop = asyncio.get_event_loop()
        cls.__engine = cls.__run(get_engine(cls.__loop))
        cls.__run(delete_records(cls.__engine))
        cls.__manager = WordsManager(cls.__engine)

    def test_create_and_get_records(self):
        encrypted = words_dict_encrypt_and_hashed(TEST_WORDS, self.__crypto)
        self.__run(self.__manager.upgrade_records(encrypted))
        getting_words = self.__run(self.__manager.get_records())
        decrypted = words_dict_decrypt(getting_words, self.__crypto)

        for item in decrypted:
            word = item['word']
            self.assertIn(word, TEST_WORDS.keys())
            self.assertEqual(item['count'], TEST_WORDS[word])

        # Update existing
        self.__run(self.__manager.upgrade_records(encrypted))
        getting_words = self.__run(self.__manager.get_records())
        decrypted = words_dict_decrypt(getting_words, self.__crypto)
        for item in decrypted:
            word = item['word']
            self.assertIn(word, TEST_WORDS.keys())
            self.assertEqual(item['count'], TEST_WORDS[word] * 2)

    @classmethod
    def tearDownClass(cls):
        cls.__run(delete_records(cls.__engine))
        cls.__run(cls.__manager.stop())
