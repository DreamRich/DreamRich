from django.db import models
from dr_auth.models import BaseUser
from dreamrich import validators
from dreamrich import models as base_models


class Country(base_models.BaseModel):

    name = models.CharField(
        max_length=55
    )

    abbreviation = models.CharField(
        max_length=3
    )

    def __str__(self):
        return self.name


class State(base_models.BaseModel):

    name = models.CharField(
        max_length=55
    )

    abbreviation = models.CharField(
        max_length=2
    )

    country = models.ForeignKey(
        Country,
        related_name='country_states',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class ClientBase(base_models.BaseModel):

    class Meta:
        abstract = True

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
        max_length=19,
        validators=[validators.validate_phone_number]
    )  # considering +55

    cpf = models.CharField(
        unique=True,
        max_length=14,
        validators=[validators.validate_cpf]
    )

    hometown = models.CharField(
        max_length=50
    )

    def __str__(self):
        return "{} cpf: {}".format(self.name, self.cpf)


class ActiveClient(BaseUser, ClientBase):

    id_document = models.ImageField(
        null=True,
        blank=True
    )

    proof_of_address = models.ImageField(
        null=True,
        blank=True
    )

    def __str__(self):
        return "{0.name} {0.username}".format(self)


class Client(ClientBase):

    active_spouse = models.OneToOneField(
        ActiveClient,
        on_delete=models.CASCADE,
        related_name='spouse',
        null=True,
        blank=True,
    )


class Dependent(base_models.BaseModel):

    name = models.CharField(
        max_length=30
    )

    surname = models.CharField(
        max_length=50
    )

    birthday = models.DateField(
        'Data de nascimento',
    )

    active_client = models.ForeignKey(
        ActiveClient,
        related_name='dependents',
        on_delete=models.CASCADE
    )


class BankAccount(base_models.BaseModel):

    active_client = models.OneToOneField(
        ActiveClient,
        related_name='bank_account',
        on_delete=models.CASCADE
    )

    agency = models.CharField(
        max_length=6,
        validators=[validators.validate_agency]
    )  # BR pattern: '[4alg]-[1dig]'

    account = models.CharField(
        max_length=13,
        validators=[validators.validate_account]
    )  # BR pattern: '[8alg]-[1dig]'

    def __str__(self):
        return str(self.agency) + ' ' + str(self.account)


class Address(base_models.BaseModel):

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

    active_client = models.ForeignKey(
        ActiveClient,
        related_name='addresses'
    )

    city = models.CharField(
        max_length=50
    )

    state = models.ForeignKey(
        State,
        related_name='state_addresses'
    )

    def __str__(self):
        return "cep: {}, nº: {}".format(self.cep, self.number)
