from django.conf.urls import url
from apps.index import views

urlpatterns = [
    url('', views.index_view, name='index'),
    url('dashboard/', views.searchDashboard),
]