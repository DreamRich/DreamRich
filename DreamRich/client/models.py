from django.db import models


class Address(models.Model):

    cep = models.PositiveIntegerField()

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

    cpf = models.CharField(
        max_length=14
    )  # max_length considering '.' and '-'

    telephone = models.CharField(
        max_length=19
    )  # considering +55

    email = models.EmailField()

    hometown = models.CharField(
        max_length=50
    )

    address = models.ManyToManyField(
        Address
    )

    def __str__(self):
        return "name: {} cpf: {}".format(self.name, self.cpf)


class ActiveClient(Client):

    id_document = models.ImageField(
        upload_to='public/id_documents'
    )

    proof_of_address = models.ImageField(
        upload_to='public/proof_of_address'
    )


class Spouse(Client):

    active_clients = models.ForeignKey(
        ActiveClient,
        related_name='spouse'
    )


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

    birthday = models.DateField(
        'Data de nascimento'
    )

    client = models.ForeignKey(
        Client,
        related_name='dependents',
        on_delete=models.CASCADE
    )


class BankAccount(models.Model):

    client = models.OneToOneField(
        Client,
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
