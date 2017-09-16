from django.db import models
from dr_auth.models import BaseUser
from dreamrich import validators


class Country(models.Model):

    name = models.CharField(
        max_length=30
    )

    abbreviation = models.CharField(
        max_length=2
    )

    def __str__(self):
        return self.name


class State(models.Model):

    name = models.CharField(
        max_length=30
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


class ClientBase(models.Model):

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
        validators=[validators.validate_phonenumber]
    )  # considering +55

    cpf = models.CharField(
        max_length=14,
        validators=[validators.validate_cpf]
    )

    hometown = models.CharField(
        max_length=50
    )

    def __str__(self):
        return "name: {} cpf: {}".format(self.name, self.cpf)


class ActiveClient(ClientBase, BaseUser):

    id_document = models.ImageField(
        upload_to='public/id_documents'
    )

    proof_of_address = models.ImageField(
        upload_to='public/proof_of_address'
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        self.username = self.cpf
        self.full_clean()

        super(ActiveClient, self).save(*args, **kwargs)


class Client(ClientBase):

    active_spouse = models.OneToOneField(
        ActiveClient,
        on_delete=models.CASCADE,
        related_name='spouse',
        null=True,
        blank=True,
    )
    
    def save(self, *args, **kwargs):
        self.full_clean()
			
        super(Client, self).save(*args, **kwargs)


class Dependent(models.Model):

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


class BankAccount(models.Model):

    active_client = models.OneToOneField(
        ActiveClient,
        related_name='client_bank_account',
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

    def save(self, *args, **kwargs):
        self.full_clean()
			
        super(BankAccount, self).save(*args, **kwargs)

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
        ActiveClient,
        related_name='client_address'
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
