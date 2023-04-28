from __future__ import annotations

from django.urls import path

from tests import views

urlpatterns = [
    path("", views.index),
    path("async/", views.async_),
    path("unauthorized/", views.unauthorized),
    path("delete-enabled/", views.delete_enabled_attribute),
]
