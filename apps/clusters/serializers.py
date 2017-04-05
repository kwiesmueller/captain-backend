from rest_framework import serializers
from .models import Cluster, Namespace, Deployment

class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = '__all__'

class NamespaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Namespace
        fields = '__all__'

class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployment
        fields = '__all__'