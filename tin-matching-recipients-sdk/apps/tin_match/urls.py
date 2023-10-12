from django.urls import path

from . import views

urlpatterns = [
    path("request/<b_id>/<b_name>/<b_tin>", views.tin_match_request, name="tin-match-request"),
    path("list/<b_id>/<b_name>/<b_tin>", views.list_request_records, name="list-request-records"),
    path("get/<b_id>/<b_name>/<b_tin>/<sub_id>/<rec_id>", views.list_request_records, name="get-request")
]

# note:-
# b_id is business_id
# b_name is business_name
# b_tin is business_tin
# sub_id is submission_id
# rec_id is record_id