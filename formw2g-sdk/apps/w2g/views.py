# django imports
from django.shortcuts import render

# folder imports
from .utils import w2g_form_serializer
from project.api_services import FormW2G, Business
from project.utils import do_alerts


loaded_business = {}
def create_w2g(request, b_id):

    url_name = request.resolver_match.url_name

    context = {
        "business_id": b_id,
        "form_data": {},
        "api_res": {}
    }

    # note: w2g_obj is FormW2G class object
    w2g_obj = FormW2G()

    global loaded_business

    # business get
    if not loaded_business or loaded_business['BusinessId'] != b_id:
        # note: b_obj is Business class object
        b_obj = Business()
        token = b_obj.get_auth_token()
        # get business using business id(b_id)
        b_res_json = b_obj.get_business(jwt_token=token, business_id=b_id)
        if 'Business' in b_res_json:
            loaded_business = b_res_json['Business']
            context.update({'business': loaded_business}) # sending gotten business to UI
        do_alerts(request, b_res_json)

    else:
        context.update({'business': loaded_business}) # sending gotten business to UI

    # create FormW2G 
    if request.method == 'POST':
        # processing the request.POST data object to json format
        w2g_form = w2g_form_serializer(request.POST, loaded_business)
        # sending FormW2G form to UI, so that user can verify after form values created with
        context['form_data'].update(w2g_form)
        
        token = w2g_obj.get_auth_token()

        if url_name == 'create-w2g':
            # creating FormW2G form
            res_json = w2g_obj.create_w2g(token, w2g_form)
                
        elif url_name == 'validate-w2g':
            # validating FormW2G form
            res_json = w2g_obj.validate_w2g(token, w2g_form)
        context['api_res'].update(res_json)     # updating api response of create form to UI context

    return render(request, 'pages/w2g/create-w2g.html', context)

def update_w2g(request, b_id, sub_id, rec_id):

    context = {
        "business_id": b_id,
        "submission_id": sub_id,
        "record_id": rec_id,
        "form_data": {},
        "api_res": {}
    }

    global loaded_business

    # business get
    if not loaded_business or loaded_business['BusinessId'] != b_id:
        # note: b_obj is Business class object
        b_obj = Business()
        token = b_obj.get_auth_token()
        # getting business using business id
        b_res_json = b_obj.get_business(jwt_token=token, business_id=b_id) 
        if 'Business' in b_res_json:
            loaded_business = b_res_json['Business']
            context.update({'business': loaded_business}) # sending gotten business to UI
        do_alerts(request, b_res_json)
        
    else:
        context.update({'business': loaded_business}) # sending gotten business to UI

    # note: w2g_obj is FormW2G class object
    w2g_obj = FormW2G()

    token = w2g_obj.get_auth_token()
    # get FormW2G data json
    res_json = w2g_obj.get_w2g(jwt_token=token, sub_id=sub_id, rec_id=rec_id)
    if 'FormW2GRecords' in res_json and res_json['FormW2GRecords']:
        context['form_data'].update(res_json['FormW2GRecords'])     # updating api response of get form data to UI context
    do_alerts(request, res_json)

    # update FormW2G data
    if request.method == 'POST':
        # processing the request.POST data object to json format
        w2g_form = w2g_form_serializer(request.POST, loaded_business, submission_id=sub_id, record_id=rec_id)
        # sending FormW2G form to UI, so that user can verify after form values updated with
        context['form_data'].update(w2g_form)

        token = w2g_obj.get_auth_token()
        # updating FormW2G
        res_json = w2g_obj.update_w2g(jwt_token=token, form=w2g_form)

        context['api_res'].update(res_json)     # updating api response of update form to UI context

    return render(request, 'pages/w2g/update-w2g.html', context)

def list_w2g(request, b_id, b_name, b_tin, sub_id=None, rec_id=None):

    # # Clean and validate name parts
    # name_parts = []
    # if is_valid(b_fname):
    #     name_parts.append(str(b_fname).strip())
    # if is_valid(b_mname):
    #     name_parts.append(str(b_mname).strip())
    # if is_valid(b_sname):
    #     name_parts.append(str(b_sname).strip())
    # if is_valid(b_lname):
    #     name_parts.append(str(b_lname).strip())

    # # Use full name if first and last names are valid
    # if is_valid(b_fname) and is_valid(b_lname):
    #     business_name = " ".join(name_parts)
    # else:
    #     business_name = b_name

    context = {
        'business_id': b_id,
        'business_name': b_name,
        'business_tin': b_tin
    }

    # note: w2g_obj is FormW2G class object
    w2g_obj = FormW2G()
    token = w2g_obj.get_auth_token()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'status':
            # getting status using submission id and record id
            res_json = w2g_obj.status_w2g(token, sub_id, rec_id)
            # sending response json to UI
            context.update({'form_status_res': res_json})

        if action == 'draft-pdf-url':
            # getting draft pdf url using submission id and record id
            res_json = w2g_obj.draft_pdf_url_of_w2g(token, rec_id)

            file_url = res_json.get('DraftPdfUrl', None)

            if file_url:
                list_bytearray_content = w2g_obj.get_pdf_as_buffer(file_url)
                res_json.update({'pdf_file': list_bytearray_content })

            # sending response json to UI
            context.update({'form_draft_pdf_url_res': res_json})

        if action == 'pdf-url':
            
            # getting pdf urls using submission id and record id
            res_json = w2g_obj.pdf_urls_of_w2g(token, sub_id, rec_id)

            current_pdf_details = {
                'submission_id': sub_id,
                'record_id': rec_id
            }
            res_json.update({'current_pdf_details': current_pdf_details})

            file_url = request.POST.get('file-url-masked')
            if file_url:
                list_bytearray_content = w2g_obj.get_pdf_as_buffer(file_url)
                res_json.update({'pdf_file': list_bytearray_content})

            # sending response json to UI
            context.update({'form_pdf_urls_res': res_json})

        if action == 'transmit':
            # getting transmit using submission id and record id
            res_json = w2g_obj.transmit_w2g(token, sub_id, rec_id)
            # sending response json to UI
            context.update({'form_transmit_res': res_json})

        if action == 'delete':
            # getting delete using submission id and record id
            res_json = w2g_obj.delete_w2g(token, sub_id, rec_id)
            # sending response json to UI
            context.update({'form_delete_res': res_json})

    # getting list of FormW2G using token and business_id
    res_json = w2g_obj.list_w2g_forms(token, b_id)
    if 'Form1099Records' in res_json:
        # sending gotton list of FormW2G to UI
        context.update({'form_list': res_json['Form1099Records']})
    do_alerts(request, res_json)

    return render(request, 'pages/w2g/list-w2g.html', context)


def is_valid(value):
    """Check if value is not None, not 'None', and not empty/whitespace."""
    return value is not None and str(value).strip().lower() != 'none' and str(value).strip() != ''
