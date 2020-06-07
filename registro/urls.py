from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from registro.views import *

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'worked_hours', WorkedHoursViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
