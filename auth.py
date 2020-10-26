import os
import json
from flask import request, _request_ctx_stack, abort, jsonify
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'dev-s9xqvku2.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'agency'

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        abort(401)
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        abort(401)
    elif len(parts) > 2:
        abort(401)
    elif len(parts) == 1:
        abort(401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(404)
    if permission not in payload['permissions']:
        abort(401)


def verify_decode_jwt(token):
    url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(url.read())
    header_unverified = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in header_unverified:
        abort(401)
    for me in jwks['keys']:
        if me['kid'] == header_unverified['kid']:
            rsa_key = {
                'kty': me['kty'],
                'kid': me['kid'],
                'use': me['use'],
                'n': me['n'],
                'e': me['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms='RS256',
                audience=f'{API_AUDIENCE}',
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            abort(403)
    abort(401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
