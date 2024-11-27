from fastapi import FastAPI, Request, APIRouter, HTTPException, status
from pydantic import BaseModel
from app.db.session import SessionLocal
import dotenv
import os
from authlib.integrations.starlette_client import OAuth
from endpoints.auth.auth import cookie_response, build_access_token

dotenv.load_dotenv()
host_ip = os.getenv('HOST_IP')
azure_client_id = os.getenv('AZURE_CLIENT_ID')
azure_tenant_id = os.getenv('OAUTH_TENANT_ID')
origins = [f"http://{host_ip}:3000", "http://localhost:3000", "http://localhost", f"http://{host_ip}",
           "https://localhost", "https://localhost:3000", f"https://{host_ip}", f"https://{host_ip}:3000"]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db = get_db()

router = APIRouter()

oauth = OAuth()
oauth.register(
    name='azure',
    client_id=os.getenv('OAUTH_CLIENT_ID'),
    client_secret=os.getenv('OAUTH_CLIENT_SECRET'),
    authorize_url=os.getenv('OAUTH_AUTHORIZATION_URL'),
    access_token_url=os.getenv('OAUTH_TOKEN_URL'),
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url=f"https://login.microsoftonline.com/{azure_tenant_id}/v2.0/.well-known/openid-configuration",
)


@router.get("/login")
async def login(request: Request):
    """
   Login Azure
   """
    return await oauth.azure.authorize_redirect(request, "http://localhost:8000/azure/auth/callback")


@router.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.azure.authorize_access_token(
        request)
    email = token['userinfo']['email']
    id_token = token['id_token']
    if token is not None:
        access_token = build_access_token(email, "", id_token)
        return cookie_response(access_token, True)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password"
        )
