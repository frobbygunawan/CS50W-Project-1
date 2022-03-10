from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title"),
    path("search/", views.search, name="search"),
    path("new_entry/", views.new_entry, name="new_entry"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random_entry/", views.random_entry, name="random_entry")
]
