from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from project.api_hitters import oAuth
from .utils import do_alerts


oaObj = oAuth()     # this oAuth class having all functionalities, we can use by call
context = {}        # this context json values are available in template

@csrf_exempt
def home(request):
    # to access the global variable of context
    global context
    
    if request.method == 'GET':
        context = {}

    elif request.method == 'POST':
        action = request.POST.get('action')

        if action == 'get_jws':

            client_id = request.POST.get('clientId')            # to get the clientId from template
            client_secret = request.POST.get('secretKey')       # to get the secretKey from template
            user_token = request.POST.get('userToken')          # to get the userToken from template

            credentials = { 'client_id': client_id, 'client_secret': client_secret, 'user_token': user_token }
            context.update(credentials)
            
            # create_jws will create jws token by using arguments - # jws is json web signature
            jws_token = oaObj.create_jws(client_id, client_secret, user_token)     
            context.update({'jws_token': jws_token})            # updating jws to template context

        elif action == 'get_jwt':

            # jwt token is json web token
            # get_jwt will get out token by using jws which is previously created
            res_json = oaObj.get_jwt()                          

            do_alerts(request, res_json)        # alert message will come if error occurs

            tokenExist = 'AccessToken' in res_json and res_json['AccessToken']
            if tokenExist:
                context.update({'jwt_token': res_json['AccessToken']})
            
        elif action == 'verify':
            
            # list_business will return list of our business based on our jwt token
            res_json = oaObj.list_business()                    

            do_alerts(request, res_json)

            businessExist = 'Businesses' in res_json and res_json['Businesses']
            if businessExist:
                context.update({'business_table': res_json['Businesses']})

        elif action == 'clear_all':
            context = {}            # all credientials, tokens, businesses will be cleared by replacing with empty dictionary

    return render(request, 'pages/home.html', context)