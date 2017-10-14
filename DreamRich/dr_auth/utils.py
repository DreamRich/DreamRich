from dr_auth.serializers import BaseUserSerializer


def jwt_response_payload_handler(token, user=None, request=None):  # pylint: disable=unused-argument
    context = BaseUserSerializer(user.baseuser).data
    context['token'] = token
    return context
