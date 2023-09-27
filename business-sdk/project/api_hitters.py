# django imports
from django.contrib import messages

# build in packages
import os
import time
from datetime import datetime

# installed packages
import requests
import jwt


class oAuth:

    def create_jws(self, client_id:str, client_secret:str, user_token:str):

        header = {
            "alg": "HS256",     # Algorithm = HS256
            "typ": "JWT"        #Type = JSON Web Token (JWT)
        }

        payload = {
            "iss": client_id,           # Issuer: Client ID retrieved from the console site
            "sub": client_id,           # Subject: Client ID retrieved from the console site
            "aud": user_token,          # Audience: User Token retrieved from the console site
            "iat": round(time.time())   # Issued at: Number of seconds from Jan 1 1970 00:00:00 (Unix epoch format) - time in 
        }

        jws_token = jwt.encode(
            headers=header,
            payload=payload, 
            key=client_secret, 
        )

        return jws_token
    
    def get_jwt(self, jws_token):

        url = f'{self.oauth_url}/tbsauth'   # url to get jwt

        response = requests.get(
            url=url,
            headers={ 'Authentication': jws_token }
        )
        
        res_json = self.response_to_json(response)
        
        # getting jwt token from response
        jwt_token = res_json['AccessToken'] if 'AccessToken' in res_json else None

        return jwt_token

    def get_auth_token(self):
        client_id = os.getenv('TBS_API_CONSOLE_CLIENT_ID')
        client_secret = os.getenv('TBS_API_CONSOLE_CLIENT_SECRET_KEY')
        user_token = os.getenv('TBS_API_CONSOLE_USER_TOKEN')

        jws = self.create_jws(client_id, client_secret, user_token)   # jws - json web signature token - using this only we can create jwt
        jwt = self.get_jwt(jws_token=jws)                             # jwt - json web token - this acts as an authorization token

        return jwt

class Business(oAuth):
    def __init__(self):
        # getting env variable values and assigning
        self.oauth_url = os.getenv("TBS_PUBLIC_API_OAUTH")
        self.base_url = os.getenv("TBS_PUBLIC_API_BASE_URL")

    def response_to_json(self, res):

        try:
            res_json = res.json()      # converting response object to json here
        except Exception as err:
            res_json = { 'StatusMessage': f'something went wrong during json conversion due to : {err}' }

        return res_json

    # method to create business using jwt token and business data contents
    def create_business(self, jwt_token, business_form):

        url = f"{self.base_url}/Business/Create"    # url to create business

        res = requests.post(
            url=url,
            json=business_form,
            headers={'Authorization': f'Bearer {jwt_token}'}
        )

        res_json = self.response_to_json(res)   # convering response to json

        return res_json

    # method to update business using jwt token and business data contents
    def update_business(self, jwt_token, business_form):

        url = f"{self.base_url}/Business/update"    # url to update business

        res = requests.put(
            url=url,
            json=business_form,
            headers={'Authorization': f'Bearer {jwt_token}'}
        )

        res_json = self.response_to_json(res)   # convering response to json

        return res_json

    # method to get business using jwt token and business id
    def get_business(self, jwt_token, business_id):
        
        url = f'{self.base_url}/Business/get'   # url for get business

        res = requests.get(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            params={
                'BusinessId': business_id
            }
        )

        res_json = self.response_to_json(res)   # convering response to json

        return res_json

    # method to list business using jwt token and it associated user
    def list_business(self, jwt_token):

        now = datetime.now()

        # note: getenv will get values of requested argument from .env file 
        page = os.getenv('PAGE')
        page_size = os.getenv('PAGE_SIZE')
        
        from_date = os.getenv('FROM_DATE')
        to_date = now.strftime("%m/%d/%Y")

        url = f'{self.base_url}/Business/List'  # url for list of businesses

        res = requests.get(
            url=url,
            params={
                'Page': page,
                'PageSize': page_size,
                'FromDate': from_date,
                'ToDate': to_date
            },
            headers={'Authorization': f'Bearer {jwt_token}'}
        )

        res_json = self.response_to_json(res)   # converting response to json

        return res_json
