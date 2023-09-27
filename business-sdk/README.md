# TaxBandits Business API SDK

## Introduction

In this SDK, we demonstrate how to create, list and update business with TaxBandits Business Endpoints. here we using Jinja2 as frontend and Django as backend in Python.

##### Version details:-

* **Python version - 3.11.4**
* **Django version - 4.2.5**
* **Jinja2 version - 3.1.2**

## Setup Application in local

- Install python 3.11 version in your machine. Clone the project into your local machine using below command in Terminal/Command Prompt.

  ```bash
  git clone https://github.com/TaxBandits/tbs-python-sdk.git
  ```
- Open the business-sdk folder path in terminal.
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
* `api_hitters.py`

  * This is created file to organise the code, this file contains the collections of api hit methods in separeted classes
* `wsgi.py`

  * Web Server Gateway Interface (WSGI) is **a mediator responsible for conveying communication between a web server and a Python web application.**
* `asgi.py`

  * the  **Asynchronous Server Gateway Interface** . Like **WSGI**, ASGI describes a common interface between a Python web application and the web server. Unlike WSGI, ASGI allows multiple, asynchronous events per application.
* `urls.py`

  * In this file we can write our project router url in `urlpatterns` list variable, here only we can assign our associated views with it's associated urls and also we can include our project apps url.
* `jinja/`

  * Inside this folder we have `jinja2.py` file consisting `environment`  function and using this environment we can set many configurations for jinja2 frontend, we can export functions and more informations from backend and we can import those to our html template frontend
  * this `jinja2.environment` where configured with our backend in `settings.py`  - TEMPLATES list variable

### `business/`

* this folder act as a app but not included in INSTALLED_APPS in `settings.py` because here we don't need to do Database connections
* `urls.py`
  * this file contains that specific app urls in urls_patterns list, this will be included by the `urls.py` file in project, this urls are connected with associated views from this app
* `utils.py`
  * contains functions and class methods used in this app views
* `views.py`
  * this file contains views of this app which render the templates, this views assigned with associated urls in this app

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
* `components/`

  * this folder contains all of our reusable UI components, using this we can reuse set of html codes and also we can send value as argument to the macro function so that from parameter we can get that value and use it in component

### `static/`

* `css/`

  * this folder having all of our stylesheets
  * `common.css` is our main css file
* `js/`

  * this folder having all of our javaScripts
  * `document_init.js` is have some script which should run once our project initiated or started, withing sometime some activities have to be done like showing and removing message alerts like that
  * `constant_values/`
    * this folder contains some js files which is act like .env file, it contains many constant value in js variables which are used in some places in project js code, if we need to change we have to change from files here
    * example we have `business_form_select_options.js` here we can change the option value so it will reflect in business_form component select tag options list in `components/business_form.html`
* `libraries/`

  * this folder having all of libraries like bootstrap5, font-awesome4, jQuery3 and more
* `images/`

  * this folder having our project used images

### `manage.py`

* This file will manage everything in project, as centralized file it will run the server backend using `project/` and this will do many things in django like create apps for our project, migrate db etc..,

### `.env`

* This file contains environment variables for this projects, some of the values here are used many places in code, so once we change here means it will reflect many places with those changed values

## Functionalities of Application

### Create Business

For creating business, pass the required data from Frontend to the Backend. In Backend, JWT will be generated by oAuth_collections and passed to the TaxBandits Create Business Endpoint in headers as Authorization. By requesting the TaxBandits Create Business Endpoint, the business will be created and output will be shown in a modal.

**TaxBandits Public API Base URL:** [https://testapi.taxbandits.com/{version}/Business/Create]

### List Business

For listing business we are passing page, page size, FromDate as params which is taken from .env files and ToDate is taken as current date which is also passed as params and JWT token as headers. By passing these values we request to TaxBandits Public API Base URL.
After requesting list method in business API we'll display the response data as a list.

**TaxBandits Public API Base URL:** [https://testapi.taxbandits.com/{version}/Business/List]

- If there is no business under the User, it shows the response from the list method in Business TaxBandits Public API Base URL.#### Sample No Business found

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

### Update Business

For updating business we are requesting get business method from Business API and fetch the data based on Business ID which is passed as params. After retrieving data we'll update it by requesting TaxBandits Public API Base URL.
After requesting update method in business API, output will be shown in a modal.

**TaxBandits Public API Base URL:** [https://testapi.taxbandits.com/{version}/Business/Update]

In the above URLs, `{version}` is the endpoint version of TaxBandits API.

For more information, please refer: [https://developer.taxbandits.com/](https://developer.taxbandits.com/)
