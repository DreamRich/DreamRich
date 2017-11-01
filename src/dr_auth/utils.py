from dr_auth.serializers import BaseUserSerializer


def jwt_response_payload_handler(token, user=None, unused_request=None):
    context = BaseUserSerializer(user.baseuser).data
    context['token'] = token

    return context
