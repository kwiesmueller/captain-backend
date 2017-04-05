import base64
import random
import string

from django.conf import settings

from Crypto.Cipher import AES


class EncryptionFormattingManager(object):
    """
    takes care of formatting a string in a way, that makes it encryptable and deformating it back to it's initial value
    """
    @staticmethod
    def format(unformatted_string):
        """
        brings the given string into a encryptable format

        :param unformatted_string: string to format
        :type unformatted_string: str
        :return: formatted string
        :rtype: str
        """
        length = len(unformatted_string)
        return unformatted_string.ljust(length + 16 - length % 16)

    @staticmethod
    def deformat(formatted_string):
        """
        returns the initial value of the given string

        :param formatted_string: the string, to get the initial value from
        :type formatted_string: str
        :return: unformatted string
        :rtype: str
        """
        return formatted_string.strip()


class EncryptionManager(object):
    """
    takes care of encrypting and decrypting a string and converting it from/to base64
    """
    CIPHER = AES.new(settings.SECRET_KEY[:32])

    @staticmethod
    def encrypt(plain_text):
        """
        encrypts the given plain text

        :param plain_text: the text to encrypt
        :type plain_text: str
        :return: the encrypted text
        :rtype: str
        """
        return base64.b64encode(EncryptionManager.CIPHER.encrypt(EncryptionFormattingManager.format(plain_text)))

    @staticmethod
    def decrypt(encrypted_text):
        """
        decrypts the given encrypted text

        :param encrypted_text: the encrypted text, which should be decrypted
        :type encrypted_text: str
        :return: decrypted text
        :rtype: str
        """
        return EncryptionFormattingManager.deformat(EncryptionManager.CIPHER.decrypt(base64.b64decode(encrypted_text)))


class EncryptedString(object):
    """
    takes a encrypted string, which can then be decrypted on demand
    """
    def __init__(self, encrypted_string):
        """
        initializes a EncryptedString
        :param encrypted_string: encrypted string data
        :type encrypted_string: str
        """
        self.encrypted_string = encrypted_string

    def decrypt(self):
        """
        decrypts encrypted string
        :return: decrypted string
        :rtype: str
        """
        return EncryptionManager.decrypt(self.encrypted_string)


class EncryptedDict(object):
    """
    wraps a dict key value store with encrypted values
    """
    def __init__(self, base_dict):
        """
        initializes a EncryptedDict from a dict

        :param base_dict: the dict, whoms values should be encrypted
        :type base_dict: dict
        """
        self.encrypted_dict = {}

        for key in base_dict:
            self.encrypted_dict[key] = EncryptedString(base_dict[key])

    def get(self, key):
        """
        gets and decrypts the value for the given key. Returns None in case, there is no entry for the given key.

        :param key: key for the value
        :type key: str
        :return: decrypted value
        :rtype: str
        """
        encrypted_string = self.encrypted_dict.get(key, None)

        if encrypted_string:
            return encrypted_string.decrypt()

        return None

    def set(self, key, value):
        """
        decrypts the value and sets it

        :param key: key for the value
        :type key: str
        :param value: the value to be encrypted
        :type value: str
        :return: decrypted value
        :rtype: str
        """
        self.encrypted_dict[key] = EncryptedString(EncryptionManager.encrypt(value))

        return value

    @staticmethod
    def generate():
        """
        generates a random password

        :return: generated password
        """
        return ''.join(
            random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32)
        )

    def generate_and_set(self, key):
        """
        generates a new random value for the give key, and encrypts it

        :param key: key for the value
        :type key: str
        :return: decrypted value
        :rtype: str
        """
        return self.set(key, self.generate())



    def get_or_generate(self, key):
        """
        gets and decrypts the value for the given key. Generates a new password, in case no password was found for
        the given key

        :param key: key for the value
        :type key: str
        :return: decrypted value
        :rtype: str
        """
        decrypted_string = self.get(key)

        if decrypted_string:
            return decrypted_string
        else:
            return self.generate_and_set(key)
