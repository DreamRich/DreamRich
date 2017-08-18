from django.db import models
from django.contrib.auth.models import User
from . import validators

class Country(models.Model):
 
    name = models.CharField(
        max_length=30
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
 
 
class City(models.Model):
    name = models.CharField(
        max_length=58
    )
 
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE
    )
 
    def __str__(self):
        return self.name

class Address(models.Model):

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE
    )

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

    def __str__(self):
        return "cep: {}, nº: {}".format(self.cep, self.number)


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

    hometown = models.CharField(
        max_length=50
    )

    hometown = models.ForeignKey(City, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, validators=[validators.validate_CPF])

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
        related_name='client_spouse'
    )

    address = models.ManyToManyField(
        Address
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pk:
            self.login,check = User.objects.get_or_create(username=self.cpf)
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
