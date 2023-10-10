from __future__ import annotations

from django.urls import path

from tests import views

urlpatterns = [
    path("", views.index),
    path("async/", views.async_),
    path("decorated/<slug:slug>/", views.decorated),
    path("decorated-with-conf/<slug:slug>/", views.decorated_with_conf),
    path("async-decorated/<slug:slug>/", views.async_decorated),
    path("async-decorated-with-conf/<slug:slug>/", views.async_decorated_with_conf),
    path("unauthorized/", views.unauthorized),
    path("delete-enabled/", views.delete_enabled_attribute),
]
