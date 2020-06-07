from django.shortcuts import render
from rest_framework import viewsets
from . import logging
from registro.models import *
from registro.serializers import *

# ViewSets define the view behavior.
class ProjectViewSet(viewsets.ModelViewSet):
    #logger.debug("Into view")
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ModelViewSet):
    #logger.debug("Into view")
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# ViewSets define the view behavior.
class CompanyViewSet(viewsets.ModelViewSet):
    #logger.debug("Into view")
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

# ViewSets define the view behavior.
class WorkedHoursViewSet(viewsets.ModelViewSet):
    #logger.debug("Into view")
    queryset = WorkedHours.objects.all()
    serializer_class = WorkedHoursSerializer
