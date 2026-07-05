from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import jwt

app = FastAPI()

PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuY
cxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMID
EkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXc
WyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfW
ed+zclR6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd1l9VDetJZVEgC5tkyvXsfI
SI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4LlgniT7GlkL9Mce3b0wGLs9/7ZIX
dQIDAQAB
-----END PUBLIC KEY-----
"""

ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-iu76h7tr.apps.exam.local"

class TokenRequest(BaseModel):
    token: str

@app.post("/verify")
async def verify_token(request: TokenRequest):
    try:
        payload = jwt.decode(
            request.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=ISSUER,
        )

        return {
            "valid": True,
            "email": payload.get("email"),
            "sub": payload.get("sub"),
            "aud": payload.get("aud"),
        }

    except Exception:
    return JSONResponse(
        status_code=401,
        content={"valid": False}
    )
    # ------------------- Q3 : /effective-config -------------------

DEFAULTS = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

YAML_CONFIG = {
    "workers": 10,
    "api_key": "key-0587m264vl",
}

ENV_FILE = {
    "port": 8651,
    "workers": 2,   # NUM_WORKERS -> workers
    "log_level": "info",
}

OS_ENV = {
    "port": 8518,
    "workers": 14,
    "debug": True,
    "log_level": "error",
    "api_key": "key-qcsk12icex",
}

def to_bool(value):
    return str(value).lower() in ["true", "1", "yes", "on"]

@app.get("/effective-config")
async def effective_config(set: list[str] = Query(default=[])):
    config = {}

    # Merge in precedence order
    config.update(DEFAULTS)
    config.update(YAML_CONFIG)
    config.update(ENV_FILE)
    config.update(OS_ENV)

    # CLI overrides
    for item in set:
        if "=" in item:
            key, value = item.split("=", 1)

            if key in ["port", "workers"]:
                value = int(value)
            elif key == "debug":
                value = to_bool(value)

            config[key] = value

    # Mask secret
    config["api_key"] = "****"

    return config
