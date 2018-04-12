from django.conf.urls import url
from apps.index import views

urlpatterns = [
    url('index/', views.index_view, name='index'),
    url('api/v1/dashboard/', views.searchDashboard),
]