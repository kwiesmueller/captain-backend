from django.db import models

class Repository(models.Model):
    name = models.CharField(max_length=50)
    path = models.URLField()

    class Meta:
        verbose_name = "Repository"
        verbose_name_plural = "Repositories"

    def __unicode__(self):
        return self.name

class Chart(models.Model):
    name = models.CharField(max_length=50)
    version = models.IntegerField()
    author = models.CharField(max_length=50)
    repository = models.ForeignKey(Repository)

    values = models.TextField()

    class Meta:
        verbose_name = "Chart"
        verbose_name_plural = "Charts"

    def __unicode__(self):
        return self.name