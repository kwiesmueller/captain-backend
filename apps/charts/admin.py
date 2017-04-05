from django.contrib import admin
from .models import Repository, Chart

admin.site.register(Repository)
admin.site.register(Chart)