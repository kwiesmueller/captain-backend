from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from charts.models import Chart
from .secrets import *

class Cluster(models.Model):
    name = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()

    class Meta:
        verbose_name = "Cluster"
        verbose_name_plural = "Clusters"

    def __unicode__(self):
        return self.name

class Namespace(models.Model):
    name = models.CharField(max_length=50)
    public = models.BooleanField(default=False)
    cluster = models.ForeignKey(Cluster)
    owner = models.ForeignKey(User, editable=True)

    class Meta:
        verbose_name = "Namespace"
        verbose_name_plural = "Namespaces"

    def __unicode__(self):
        return self.name

class Deployment(models.Model):
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(User, editable=True)
    chart = models.ForeignKey(Chart)
    version = models.IntegerField()
    namespace = models.ForeignKey(Namespace)
    values = models.TextField()

    @property
    def secrets(self):
        """
        :return: key value store with all secrets related to this instance. Values are still encrypted and have to
        be decrypted by calling secrets.get('key'), when needed
        :rtype: EncryptedDict>
        """
        return self.get_secrets()

    def get_secrets(self, secret_type=SecretStorage.SECRET_TYPES_LOOKUP_DICT.get('DEFAULT')):
        return SecretStorage.SecretStorageEncryptedDict(self, secret_type)