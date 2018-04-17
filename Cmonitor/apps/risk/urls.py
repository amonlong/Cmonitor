from django.conf.urls import url
from apps.risk import views

urlpatterns = [
    url('passRate/', views.passRate_view, name='passRate'),
    url('overdueRate/', views.overdueRate_view, name='overdueRate'),
    url('api/v1/risk/', views.searchRisk),
]