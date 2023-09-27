# django imports
from django.shortcuts import render
from django.contrib import messages

# folder imports
from .utils import business_form_serializer, do_alerts
from project.api_hitters import Business


def home(request):
    return render(request, 'pages/home.html')

def create_business(request):

    # this is return context used to send data to UI
    context = {
        'form_data': {},
        'api_res': {}
    }

    if request.method == 'POST':

        # processing the request.POST data object to json format
        business_form = business_form_serializer(request.POST)
        # sending business form to UI, so that user can verify after business created
        context['form_data'].update(business_form)

        b_obj = Business()
        token = b_obj.get_auth_token()
        # create business by sending that business_form json to create_business method
        res_json = b_obj.create_business(jwt_token=token, business_form=business_form)
        # sending create business api response to UI there response will shown in popup
        context['api_res'].update(res_json)

    return render(request, 'pages/create-business.html', context)

def update_business(request, b_id):

    context = {
        'form_data': {},
        'api_res': {}
    }
    
    if request.method == 'POST':

        # processing the request.POST data object to json format
        business_form = business_form_serializer(request.POST)
        # updating business id to business form its required to update business
        business_form.update({'BusinessId': b_id})
        # sending business form to UI, so that user can verify after business got updated
        context['form_data'].update(business_form)

        b_obj = Business()
        token = b_obj.get_auth_token()
        # update business by sending that business form json to update_business method
        res_json = b_obj.update_business(jwt_token=token, business_form=business_form)
        # sending update business api response to UI there response will shown in popup
        context['api_res'].update(res_json)

    else:
        b_obj = Business()
        token = b_obj.get_auth_token()
        # getting business using business id
        res_json = b_obj.get_business(jwt_token=token, business_id=b_id)
        # sending gotten business to UI for updating purpose
        context['form_data'].update(res_json['Business'])

        do_alerts(request, res_json)    # it check for the error messages and show it in UI

    return render(request, 'pages/update-business.html', context)

def list_business(request):

    context = {}

    b_obj = Business()
    token = b_obj.get_auth_token()
    # list_business method will get the list of business using token and its associated user 
    res_json = b_obj.list_business(jwt_token=token)
    # sending the list of business to UI
    context.update(res_json)
    
    do_alerts(request, res_json)    # it check for the error messages and show it in UI

    return render(request, 'pages/list-business.html', context)
