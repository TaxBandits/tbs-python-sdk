# build in packages
import os, time, json
from datetime import datetime

# installed packages
import requests
import jwt


class Utils:

    def __init__(self):
        # getting env variable values and assigning
        self.oauth_url = os.getenv("TBS_PUBLIC_API_OAUTH")
        self.base_url = os.getenv("TBS_PUBLIC_API_BASE_URL")

    def _response_to_json(self, res) -> dict:
        
        try:
            res_json = res.json()      # converting response object to json
        except Exception as err:
            res_json = { 'StatusMessage': f'something went wrong during json conversion due to : {err}' }

        if 'StatusCode' not in res_json:
            res_json['StatusCode'] = res.status_code

        return res_json
    
class oAuth(Utils):

    def __init__(self):
        super().__init__()

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
    
    def get_jwt(self, jws_token:str) -> str:

        url = f'{self.oauth_url}/tbsauth'

        response = requests.get(
            url=url,
            headers={ 'Authentication': jws_token }
        )
        
        res_json = self._response_to_json(response)

        jwt_token = res_json['AccessToken'] if 'AccessToken' in res_json else None

        return jwt_token

    def get_auth_token(self) -> str:
        
        client_id = os.getenv('TBS_API_CONSOLE_CLIENT_ID')
        client_secret = os.getenv('TBS_API_CONSOLE_CLIENT_SECRET_KEY')
        user_token = os.getenv('TBS_API_CONSOLE_USER_TOKEN')

        jws = self.create_jws(client_id, client_secret, user_token)   # jws - json web signature token - using this only we can create jwt
        jwt = self.get_jwt(jws_token=jws)                             # jwt - json web token - this acts as an authorization token

        return jwt

class Business(oAuth):

    def __init__(self):
        super().__init__()

    # method to create business using jwt token and business data contents
    def create_business(self, jwt_token:str, business_form:dict) -> dict:

        url = f"{self.base_url}/Business/Create"    # url to create business

        res = requests.post(
            url=url,
            json=business_form,
            headers={'Authorization': f'Bearer {jwt_token}'}
        )

        res_json = self._response_to_json(res)       # converting responst to json

        return res_json
    
    # method to list business using jwt token and it associated user
    def list_business(self, jwt_token:str) -> dict:

        now = datetime.now()

        # note: getenv will get values of requested argument from .env file 
        page = os.getenv('PAGE')
        page_size = os.getenv('PAGE_SIZE')

        from_date = os.getenv('FROM_DATE')
        to_date = now.strftime("%m/%d/%Y")

        url = f'{self.base_url}/Business/List'         # url for list of businesses

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

        res_json = self._response_to_json(res)   # converting response to json

        return res_json

class TinMatchReq(oAuth):

    def __init__(self):
        super().__init__()

    # method to create tin match recipeient request using jwt_token and request details
    def create_tin_match_request(self, jwt_token:str, requests_form:dict) -> dict:

        url = f'{self.base_url}/TINMatchingRecipients/Request'      # url to create tin matching request

        res = requests.post(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            json=requests_form
        )

        res_json = self._response_to_json(res)       # converting response to json

        return res_json

    # method to get list of receipients requests using jwt_token and business id
    def list_tin_match_request(self, jwt_token:str, b_id:str) -> dict:

        url = f'{self.base_url}/TINMatchingRecipients/List'     # url for get list of requests

        res = requests.get(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            params={
                "BusinessId": b_id
            }
        )

        res_json = self._response_to_json(res)       # converting response to json

        return res_json
    
    # method to get details about recipient request using subimission id, record id and jwt_token
    def get_request_record_status(self, jwt_token:str, sub_id:str, rec_id:str) -> dict:

        url = f'{self.base_url}/TINMatchingRecipients/Status'       # url for get details about the request

        res = requests.get(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            params={
                "SubmissionId": sub_id,
                "RecordId": rec_id
            }
        )

        res_json = self._response_to_json(res)       # converting response to json

        return res_json
    
    # method to cancel recipient request using submission id, record id and jwt_token
    def cancel_request_record(self, jwt_token:str, sub_id:str, rec_id:str) -> dict:

        url = f'{self.base_url}/TINMatchingRecipients/CancelRequest'        # url to cancel the recipient request

        res = requests.put(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            params={
                "SubmissionId": sub_id,
                "RecordIds": rec_id
            }
        )

        res_json = self._response_to_json(res)       # converting response to json

        return res_json