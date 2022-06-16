from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


PHONE_REGEX = RegexValidator(regex='^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$')


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
    )
    surnames = models.CharField(
        verbose_name=_('surnames'),
        max_length=200,
    )
    phone = models.CharField(
        verbose_name=_('phone'),
        max_length=12,
        validators=[PHONE_REGEX]
    )
    hobbies = models.TextField(
        verbose_name=_('hobbies'),
    )
    validated_email = models.BooleanField(
        verbose_name=_('email validated'),
        default=False
    )
    validated_phone = models.BooleanField(
        verbose_name=_('phone validated'),
        default=False
    )
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email
