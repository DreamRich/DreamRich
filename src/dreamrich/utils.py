from rest_framework_jwt.settings import api_settings


def get_token(user):
    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    token = api_settings.JWT_ENCODE_HANDLER(payload)
    return token
