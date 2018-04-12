from django.conf.urls import url
from apps.userInfo import views

urlpatterns = [
    url('userIncrease/', views.userIncrease_view, name='userIncrease'),
    url('api/v1/userInfo/', views.searchUserInfo),
]