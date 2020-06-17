from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from registro import views

api_prefix = "v1"

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'v1/projects', views.ProjectViewSet)
router.register(r'v1/categories', views.CategoryViewSet)
router.register(r'v1/companies', views.CompanyViewSet)
router.register(r'v1/worked_hours', views.WorkedHoursViewSet)


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
    url(r'^manage/companies', views.manageCompanies, name='manage_companies'),
    url(r'^manage/categories', views.manageCategories, name='manage_categories'),
    url(r'^manage/projects', views.manageProjects, name='manage_projects'),
]
