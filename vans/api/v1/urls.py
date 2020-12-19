# -*- coding: utf-8 -*-

from django.urls import path

from vans.api.v1.views import VansView, VanView

app_name = 'vans'
urlpatterns = [
    path(
        'vans/',
        VansView.as_view(),
        name='vans',
    ),
    path(
        'vans/<str:uuid>/',
        VanView.as_view(),
        name='van-detail',
    ),
]
