from django.contrib import admin
from django.urls import path, include

from business import views

urlpatterns = [
    path("create/", views.create_business, name="create-business"),
    path("list/", views.list_business, name="list-business"),
    path("update/<str:b_id>", views.update_business, name="update-business")
]