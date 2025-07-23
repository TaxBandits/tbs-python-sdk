# django imports
from django.shortcuts import render

# folder imports
from .utils import business_form_serializer
from project.utils import do_alerts
from project.api_services import Business


def create_business(request):

    # this is return context used to send data to UI
    context = {
        'form_data': {},
        'api_res': {}
    }

    if request.method == 'POST':

        # processing the request.POST data object to json format
        business_form = business_form_serializer(request.POST)
        # sending business form to UI, so that user can verify after business values created with
        context['form_data'].update(business_form)

        # note: b_obj is Business class object
        b_obj = Business()
        token = b_obj.get_auth_token()
        # create business by sending that business_form json to create_business method
        res_json = b_obj.create_business(jwt_token=token, business_form=business_form)
        # sending create business api response to UI there response will shown in popup
        context['api_res'].update(res_json)

    return render(request, 'pages/business/create-business.html', context)

def list_business(request):

    context = {}

    # note: b_obj is Business class object
    b_obj = Business()
    token = b_obj.get_auth_token()
    # list_business method will get the list of business using token and its associated user 
    res_json = b_obj.list_business(jwt_token=token)
    # sending the list of business to UI
    context.update(res_json)
    
    do_alerts(request, res_json)        # it check for the error messages and show it in UI

    return render(request, 'pages/business/list-business.html', context)
