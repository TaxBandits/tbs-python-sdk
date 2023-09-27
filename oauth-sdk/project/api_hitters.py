# build in packages
import os
import time
from datetime import datetime

# installed packages
import jwt          # PyJWT
import requests


class oAuth:

    def __init__(self):
        self.oauth_url = os.getenv("TBS_PUBLIC_API_OAUTH")      # getting env variable values and assigning
        self.base_url = os.getenv("TBS_PUBLIC_API_BASE_URL")        
    
    def response_to_json(self, res):
    
        try:
            res_json = res.json()      # converting response object to json
        except Exception as err:
            res_json = { 'StatusMessage': f'something went wrong during json conversion due to : {err}' }

        if 'StatusCode' not in res_json:
            res_json['StatusCode'] = res.status_code

        return res_json

    def create_jws(self, client_id:str, client_secret:str, user_token:str):

        header = {
            "alg": "HS256",                     # Algorithm = HS256
            "typ": "JWT"                        # Type = JSON Web Token (JWT)
        }

        payload = {
            "iss": client_id,                   # Issuer: Client ID retrieved from the console site
            "sub": client_id,                   # Subject: Client ID retrieved from the console site
            "aud": user_token,                  # Audience: User Token retrieved from the console site
            "iat": round(time.time())           # Issued at: Number of seconds from Jan 1 1970 00:00:00 (Unix epoch format) - time in 
        }

        # encode from jwt package will encode the details and generate jwt token
        self.jws_token = jwt.encode(
            headers=header,
            payload=payload, 
            key=client_secret, 
        )

        return self.jws_token
    
    def get_jwt(self):

        url = f'{self.oauth_url}/tbsauth'   # url to get jwt

        response = requests.get(
            url=url,
            headers={'Authentication': self.jws_token}
        )
        
        res_json = self.response_to_json(response)

        # getting jwt token from response
        self.jwt_token = res_json['AccessToken']        

        return res_json

    def create_business_dummy(self):

        # this is dummy data to create dummy business for verifying the token
        business_form = {           
            "BusinessNm": "Eastman Kodak Company",
            "PayerRef": "QWErty1234",
            "TradeNm": "Kodak",
            "IsEIN": True,
            "EINorSSN": "003313330",
            "Email": "sample@bodeem.com",
            "ContactNm": "John",
            "Phone": "6549873215",
            "PhoneExtn": "12345",
            "Fax": "9876543544",
            "BusinessType": "ESTE",
            "SigningAuthority": {
                "Name": "John",
                "Phone": "9876549874",
                "BusinessMemberType": "ADMINISTRATOR"
            },
            "KindOfEmployer": "FEDERALGOVT",
            "KindOfPayer": "REGULAR941",
            "IsBusinessTerminated": True,
            "IsForeign": True,
            "USAddress": {
                "Address1": "3521 Airport Way",
                "Address2": "Unit 9",
                "City": "Fairbanks",
                "State": "AK",
                "ZipCd": "99709"
            },
            "ForeignAddress": {
                "Address1": "22 St",
                "Address2": "Clair Ave E",
                "City": "Toronto",
                "ProvinceOrStateNm": "Ontario",
                "Country": "CA",
                "PostalCd": "M1R 0E9"
            }
        }

        url = f"{self.base_url}/Business/Create"            # url to create business

        # requesting to create business
        response = requests.post(
            url=url,
            json=business_form,
            headers={'Authorization': f'Bearer {self.jwt_token}'}
        )

        res_json = self.response_to_json(response)

        return res_json

    def list_business(self):

        page = os.getenv('PAGE')                            # getting value from env
        page_size = os.getenv('PAGE_SIZE')                   
        from_date = os.getenv('FROM_DATE')

        now = datetime.now()
        to_date = now.strftime("%m/%d/%Y")                  # using current date for to_date
        
        url = f'{self.base_url}/Business/List'              # url to get list of our business, based on the jwt_token in headers

        # requesting to list business
        response = requests.get(
            url=url,
            headers={'Authorization': f'Bearer {self.jwt_token}'},
            params={
                'Page': page,
                'PageSize': page_size,
                'FromDate': from_date,
                'ToDate': to_date
            },
        )

        res_json = self.response_to_json(response)

        # checking business exist
        business_exist = response and 'Businesses' in res_json and res_json['Businesses']   

        if not business_exist:      # if no business exist
            res_json = self.create_business_dummy()     # this will create dummy business
            if 'StatusCode' in res_json and res_json['StatusCode'] == 200:
                # once dummy business create this will list that to response
                return self.list_business()

        return res_json