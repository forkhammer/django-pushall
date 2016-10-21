#-*- coding: utf-8 -*-
from django.conf.urls import url
from .views import CallbackView


urlpatterns = [
    url(r'^callback$', CallbackView.as_view()),
]