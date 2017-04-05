from rest_framework import routers
from django.conf.urls import url, include
from charts.views import ChartViewSet, RepositoryViewSet
from clusters.views import ClusterViewSet, NamespaceViewSet, DeploymentViewSet

router = routers.DefaultRouter()
router.register(r'repositories', RepositoryViewSet)
router.register(r'charts', ChartViewSet)
router.register(r'clusters', ClusterViewSet)
router.register(r'namespaces', NamespaceViewSet)
router.register(r'deployments', DeploymentViewSet)