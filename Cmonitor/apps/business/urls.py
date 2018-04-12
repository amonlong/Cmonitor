from django.conf.urls import url
from apps.business import views

urlpatterns = [
    url('flowLoan/', views.flowLoan_view, name='loan'),
    url('flowDelayRate/', views.flowDelayRate_view, name='delayRate'),
    url('api/v1/business/', views.searchBussiness),
]