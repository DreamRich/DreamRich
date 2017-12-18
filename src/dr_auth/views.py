from json import dumps
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.contrib.auth.models import User


class AuthView(APIView):

    def post(self, request):
        """Method to change the password value"""

        try:
            data = request.data
            user = User.objects.get(pk=data.get('userid'))

            response = Response()
            if data.get('new_password') != data.get('new_password' +
                                                    '_confirmation'):

                response = Response(
                    dumps({'detail': 'different password'}),
                    status=400
                )

            elif user.check_password(data.get('password')):
                user.set_password(data.get('new_password'))
                user.save()
                response = Response(
                    dumps({'detail': 'password changed'}),
                    status=200
                )

            else:
                response = Response(dumps({'detail': 'invalid password'}),
                                    status=400)

        except User.DoesNotExist:
            response = Response(dumps({'detail': 'user not found'}),
                                status=404)

        return response

    def get(self, request, email=None):
        """Reset password sending in e-mail"""

        user = User.objects.filter(email=request.GET.get('email'))

        if user.count() == 1 and user.first() is not None:
            user = user.first()

            random_password = User.objects.make_random_password()
            user.set_password(random_password)
            user.save()

            message = """Olá,\nSua senha foi resetada, acesse a plataforma
                         no link http://127.0.0.1/user/password e troque a
                         senha\nSua nova senha é:\n {}\nAtenciosamente,
                         \nEquipe Dream Rich.""".format(random_password)

            email = EmailMessage('Password reset',
                                 message, to=[user.email])
            email.send()

            return Response(dumps({'detail': 'email sent'}), status=200)

        return Response(dumps({'detail': 'user not found'}), status=404)


# Create your views here.
