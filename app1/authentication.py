import jwt, datetime
import uuid
from django.conf import settings


def create_access_token(username,account_type):
    token_id = str(uuid.uuid1())
    return jwt.encode({
        'username': username,
        'account_type': account_type,
        'token_id': token_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow()
    }, settings.ACCESS_SECRET, algorithm='HS256')

def decode_access_token(token,verify=True):
    try:
        payload = jwt.decode(token, settings.ACCESS_SECRET, algorithms='HS256',options={'verify_exp': verify})
        return payload
    except:
        return

# def create_refresh_token(id):
#     return jwt.encode({
#         'user_id': id,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
#         'iat': datetime.datetime.utcnow()
#     }, 'refresh_secret', algorithm='HS256')

# def decode_refresh_token(token):
#     try:
#         payload = jwt.decode(token, 'refresh_secret', algorithms='HS256')

#         return payload['user_id']
#     except:
#         raise exceptions.AuthenticationFailed('unauthenticated')