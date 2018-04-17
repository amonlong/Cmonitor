from django.conf.urls import url
from apps.product import views

urlpatterns = [
    url('api/v1/product/', views.searchProduct),
]