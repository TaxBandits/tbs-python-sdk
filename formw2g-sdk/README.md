# TaxBandits Form W2G API SDK

## Introduction

In this SDK, we demonstrate how to Validate, Create, List, Update, Status, Delete, Transmit, RequestPdf, and RequestDraftPdfUrl of FormW-2G. here we using Jinja2 as frontend and Django as backend in Python.

##### Version details:-

* **Python version - 3.11.4**
* **Django version - 4.2.5**
* **Jinja2 version - 3.1.2**
* **Boto3 version - 1.28.63**

## Setup Application in local

- Install python 3.11 version in your machine. Clone the project into your local machine using below command in Terminal/Command Prompt.

  ```bash
  git clone https://github.com/TaxBandits/tbs-python-sdk.git
  ```
- Open the formW2G-sdk folder path in terminal.
- Then

  - Create your python environment if you need local package installer environment.
  - All Dependency Packages are there in requirements.txt file,  Install those packages.
  - Run the project using below commands.
  - In Linux if you got any bugs use python 3.11, python3 should have version 3.11.

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
  * This package is a framework running project server and act as backend.
* jinja2
  * This package is used in frontend for creating components and reuse them.
* PyJWT
  * This package used to create JWS Token it is the first step of our project.
* requests
  * This package used to give request to any API with any methods.
* boto3
  * This package used to access data exist in AWS.

## Structure of the Application

### `project/`

* This is our project folder only contains all backend files except `manage.py`.
* `settings.py`

  * This file act as a complete configuration of our backend like setting middleware, template and static paths etc..,
* `api_services.py`

  * This is created file to organise the code, this file contains the collections of  api methods in separeted classes, which can able to request TaxBandits API and return response.
* `wsgi.py`

  * Web Server Gateway Interface (WSGI) is **a mediator responsible for conveying communication between a web server and a Python web application.**
* `asgi.py`

  * the  **Asynchronous Server Gateway Interface** . Like **WSGI**, ASGI describes a common interface between a Python web application and the web server. Unlike WSGI, ASGI allows multiple, asynchronous events per application.
* `views.py`

  * This file consist all our project views which is responsible for rendering html template along with backend data.
* `urls.py`

  * In this file we can write our project router url in `urlpatterns` list variable, here only we can assign our associated views with it's associated urls.
* `utils.py`

  * This file having utils functions and methods this is created file for code organizing purpose, all views functionality codes are here only.
* `jinja/`

  * Inside this folder we have `jinja2.py` file consisting `environment`  function and using this environment we can set many configurations for jinja2 frontend, we can export functions and more informations from backend and we can import those to our html template frontend.
  * this `jinja2.environment` where configured with our backend in `settings.py`  - TEMPLATES list variable.

### `apps/`

* this folder contains all our apps but not included in INSTALLED_APPS in `settings.py` because here we don't need to do database connections.
* `business/`

  * this business app take care of all business activities like create and list business.
* `w2g/`

  * this w2g app take care of all form w2g activities like validate, create, update, get and list Form w2g and also with some feature like get status, request draft pdf url, request pdf urls, transmit and delete form w2g.
* Otherwise the below files are same in each app.
* `urls.py`

  * this file contains that specific app urls in urls_patterns list, this will be included by the `urls.py` file in project, this url is connected with associated views from this app.
* `utils.py`

  * it contains some functions and class methods used in this app views.
* `views.py`

  * this file contains views of this app which render the templates, this views assigned with associated urls in this app.

### `templates/`

* Our project frontend is having architechture like single page application but this will not work like react js or angular js, this will reload whole page for every request but the reusability of set of codes using components by import and reusing a block of code by extend it, those feature we can perform with the help of jinja2.
* `macro` is a keyword in jinja2 to initiate a function which act like a component, will return a set of html tags, we can pass values to that component likewise passing arguments to parameter of the function.
* `base.html`

  * this file act as our base file consisting of styles and scripts, from `app.html` we are extending this file, so if we call `app.html` means `base.html` also will include.
* `requirement.html`

  * this file contains all of our required Libraries like jQuery, Bootstrap, Font-awesome etc.., here to organize we are using `macro` and we call those in `base.html`.
  * In `static/` folder we have `libraries/` folder, from there we are importing libraries.
* `app.html`

  * this file act as container of our html page, which contains components like navbar, sidebar or showing any alerts here.
* `pages/`

  * this folder contains all of our pages and each page will extend `app.html` so that from app `base.html` file will also extend so our page will have all library resources.
* `components/`

  * this folder contains all of our reusable UI components, using this we can reuse set of html codes and also we can send value as argument to the macro function so that from parameter we can get that value and use it in component.

### `static/`

* `css/`

  * this folder having all of our stylesheets.
  * `common.css` is our main css file.
* `js/`

  * this folder having all of our javaScripts.
  * `form_utils.js` is having javascript functions which is used by forms in this project
  * `document_init.js` is have some script which should run once our project initiated or started, withing sometime some activities have to be done like showing and removing message alerts like that.
  * `constant_values.js` file acts like .env file for frontend javascript, it contains many constant value in js variables which are used in some places of project js code, if we change from here, it will reflect in many places, so it is efficient.
* `libraries/`

  * this folder having all of libraries like bootstrap5, font-awesome4, jQuery3 and more.
* `images/`

  * this folder having our project used images.

### `manage.py`

* This file will manage everything in project, as centralized file it will run the server backend using `project/` and this will do many things in django like create apps for our project, migrate db etc..,

### `.env`

* This file contains environment variables for this projects, some of the values here are used many places in code, so once we change here means it will reflect many places with those changed values.

## Functionalities of Application

### Validate FormW-2G

It checks the request's W-2G Forms to IRS business standards and field specifications before creating FormW-2G. For validating FormW-2G, pass the recipient and FormW2G data as input along with Access Token in the header as Bearer Token (Generated using TaxBandits OAuth authentication API). After requesting validateForm method in FormW2G API, the response will be shown in a modal..

**TaxBandits Public API Base URL:** [https://testapi.taxbandits.com/{version}/FormW2G/ValidateForm]

### Create FormW-2G

For creating FormW-2G, pass the recipient and FormW2G data as input along with Access Token in the header as Bearer Token (Generated using TaxBandits OAuth authentication API) against businessId. After requesting create method in FormW2G API, the response will be shown in a modal.

**TaxBandits Public API Base URL:** [https://testapi.taxbandits.com/{version}/FormW2G/Create]

### List FormW-2G

For listing FormW-2G, BusinessId is passed as query parameter along with Access Token in the header as Bearer Token (Generated using TaxBandits OAuth authentication API).  After requesting list method in FormW-2G, the response is shown as a table.

**TaxBandits Public API Base URL:** [https://testapi.taxbandits.com/{version}/FormW2G/List]

### Update FormW-2G

For updating FormW-2G we are requesting get FormW-2G method from FormW2G API and fetch the data against SubmissionId and RecordId which is passed as query.  After retrieving data we'll update it by requesting TaxBandits Public API Base URL.

After requesting update method in FormW2G API, output will be shown in a modal and navigated to list FormW2G page.

**TaxBandits Public API Base URL:** [https://testapi.taxbandits.com/{version}/FormW2G/Update]

### Status FormW-2G

For displaying FormW-2G Status, pass the SubmissionId and RecordId as query along with Access Token in the header as Bearer Token (Generated using TaxBandits OAuth authentication API).
After requesting status method in FormW2G API, the response will be shown in a modal.

**TaxBandits Public API Base URL:** [https://testapi.taxbandits.com/{version}/FormW2G/Status]

### Delete FormW-2G

For deleting FormW-2G, pass the SubmissionId and RecordId as query along with Access Token in the header as Bearer Token (Generated using TaxBandits OAuth authentication API). Delete method in FormW2G API shows success response only if requested FormW2G is in not transmitted status else it will show error response. By passing these values we request to TaxBandits Public API Base URL.
After requesting delete method in FormW2G API, the response will be shown in a modal.

**TaxBandits Public API Base URL:** [https://testapi.taxbandits.com/{version}/FormW2G/Delete]

### Transmit FormW-2G

For transmitting FormW-2G, pass the SubmissionId and RecordId as query along with Access Token in the header as Bearer Token (Generated using TaxBandits OAuth authentication API). Transmit method in FormW2G API shows error response for already transmitted forms. By passing these values we request to TaxBandits Public API Base URL.
After requesting transmit method in FormW2G API, the response will be shown in a modal.

**TaxBandits Public API Base URL:** [https://testapi.taxbandits.com/{version}/FormW2G/Transmit]

### Request PDF-Urls FormW-2G

For requestingPdfUrl of FormW-2G, pass the SubmissionId and RecordId as request body along with Access Token in the header as Bearer Token (Generated using TaxBandits OAuth authentication API). requestPdfUrl method in FormW2G API shows success response only for transmitted forms else it shows error response. By passing these values we request to TaxBandits Public API Base URL.
After requesting requestPdfUrl method in FormW2G API, the response pdf urls will be shown in a table and by choosing anyone url ,it will be decrypted and shown as pdf in a modal.

**TaxBandits Public API Base URL:** [https://testapi.taxbandits.com/{version}/FormW2G/RequestPdfURLs]

### Request Draft PDF-Url FormW-2G

For requesting Draft of PDF Url of FormW-2G, pass the SubmissionId and RecordId as request body along with Access Token in the header as Bearer Token (Generated using TaxBandits OAuth authentication API). request Draft PDF Url method in FormW2G API shows success response only for not transmitted forms else it shows error response. By passing these vales we request to TaxBandits Public API Base URL.

After requestPdfUrl method in FormW2G API, the response pdf will be shown in the iframe inside popup model.

**TaxBandits Public API Base URL:** [https://testapi.taxbandits.com/{version}/FormW2G/RequestDraftPdfUrl]

In the above URLs, `{version}` is the endpoint version of TaxBandits API.

For more information, please refer:[https://developer.taxbandits.com/](https://developer.taxbandits.com/)
