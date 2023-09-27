from django.contrib import messages

# this will show some error messages in web page if error occurs
def do_alerts(request, res_json):
    
    success = 'StatusCode' in res_json and res_json['StatusCode'] == 200
    if not success:
        
        msg_exist = 'StatusMessage' in res_json and res_json['StatusMessage']
        if msg_exist:
            messages.error(request, f'{res_json["StatusMessage"]}', extra_tags='danger')
