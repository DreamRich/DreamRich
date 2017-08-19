from django.db import models
from django.contrib.auth.models import User
from . import validators


class Country(models.Model):

    name = models.CharField(
        max_length=30
    )

    state_acronym = models.CharField(
        max_length=2
    )

    def __str__(self):
        return self.name


class State(models.Model):

    name = models.CharField(
        max_length=30
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Client(models.Model):

    name = models.CharField(
        max_length=30
    )

    surname = models.CharField(
        max_length=50
    )

    birthday = models.DateField(
        'Data de nascimento'
    )

    profession = models.CharField(
        max_length=200
    )

    telephone = models.CharField(
        max_length=19
    )  # considering +55

    email = models.EmailField()

    cpf = models.CharField(
        max_length=14,
        validators=[validators.validate_CPF]
    )

    hometown = models.CharField(
        max_length=50
    )

    def __str__(self):
        return "name: {} cpf: {}".format(self.name, self.cpf)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Client, self).save()


class ActiveClient(Client):

    login = models.OneToOneField(User, null=True, blank=True)

    id_document = models.ImageField(
        upload_to='public/id_documents'
    )

    proof_of_address = models.ImageField(
        upload_to='public/proof_of_address'
    )

    spouse = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='active_spouse'
    )

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.pk:
            self.login, check = User.objects.get_or_create(username=self.cpf)
            self.login.set_password('123456')
            self.login.save()

        super(ActiveClient, self).save(*args, **kwargs)


class Dependent(models.Model):

    name = models.CharField(
        max_length=30
    )

    surname = models.CharField(
        max_length=50
    )

    birthday = models.DateField(
        'Data de nascimento'
    )

    active_client = models.ForeignKey(
        ActiveClient,
        related_name='dependents',
        on_delete=models.CASCADE
    )


class BankAccount(models.Model):

    active_client = models.OneToOneField(
        ActiveClient,
        on_delete=models.CASCADE
    )  # 1-to-1

    agency = models.CharField(
        max_length=6
    )  # BR pattern: '[4alg]-[1dig]'

    account = models.CharField(
        max_length=10
    )  # BR pattern: '[8alg]-[1dig]'

    def __str__(self):
        return str(self.agency) + ' ' + str(self.account)


class Address(models.Model):

    type_of_address = models.CharField(
        max_length=20
    )  # work or residential

    neighborhood = models.CharField(
        max_length=20
    )

    detail = models.CharField(
        max_length=50
    )

    cep = models.CharField(
        max_length=9
    )

    number = models.IntegerField()

    complement = models.CharField(
        max_length=20
    )

    client = models.ManyToManyField(
        ActiveClient
    )

    city = models.CharField(
        max_length=50
    )

    state = models.ForeignKey(
        State,
        related_name='state_addresses'
    )

    client = models.ForeignKey(
        ActiveClient,
        related_name='client_addresses'
    )

    def __str__(self):
        return "cep: {}, nº: {}".format(self.cep, self.number)
