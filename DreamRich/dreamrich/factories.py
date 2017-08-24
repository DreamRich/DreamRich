import factory
from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker('first_name')
    password = factory.PostGenerationMethodCall('set_password', 'qwer1234')

    is_superuser = True
    is_staff = True
    is_active = True
