import requests
from app.db.session import get_db, SessionLocal
from endpoints.auth.auth import login
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
import os

load_dotenv()
test_user = os.getenv("TEST_USER")
test_password = os.getenv("TEST_PASSWORD")


def get_cookie():
    session = requests.Session()
    db = next(get_db())
    login_credentials = OAuth2PasswordRequestForm(
        username=test_user,
        password=test_password
    )
    login_response = login(login_credentials, db)

    cookie = login_response.headers.get('set-cookie')

    cookie_separated = cookie.split(';')
    for section in cookie_separated:
        if section.startswith('access_token='):
            token_value = section.split('=')[1]
    session.cookies.set('access_token', token_value)
    return session

