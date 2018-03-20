import hashlib
import base64
from bs4 import BeautifulSoup
from collections import Counter
from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from crypto import Crypto


def preprocess_text(text: str) -> Dict[str, int]:
    array = text.split(' ')
    filtered = filter(lambda s: s.strip().isalpha(), array)
    c = Counter(filtered)
    return dict(c)


def words_dict_encrypt_and_hashed(words: dict, crypto: 'Crypto') -> List[dict]:
    return [{
        'hash': hashlib.sha256(k.encode()).hexdigest(),
        'word': base64.b64encode(crypto.encrypt(k)),
        'count': v
    } for k, v in words.items()]


def words_dict_decrypt(words: List[dict], crypto: 'Crypto') -> List[dict]:
    for item in words:
        item['word'] = crypto.decrypt(base64.b64decode(item['word']))
    return words


def get_text(text: str) -> str:
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()


def main_preprocess(text: str) -> Dict[str, int]:
    parsed_text = get_text(text)
    return preprocess_text(parsed_text)
