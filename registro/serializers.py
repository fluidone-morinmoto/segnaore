from rest_framework import serializers
from registro.models import *
from . import logger


# Serializers define the API representation.
class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'code']

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class CompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name']

class WorkedHoursSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WorkedHours
        fields = [
            'id',
            'from_time',
            'to_time',
            'description',
            'category',
            'category_id',
            'project',
            'project_id'
        ]
