from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.login.urls')),
    url(r'^', include('apps.index.urls')),
    url(r'^', include('apps.userInfo.urls')),
    url(r'^', include('apps.business.urls')), 
    url(r'^', include('apps.risk.urls')), 
    url(r'^', include('apps.product.urls')), 
    url(r'^', include('apps.record.urls')), 
]
