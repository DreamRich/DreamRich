from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from json import dumps


class AuthView(APIView):

    def post(self, request):
        """Method to change the password value"""

        try:
            user = get_object_or_404(User, pk=request.data.get('userid'))
            data = request.data

            if data.get('new_password') != data.get('new_password_confirmation'):
                return Response(dumps({'detail': 'different password'}), status=400)

            elif user.check_password(data.get('password')):
                user.set_password(data.get('new_password'))
                user.save()
                return Response(dumps({'detail': 'password changed'}), status=200)

            return Response(dumps({'detail': 'invalid password'}), status=400)

        except User.DoesNotExist:
            return Response(dumps({'detal': 'user not found'}), status=404)

    def get(self, request, email=None):
        """Reset password sending in e-mail"""
        user = get_object_or_404(User, email=request.GET.get('email'))
        # send e-mail
        print(user)
        import json
        return Response(json.dumps({'user': user.username}), status=200)
