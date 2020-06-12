from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from registro import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'worked_hours', views.WorkedHoursViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate,
        name='activate'
    ),
    url(r'^home/$', views.home, name='home'),
    url(r'^index/$', views.index, name='index'),
]
