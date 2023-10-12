from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_business, name="create-business"),
    path("list/", views.list_business, name="list-business"),
]

