from fastapi import Request, HTTPException
from app.config import settings

def verify_token(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token_type, token = auth_header.split(' ', 1)
        if token_type == "Bearer" and token == settings.static_token:
            return
    raise HTTPException(status_code=403, detail="Invalid token")
