# TaxBandits OAUTH API SDK

## Introduction

In this SDK, we demonstrate how to generate **JWT** (JSON Web Token) by generating **JWS** (JSON Web Signature) with user credentials provided from TaxBandits Console Site using Jinja2 as frontend and Django as backend in Python.

##### Version details:-

* **Python version - 3.11.4**
* **Django version - 4.2.5**
* **Jinja2 version - 3.1.2**

## Setup Application in local

- Install python 3.11 version in your machine. Clone the project into your local machine using below command in Terminal/Command Prompt.

  ```bash
  git clone https://github.com/TaxBandits/tbs-python-sdk.git
  ```
- Open the oauth-sdk folder path in terminal.
- Then

  - Create your python environment if you need local package installer environment
  - All Dependency Packages are there in requirements.txt file,  Install those packages
  - Run the project
  - using below commands as per your OS

  Linux or MacOS

  ```bash
  python3 --version
  > Python 3.11.4

  python3 -m venv venv311

  source venv/bin/activate

  pip3 install -r requirements.txt\

  python3 manage.py runserver
  ```

  Windows

  ```bash
  py -3.11 -m venv venv311

  .\venv311\Scripts\activate

  pip install -r requirements.txt

  python manage.py runserver
  ```

## Dependencies Used

#### Installed Packages for information

* django
  * this package is a framework running project server and act as backend
* jinja2
  * this package is used in frontend for creating components and reuse them
* PyJWT
  * this package used to create JWS Token it is the first step of our project
* requests
  * this package used to give request to any API with any methods

## Structure of the Application

### `project/`

* This is our project folder only contains all backend files except `manage.py`
* `settings.py`

  * This file act as a complete configuration of our backend like setting middleware, template and static paths etc..,
* `wsgi.py`

  * Web Server Gateway Interface (WSGI) is **a mediator responsible for conveying communication between a web server and a Python web application.**
* `asgi.py`

  * the  **Asynchronous Server Gateway Interface** . Like **WSGI**, ASGI describes a common interface between a Python web application and the web server. Unlike WSGI, ASGI allows multiple, asynchronous events per application.
* `urls.py`

  * In this file we can write our project router url in `urlpatterns` list variable, here only we can assign our associated views with it's associated urls.
* `api_hitters.py`

  * This file having utils functions and methods this is created file for code organizing purpose, all views functionality codes are here only
* `jinja/`

  * Inside this folder we have `jinja2.py` file consisting `environment`  function and using this environment we can set many configurations for jinja2 frontend, we can export functions and more informations from backend and we can import those to our html template frontend
  * this `jinja2.environment` where configured with our backend in `settings.py`  - TEMPLATES list variable

### `oauth/`

* this folder act as a app but not included in INSTALLED_APPS in `settings.py` because here we don't need to do Database connections
* `utils.py`
  * contains functions and class methods used in this app views
* `views.py`
  * This file consist all our project views which is responsible for rendering html template along with backend data

### `templates/`

* Our project frontend is having architechture like single page application but this will not work like react js or angular js, this will reload whole page for every request but the reusability of set of codes using components by import and reusing a block of code by extend it, those feature we can perform with the help of jinja2
* `macro` is a keyword in jinja2 to initiate a function which act like a component, will return a set of html tags, we can pass values to that component likewise passing arguments to parameter of the function
* `base.html`

  * this file act as our base file consisting of styles and scripts, from `app.html` we are extending this file, so if we call `app.html` means `base.html` also will include
* `requirement.html`

  * this file contains all of our required Libraries like jQuery, Bootstrap, Font-awesome etc.., here to organize we are using `macro` and we call those in `base.html`
  * In `static/` folder we have `libraries/` folder, from there we are importing libraries
* `app.html`

  * this file act as container of our html page, which contains components like navbar, sidebar or showing any alerts here
* `pages/`

  * this folder contains all of our pages and each page will extend `app.html` so that from app `base.html` file will also extend so our page will have all library resources

### `static/`

* `css/`

  * this folder having all of our stylesheets
  * `common.css` is our main css file
* `js/`

  * this folder having all of our javaScripts
  * `document_init.js` is have some script which should run once our project initiated or started, withing sometime some activities have to be done like showing and removing message alerts like that
* `libraries/`

  * this folder having all of libraries like bootstrap5, font-awesome4, jQuery3 and more## JWS Authorization
* `images/`

  * this folder having our project used images

### `manage.py`

* This file will manage everything in project, as centralized file it will run the server backend using `project/` and this will do many things in django like create apps for our project, migrate db etc..,

### `.env`

* This file contains environment variables for this projects, some of the values here are used many places in code, so once we change here means it will reflect many places with those changed values

## Functionalities of Application

### JWS Authorization

Using JWS pip package, we generate signature by passing headers, payload and secret key.

```python
header = {
	"alg": "HS256",                     # Algorithm = HS256
	"typ": "JWT"                        # Type = JSON Web Token (JWT)
}
```

```python
payload = {
	"iss": client_id,                   # Issuer: Client ID retrieved from the console site
	"sub": client_id,                   # Subject: Client ID retrieved from the console site
	"aud": user_token,                  # Audience: User Token retrieved from the console site
	"iat": round(time.time())           # Issued at: Number of seconds from Jan 1 1970 00:00:00 (Unix epoch format) - time in 
}
```

In the above payload, unixEpochStringConversion is used to convert the current time to Unix Epoch format in our project.

> Note : You can get your own ClientId, Secret key and User Token from our TaxBandits Console Site. [Goto TaxBandits Console Site](https://sandbox.taxbandits.com/)

```javascript
self.jws_token = jwt.encode(
	headers=header,
	payload=payload, 
	key=client_secret, # Client Secret retrieved from the console site
)
```

#### Sample JWS

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOi  
I5NjhhOWM3OGRhZTI5YTI5Iiwic3ViIjoiOTY4YTljNzhkYWUyOWEyOSIsImF1  
ZCI6ImE1NzRiNzVmMThiMjRmYzA5ZjkwMzlmZmI1Y2IwOGYzIiwiaWF0IjoxN  
TE2MjM5MDIyfQ.HNQznxlPyVt62kyUeVwtk1-uzm1uDWH4NBDLShA6Ac0
```

### JWT Authentication

Once the JWS is created, then send a request to the Authentication Server by passing JWS in headers for an generating Access token.
**Authentication Server URL:** [https://testoauth.expressauth.net/v2/tbsauth]

```python
response = requests.get(
	url=url,
	headers={'Authentication': self.jws_token}
)
```

#### Sample JWT

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3  
MiOiJ0ZXN0YXBpLnRheGJhbmRpdHMuY29tIiwiYXVkI  
joiYTU3NGI3NWYxOGIyNGZjMDlmOTAzOWZmYjVjYjA4ZjMiLCJp  
YXQiOjE1OTU5MjAxMjQsImV4cCI6MTU5NTkyNzMyNH0.BIg8764SOhOai9As  
3uRSidrF1-B9CxL6D5z4OggcVbs
```

Once you obtain the JWT (Access token), you can use the same JWT along with every API request until the token expires.

> Note: Your JWT will expires in One hour from the time of creation.

### Verify JWT

- You can verify your JWT is valid by clicking on the Verify JWT button.
- If there is any business under the User, it will be shown as a list of business by hitting Business/List method.
  **Business/List API URL:** [https://testapi.taxbandits.com/{version}/Business/List]
- If there is no business under the User, it shows the response from the list method in Business TBS Public API Base URL.

  #### Sample No Business found

  ![No Business found]


  ```json
  {
  	"StatusCode": 404,
  	"StatusName": "NotFound",
  	"StatusMessage": "The resource you have specified cannot be found",
  	"Businesses": null,
  	"Page": 1,
  	"TotalRecords": 0,
  	"TotalPages": 0,
  	"PageSize": 10,
  	"Errors": null
  }
  ```

 In the above URLs, `{version}` is the endpoint version of TaxBandits API. if we got the above response means then the project will create dummy business in the details mentioned below and that dummy business will come as a response in the list business

#### Sample dummy business

```json
{
	"BusinessNm": "Eastman Kodak Company",
	"PayerRef": "QWErty1234",
	"TradeNm": "Kodak",
	"IsEIN": True,
	"EINorSSN": "003313330",
	"Email": "sample@bodeem.com",
	"ContactNm": "John",
	"Phone": "6549873215",
}
```

For more information, please refer: [https://developer.taxbandits.com/](https://developer.taxbandits.com/)
