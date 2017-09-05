import re

from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

ERROR_MESSAGES = {
    'invalid': _("Invalid CPF number."),
    'digits_only': _("This field requires only numbers."),
    'max_digits': _("This field requires exactly 11 digits."),
}


def verifying_digit_maker(digit):
    if digit >= 2:
        return 11 - digit
    return 0


def validate_cpf(value):
    """
    Value can be either a string in the format XXX.XXX.XXX-XX or an
    11-digit number.
    """

    if value in EMPTY_VALUES:
        return u''
    if not value.isdigit():
        value = re.sub("[-\.]", "", value)
    orig_value = value[:]
    try:
        int(value)
    except ValueError:
        raise ValidationError(ERROR_MESSAGES['digits_only'])
    if len(value) != 11:
        raise ValidationError(ERROR_MESSAGES['max_digits'])
    orig_dv = value[-2:]

    first_digit_verify = sum([i * int(value[idx])
                              for idx, i in enumerate(range(10, 1, -1))])
    first_digit_verify = verifying_digit_maker(first_digit_verify % 11)
    value = value[:-2] + str(first_digit_verify) + value[-1]
    seccond_digit_verify = sum([i * int(value[idx])
                                for idx, i in enumerate(range(11, 1, -1))])
    seccond_digit_verify = verifying_digit_maker(seccond_digit_verify % 11)
    value = value[:-1] + str(seccond_digit_verify)
    if value[-2:] != orig_dv:
        raise ValidationError(ERROR_MESSAGES['invalid'])

    return orig_value

def validate_phonenumber(phone_number):
    for char in phone_number:
        if not char.isdigit():
            raise ValidationError("Phone number must be number") 
             

def validate_agency(agency):
    #print("Entrouuu")
    #agency = RegexValidator('\b\d{4}[-]?\d{1}\b', "Hashtag doesn't comply.")
    for char in phone_number:
        if not char.isdigit():
            raise ValidationError("Phone number must be number")