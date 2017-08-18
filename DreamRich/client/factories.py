import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker('word')
    password = factory.PostGenerationMethodCall('set_password',
                                                'default123')
    email = factory.LazyAttribute(lambda x: '{}@mail.com'.format(x.username))
    is_staff = True
    is_superuser = True
