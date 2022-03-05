import jwt
import logging
import datetime

KEY = 'OPENnuclearNetwork'

def is_dev():
    # hydrate if profuction or dev
    return True

def generate_auth_token(user_id, expires=True):
    LIFESPAN = 60 * 15  # expires after 15 minutes
    now = datetime.datetime.utcnow()
    payload = {'iat': now, 'user_id': user_id, 'iss': 'OpenNuclearNetwork'}
    if expires:
        payload['exp'] = now + datetime.timedelta(days=0, seconds=LIFESPAN)
    token = jwt.encode(payload, KEY, algorithm='HS256')

    return token


def verify_auth_token(auth_token):
    try:
        decoded_token = jwt.decode(auth_token, KEY, algorithms='HS256')
    except (jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
            jwt.InvalidIssuerError,
            jwt.InvalidSignatureError) as e:
        logging.warning('Error When Verifying Auth Token: %s' % e)
        return {'is_valid': False, 'response': e}
    return {'is_valid': True, 'response': decoded_token}
