from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from charts.views import ChartViewSet, RepositoryViewSet

router = routers.DefaultRouter()
router.register(r'repositories', RepositoryViewSet)
router.register(r'charts', ChartViewSet)

schema_view = get_schema_view(title='Captain API')

urlpatterns = [
    url('^$', schema_view),
    url(r'^', include(router.urls)),
]