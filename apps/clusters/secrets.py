from django.db import models
from django.conf import settings
from base.encrypted_dict import EncryptionManager, EncryptedDict, EncryptedString
from base.models import LookupDict

class EncryptedField(models.BinaryField):
    """
    custom field which encrypts a string before saving
    """
    def pre_save(self, model_instance, add):
        if add or SecretStorage.objects.get(pk=model_instance.id).value != model_instance.value:
            model_instance.value = EncryptionManager.encrypt(model_instance.value)

        return super(EncryptedField, self).pre_save(model_instance, add)


class SecretStorage(models.Model):
    class SecretStorageEncryptedDict(EncryptedDict):
        def __init__(self, deployment, secret_type=None):
            """
            initializes a EncryptedDict from a Deployment

            :param deployment: deployment to retrieve the passwords from
            :type deployment: Deployment
            """
            if not secret_type:
                secret_type = SecretStorage.SECRET_TYPES_LOOKUP_DICT.get('DEFAULT')

            self.deployment = deployment
            secret_storage_dict = {}

            for entry in self.deployment.secret_storage.filter(secret_type=secret_type):
                secret_storage_dict[entry.key] = entry.value

            super(SecretStorage.SecretStorageEncryptedDict, self).__init__(secret_storage_dict)

        def set(self, key, value, secret_type=None):
            """
            decrypts the value and sets it

            :param key: key for the value
            :type key: str
            :param value: the value to be encrypted
            :type value: str
            :param secret_type: optional provide the password type the password storage object is saved with
            :type secret_type: int
            :return: decrypted value
            :rtype: str
            """
            if not secret_type:
                secret_type = SecretStorage.SECRET_TYPES_LOOKUP_DICT.get('DEFAULT')

            secret_storage = SecretStorage.objects.get_or_create(
                key=key,
                deployment=self.deployment,
                secret_type=secret_type
            )[0]
            secret_storage.value = value
            secret_storage.save()

            self.encrypted_dict[key] = EncryptedString(secret_storage.value)

            return value


    SECRET_TYPES = (
        (0, 'DEFAULT'),
    )

    SECRET_TYPES_LOOKUP_DICT = LookupDict.factory(SECRET_TYPES)

    deployment = models.ForeignKey('Deployment', related_name='secret_storage')
    key = models.CharField(max_length=255)
    value = EncryptedField()
    secret_type = models.IntegerField(choices=SECRET_TYPES, default=SECRET_TYPES_LOOKUP_DICT.get('DEFAULT'))

