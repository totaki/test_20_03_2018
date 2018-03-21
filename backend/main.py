import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient, HTTPError
from managers import WordsManager
from crypto import Crypto
from config import get_connection
from preprocess import (
    main_preprocess,
    words_dict_encrypt_and_hashed,
    words_dict_decrypt
)


class WordsHandler(tornado.web.RequestHandler):

    @property
    def manager(self):
        return self.settings['manager']

    @property
    def crypto(self):
        return self.settings['crypto']

    @property
    def client(self):
        return self.settings['client']

    async def get(self):
        words = await self.manager.get_records()
        decrypted = words_dict_decrypt(words, self.crypto)
        total_count_words = sum([i['count'] for i in decrypted])
        self.finish({'data': decrypted, 'total': total_count_words})

    async def post(self):
        url = self.get_body_argument('url', None)
        if not url:
            self.write_error(400)
        try:
            result = await self.client.fetch(url)
            preprocessed_text = main_preprocess(result.body.decode())
            encrypted = words_dict_encrypt_and_hashed(preprocessed_text, self.crypto)
            await self.manager.upgrade_records(encrypted)
            ordered_items = sorted(preprocessed_text.items(), key=lambda i: i[1], reverse=True)[:100]
            self.finish({'data': ordered_items})
        except HTTPError as err:
            self.write_error(err.code)


def create_app(manager, crypto, client):
    return tornado.web.Application([
        (r"/api/words", WordsHandler),
    ], debug=True, manager=manager, crypto=crypto, client=client)


if __name__ == "__main__":
    loop = tornado.ioloop.IOLoop.current()
    words_manager = loop.run_sync(
        lambda: WordsManager.create(loop=loop.asyncio_loop, **get_connection()))
    application = create_app(words_manager, Crypto(), AsyncHTTPClient())
    application.listen(8888)
    try:
        loop.start()
    except KeyboardInterrupt:
        print('Stop engine')
        loop.run_sync(lambda: application.settings['manager'].stop())
