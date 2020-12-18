# -*- coding: utf-8 -*-

from django.urls import path, include

app_name = 'vans'
urlpatterns = [
    path('v1/', include('vans.api.v1.urls', namespace='v1')),
]
