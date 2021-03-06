"""vans_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import (
    url,
    include,
)
from django.contrib import admin
from django.urls import include, re_path as path

from django.views.static import serve

from vans_api.settings import (
    STATIC_ROOT,
    MEDIA_ROOT,
)
from vans_api.views import index

urlpatterns = [
    path('admin/', admin.site.urls),

    #apps urls
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('common.urls')),
    path('api/', include('vans.api.urls', namespace='api')),

    path('', index, name='index_view'),
]

admin.site.site_header = "Vans Administrator"
