from django.contrib import admin
from .models import Cluster, Namespace, Deployment

admin.site.register(Cluster)
admin.site.register(Namespace)
admin.site.register(Deployment)