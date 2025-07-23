# build in packages
import os, time, base64
from datetime import datetime

# installed packages
import requests, jwt, boto3


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
    
    def get_pdf_as_buffer(self, file_url):
    
        file_path_parts = file_url.split('.com/')

        bucket_name = os.getenv('BUCKET_NAME')
        access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        secret_access_key = os.getenv('AWS_SECRET_KEY_ID')
        eCustomerKey = os.getenv('AWS_ENCRYPTION_KEY')
        
        enc_eCustomerKey = base64.b64decode(eCustomerKey)

        list_bytearray_content = self._get_file_from_aws_bucket(
            bucket_name = bucket_name, 
            access_key_id = access_key_id, 
            secret_access_key = secret_access_key,
            eCustomerKey = enc_eCustomerKey,
            eCustomerAlg = 'AES256',
            file_key = file_path_parts[len(file_path_parts)-1]
        )

        return list_bytearray_content

    def _get_file_from_aws_bucket(self, bucket_name, access_key_id, secret_access_key, eCustomerKey, eCustomerAlg, file_key):
   
        s3 = boto3.client(
            service_name='s3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name="us-east-1"
        )

        response = s3.get_object(
            Bucket=bucket_name,
            Key=file_key,
            SSECustomerKey=eCustomerKey,
            SSECustomerAlgorithm=eCustomerAlg
        )

        read_content = response['Body'].read()
        byte_array_content = bytearray(read_content)
        listed_bytearray_content = list(byte_array_content)

        return listed_bytearray_content
    
        # ---- In frontend use this method to show the "listed_bytearray_content" -----
        # const byte_array = new Uint8Array({{ listed_bytearray_content|safe }});
        # const blob = new Blob([byte_array], { type: 'application/pdf' });
        # const pdfUrl = URL.createObjectURL(blob);

        # const iframe = document.createElement('iframe');
        # iframe.src = pdfUrl;
        # iframe.style.width = '100%';
        # iframe.style.height = '600px'; 
        # document.body.appendChild(iframe);

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
    
    def get_jwt(self, jws_token:str):

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
    
    # method to get business using jwt token and business id
    def get_business(self, jwt_token:str, business_id:dict) -> dict:
        
        url = f'{self.base_url}/Business/get'
        res = requests.get(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            params={
                'BusinessId': business_id
            }
        )

        res_json = self._response_to_json(res)

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

class FormW2G(oAuth):

    def __init__(self):
        super().__init__()

    # method to create FormW2G using jwt_token and form data json
    def create_w2g(self, jwt_token:str, form:dict) -> dict:

        url = f'{self.base_url}/FormW2G/create'      # url to create FormW2G

        res = requests.post(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            json=form
        )
        
        res_json = self._response_to_json(res)       # converting response to json

        return res_json
    
    # method to validate FormW2G using jwt_token and form data json
    def validate_w2g(self, jwt_token:str, form:dict) -> dict:

        url = f'{self.base_url}/FormW2G/validateform'      # url to validate FORMW2G

        res = requests.post(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            json=form
        )
        
        res_json = self._response_to_json(res)       # converting response to json

        return res_json

    # method to update FormW2G using jwt_token and form data json
    def update_w2g(self, jwt_token:str, form:dict):

        url = f'{self.base_url}/FormW2G/update'      # url to update FormW2G

        res = requests.put(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            json=form
        )
        
        res_json = self._response_to_json(res)       # converting response to json

        return res_json

    # method to get details of FormW2G using jwt_token, subimission id and record id
    def get_w2g(self, jwt_token:str, sub_id:str, rec_id:str):

        url = f'{self.base_url}/FormW2G/Get'       # url for get details of FormW2G

        res = requests.get(
            url=url,
            headers={'Authorization': f'{jwt_token}'},
            params={
                "SubmissionId": sub_id,
                "RecordId": rec_id
            }
        )

        res_json = self._response_to_json(res)       # converting response to json

        return res_json
    
    # method to list of FormW2G using jwt_token and business id
    def list_w2g_forms(self, jwt_token:str, b_id:str) -> dict:

        # note: getenv will get values of requested argument from .env file 
        page = os.getenv('PAGE')
        page_size = os.getenv('PAGE_SIZE')

        url = f'{self.base_url}/FormW2G/list'     # url for list of FORMW2G

        res = requests.get(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            params={
                "BusinessId": b_id,
                "Page": page,
                "PageSize": page_size
            }
        )

        res_json = self._response_to_json(res)       # converting response to json

        return res_json
    
    # method to status of FormW2G using jwt_token, submission id and record id
    def status_w2g(self, jwt_token:str, sub_id:str, rec_id:str):

        url = f'{self.base_url}/FormW2G/status'     # url for status of FormW2G

        res = requests.get(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            params={
                "SubmissionId": sub_id,
                "RecordIds": rec_id
            }
        )

        res_json = self._response_to_json(res)       # converting response to json

        return res_json
    
    # method to request Draft Pdf Url of FormW2G using jwt_token and record id
    def draft_pdf_url_of_w2g(self, jwt_token:str, rec_id:str):

        url = f'{self.base_url}/FormW2G/RequestDraftPdfUrl'     # url for request Draft Pdf Url of FormW2G

        res = requests.post(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            json={
                "TaxYear": None,
                "RecordId": rec_id,
                "Business": None,
                "Recipient": None
            }
        )

        res_json = self._response_to_json(res)       # converting response to json

        return res_json
    
    # method to request Pdf Urls of FormW2G using jwt_token, submission id and record id
    def pdf_urls_of_w2g(self, jwt_token:str, sub_id:str, rec_id:str):

        url = f'{self.base_url}/FormW2G/RequestPdfURLs'     # url for request Pdf URLs of FormW2G

        res = requests.post(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            json={
                "SubmissionId": sub_id,
                "RecordIds": [
                    { "RecordId": rec_id }
                ],
                "Customization": {
                   "TINMaskType": "Both"
                }
            }
        )

        res_json = self._response_to_json(res)       # converting response to json

        return res_json
    
    # method to transmit of FormW2G using jwt_token, submission id and record id
    def transmit_w2g(self, jwt_token:str, sub_id:str, rec_id:str):
                
        url = f'{self.base_url}/FormW2G/Transmit'     # url for Transmit of FormW2G

        res = requests.post(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            json={
                "SubmissionId": sub_id,
                "RecordIds": [rec_id]
            }
        )

        res_json = self._response_to_json(res)       # converting response to json

        return res_json
    
    # method to delete of FormW2G using jwt_token, submission id and record id
    def delete_w2g(self, jwt_token:str, sub_id, rec_id):

        url = f'{self.base_url}/FormW2G/delete'     # url for delete of FormW2G

        res = requests.delete(
            url=url,
            headers={'Authorization': f'Bearer {jwt_token}'},
            params={
                "SubmissionId": sub_id,
                "RecordIds": rec_id
            }
        )

        res_json = self._response_to_json(res)       # converting response to json

        return res_json