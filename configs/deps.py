from typing import Annotated
from jose import JWTError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException, Depends
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import json, base64, jwt, json
from urllib.request import urlopen
from jwt.exceptions import DecodeError, InvalidSignatureError, ExpiredSignatureError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user_azure(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        tenant_id = "0ae51e19-07c8-4e4b-bb6d-648ee58410f4"
        jwks_url = f"https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys"
        issuer_url = f"https://login.microsoftonline.com/{tenant_id}/v2.0"

        jwks = json.loads(urlopen(jwks_url).read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = find_rsa_key(jwks, unverified_header)
        public_key = rsa_pem_from_jwk(rsa_key)

        return jwt.decode(
        token,
        public_key,
        verify=True,
        algorithms=["RS256"],
        issuer=issuer_url,
        options={"verify_aud": False,}
        )
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (JWTError, InvalidSignatureError, DecodeError) as e:
        raise credentials_exception

def find_rsa_key(jwks, unverified_header):
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            return {
              "kty": key["kty"],
              "kid": key["kid"],
              "use": key["use"],
              "n": key["n"],
              "e": key["e"]
            }

def ensure_bytes(key):
    if isinstance(key, str):
        key = key.encode('utf-8')
    return key


def decode_value(val):
    decoded = base64.urlsafe_b64decode(ensure_bytes(val) + b'==')
    return int.from_bytes(decoded, 'big')


def rsa_pem_from_jwk(jwk):
    return RSAPublicNumbers(
        n=decode_value(jwk['n']),
        e=decode_value(jwk['e'])
    ).public_key(default_backend()).public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )