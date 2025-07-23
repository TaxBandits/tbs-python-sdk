from django.urls import path

from . import views

urlpatterns = [
    path("create/<b_id>", views.create_w2g, name="create-w2g"),
    path('validate/<b_id>', views.create_w2g, name="validate-w2g"),
    path("update/<b_id>/<sub_id>/<rec_id>", views.update_w2g, name="update-w2g"),
    path("list/<b_id>/<b_name>/<b_tin>", views.list_w2g, name="list-w2g"),
    path("get/<b_id>/<b_name>/<b_tin>/<sub_id>/<rec_id>", views.list_w2g, name="get-w2g"),
]

# note:-
# b_id is business_id
# b_name is business_name
# b_tin is business_tin
# sub_id is submission_id
# rec_id is record_id
