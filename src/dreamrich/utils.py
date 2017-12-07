from rest_framework_jwt.settings import api_settings
from rest_framework.test import APIClient

def get_token(user):
    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    token = api_settings.JWT_ENCODE_HANDLER(payload)
    return token

def authenticate_user(user):
    django_client = apiclient()

    user_token = get_token(user)
    token = 'jwt {}'.format(user_token)
    django_client.credentials(http_authorization=token)

    return token

