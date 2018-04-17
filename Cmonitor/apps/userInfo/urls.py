from django.conf.urls import url
from apps.userInfo import views

urlpatterns = [
    url('userIncrease/', views.userIncrease_view, name='userIncrease'),
    url('userAge/', views.userAge_view, name='userAge'),
    url('api/v1/userInfo/', views.searchUserInfo),
]