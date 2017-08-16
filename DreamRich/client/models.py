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
        max_length=100
    )

    id_document = models.ImageField(
        upload_to='public/id_documents'
    )

    proof_of_address = models.ImageField(
        upload_to='public/proof_of_address'
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

    address = models.ManyToManyField(
        Address
    )

    def __str__(self):
        return self.name


class Dependent(models.Model):

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )

    birthday = models.DateField(
        'Data de nascimento'
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
