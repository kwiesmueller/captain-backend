from django.db import models
from django.conf import settings
from base.encrypted_dict import EncryptionManager, EncryptedDict, EncryptedString

class LookupDict(object):

    @staticmethod
    def factory(tuple_set):
        """
        takes a set of pairwise tuples and generates a dict to lookup keys by value

        :param tuple_set: iterable set of tuples
        :type tuple_set: iterable<tuple>
        :return: dict with value -> key
        :rtype: dict
        """
        lookup_dict = {}

        for entry in tuple_set:
            lookup_dict[entry[1]] = entry[0]

        return lookup_dict
