import factory
from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User
        abstract = False

    username = factory.Faker('word')
    password = factory.PostGenerationMethodCall('set_password', 'def123')
