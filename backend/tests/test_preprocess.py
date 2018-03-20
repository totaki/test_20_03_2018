import random
import preprocess
from crypto import Crypto
from unittest import TestCase

TEST_HTML = './tests/test.html'


def genertate_text():
    words = ['hello', 'world', 'python', 'develop', 'end\n']
    words_count = [5, 6, 10, 3, 2]
    assert len(words) == len(words_count)
    words_dict = dict(zip(words, words_count))

    not_words = [
        f'{random.choice(words)}_{random.randint(0, 100)}'
        for _ in range(10)
    ]

    total_words_array = sum([[w] * c for w, c in zip(words, words_count)], [])
    total_words_array.extend(not_words)
    random.shuffle(total_words_array)
    return words_dict, (' ').join(total_words_array)


class TestPreprocessFlow(TestCase):

    def test_preprocess_flow(self):
        words_dict, text = genertate_text()
        result_words_dict = preprocess.preprocess_text(text)
        for k, v in words_dict.items():
            self.assertEqual(result_words_dict[k], v)

        cr = Crypto()
        encrypted = preprocess.words_dict_encrypt_and_hashed(result_words_dict, cr)
        decrypted = preprocess.words_dict_decrypt(encrypted, cr)
        for item in decrypted:
            word = item['word']
            self.assertIn(word, words_dict.keys())
            self.assertEqual(item['count'], words_dict[word])

        with open(TEST_HTML) as f:
            text = f.read()

        # Next we expect found more 5 unique words in text
        self.assertGreater(len(preprocess.main_preprocess(text)), 5)


