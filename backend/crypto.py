from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding


DEFAULT_PEM = './assets/private.pem'
DEFAULT_PADDING = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None
)


class Crypto:

    pem_file = DEFAULT_PEM

    def __init__(self, pem_file=None):
        self._pem_file = pem_file or DEFAULT_PEM
        with open(self.pem_file, "rb") as key_file:
            self._private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

    @property
    def _public_key(self):
        return self._private_key.public_key()

    def encrypt(self, text):
        return self._public_key.encrypt(text.encode(), DEFAULT_PADDING)

    def decrypt(self, text):
        return self._private_key.decrypt(text, DEFAULT_PADDING).decode()


if __name__ == '__main__':
    import os
    if os.path.isfile(DEFAULT_PEM):
        print('Private pem key is exists delete before generate new')
    else:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(DEFAULT_PEM, 'wb') as f:
            f.write(pem)

    # Test encryption
    test_text = 'Test text'
    crypto = Crypto()

    ciphertext = crypto.encrypt(test_text)
    plaintext = crypto.decrypt(ciphertext)
    assert test_text == plaintext
    print("Test success")
