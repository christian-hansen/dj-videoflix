# Django backend for "Videoflix

## Project Description

This is a learning project created as part of my studies with the Developer Akademie. The project serves as the backend for a video platform application. The frontend for this application can be found [here](https://github.com/christian-hansen/ng-videoflix).

## Installation and Setup

1. Clone the Repository:
    ```bash
    git clone https://github.com/christian-hansen/dj-videoflix.git
    cd dj-videoflix
    ```
2. Create a virtual environment and install the dependencies:
    ```bash
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```
3. For security reasons secrets are stored separately. You need to create .env file in the main folder and enter the secrets (without []) to the following variables:
    ```bash
    EMAIL_HOST=[]
    EMAIL_PORT=[]
    EMAIL_HOST_USER=[]
    EMAIL_HOST_PASSWORD=[]
    DEFAULT_FROM_EMAIL=[]
    DJANGO_SECRET=[]
    RQ_PASSWORD=[]
     #Incase you use postgres database. 
    PSQL_USER=[]
    PSQL_PW=[]
     #If not make sure to update settings.py back to sqlite database.
    ```
4. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5. Create a Superuser
    ```bash
    python manage.py createsuperuser
    ```
6. Start the Django development server:
    ```bash
    python manage.py runserver
    ```
7. Check URLS and Ports (Ensure the backend is running on port 8000, as some links may not work otherwise):
    ```bash
    open http://localhost:8000/admin
    ```
8. To convert videos after uploading the RQ Worker needs to be started:
    ```bash
    python manage.py rqworker default
    ```

## Running included tests
To run the include test file and get a report in the command line please run:
```bash
coverage run manage.py test
coverage report
```
