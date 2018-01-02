from django.db import models
from dreamrich import validators
from dreamrich import models as base_models
from dr_auth.models import BaseUser
from dr_auth.models_permissions import (
    CLIENT_MODEL_PERMISSIONS,
    CLIENT_DEFAULT_CODENAMES_PERMISSIONS
)


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

    class Meta:
        permissions = CLIENT_MODEL_PERMISSIONS

    id_document = models.ImageField(
        null=True,
        blank=True
    )

    proof_of_address = models.ImageField(
        null=True,
        blank=True
    )

    default_permissions_codenames = CLIENT_DEFAULT_CODENAMES_PERMISSIONS

    @property
    def is_complete(self):
        if hasattr(self, 'financial_planning'):
            return self.financial_planning.is_complete()
        return False

    def __str__(self):
        return "{0.name} {0.username}".format(self)


class Client(ClientBase):

    active_spouse = models.OneToOneField(
        'ActiveClient',
        on_delete=models.CASCADE,
        related_name='spouse',
        null=True,
        blank=True,
    )


class Dependent(base_models.BaseModel):

    active_client = models.ForeignKey(
        ActiveClient,
        related_name='dependents',
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=30
    )

    surname = models.CharField(
        max_length=50
    )

    birthday = models.DateField(
        'Data de nascimento',
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

    joint_account = models.BooleanField(default=False)

    account = models.CharField(
        max_length=13,
        validators=[validators.validate_account]
    )  # BR pattern: '[8alg]-[1dig]'

    def __str__(self):
        return '{0.agency} {0.account}'.format(self)


class Address(base_models.BaseModel):

    active_client = models.ForeignKey(
        ActiveClient,
        related_name='addresses'
    )

    state = models.ForeignKey(
        'State',
        related_name='state_addresses'
    )

    type_of_address = models.CharField(
        max_length=20
    )  # work or residential

    neighborhood = models.CharField(
        max_length=30
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

    city = models.CharField(
        max_length=50
    )

    def __str__(self):
        return "cep: {}, nº: {}".format(self.cep, self.number)


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

    country = models.ForeignKey(
        Country,
        related_name='country_states',
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=55
    )

    abbreviation = models.CharField(
        max_length=2
    )

    def __str__(self):
        return self.name
