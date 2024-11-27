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
azure_tenant_id = os.getenv('AZURE_TENANT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
authorize_url = f"https://login.microsoftonline.com/{azure_tenant_id}/oauth2/v2.0/authorize"
access_token_url = f"https://login.microsoftonline.com/{azure_tenant_id}/oauth2/v2.0/token"


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
    client_id=azure_client_id,
    client_secret=client_secret,
    authorize_url=authorize_url,
    access_token_url=access_token_url,
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url=f"https://login.microsoftonline.com/{azure_tenant_id}/v2.0/.well-known/openid-configuration",
)


@router.get("/login")
async def login(request: Request):
    """
   Login Azure
   """
    scheme = request.url.scheme
    redirect_uri = f"{scheme}://{host_ip}:8000/azure/auth/callback"

    return await oauth.azure.authorize_redirect(request, redirect_uri)


@router.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.azure.authorize_access_token(
        request)
    email = token['userinfo']['email']
    id_token = token['id_token']
    if token is not None:
        access_token = build_access_token(email, "", id_token)
        return cookie_response(access_token=access_token, request=request,azure_token=True)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password"
        )
