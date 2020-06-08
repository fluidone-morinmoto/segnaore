from django.shortcuts import render
from rest_framework import viewsets
from . import logger
from registro.models import *
from registro.serializers import *

# ViewSets define the view behavior.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# ViewSets define the view behavior.
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

# ViewSets define the view behavior.
class WorkedHoursViewSet(viewsets.ModelViewSet):
    queryset = WorkedHours.objects.all()
    serializer_class = WorkedHoursSerializer
