# django imports
from django.shortcuts import render

# folder imports
from .utils import tin_match_request_form_serializer
from project.api_services import TinMatchReq
from project.utils import do_alerts


def tin_match_request(request, b_id, b_name, b_tin):

    # this is return context used to send data to UI
    context = {
        "business_id": b_id,
        "business_name": b_name,
        "business_tin": b_tin,
        "form_data": {},
        "api_res": {}
    }

    if request.method == 'POST':
        # processing the request.POST data object to json format
        requests_form = tin_match_request_form_serializer(request.POST, b_id)
        context['form_data'].update(requests_form)
        
        # note: tmr_obj is TinMatchReq class object
        tmr_obj = TinMatchReq()
        token = tmr_obj.get_auth_token()
        # create tin matching recipient request
        res_json = tmr_obj.create_tin_match_request(token, requests_form)
        context['api_res'].update(res_json)     # updating api response of create request to UI context

    return render(request, 'pages/tin_match/create-request.html', context)

def list_request_records(request, b_id, b_name, b_tin, sub_id=None, rec_id=None):
    
    context = {
        "business_id": b_id,
        "business_name": b_name,
        "business_tin": b_tin
    }

    # note: tmr_obj is TinMatchReq class object
    tmr_obj = TinMatchReq()
    token = tmr_obj.get_auth_token()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'status':
            # getting details of request using submission id and record id
            res_json = tmr_obj.get_request_record_status(token, sub_id, rec_id)
            # sending gotton details of request to UI
            context.update({'request_record_status': res_json})

        if action == 'cancel':
            # requesting to cancel the tin matching recipient request
            res_json = tmr_obj.cancel_request_record(token, sub_id, rec_id)
            # sending the response to UI
            context.update({'request_record_cancel': res_json})

    # getting list of tin match recipients requests using token and business_id
    res_json = tmr_obj.list_tin_match_request(token, b_id)
    if 'TINMatchingRecords' in res_json:
        # sending gotton list of requests to UI
        context.update({'request_records_list': res_json['TINMatchingRecords']})

    # it check for the error messages and show it in UI
    do_alerts(request, res_json)

    return render(request, 'pages/tin_match/list_requests.html', context)
