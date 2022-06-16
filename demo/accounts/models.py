from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, _user_has_perm, _user_has_module_perms
from django.utils.translation import gettext_lazy as _


PHONE_REGEX = RegexValidator(regex='^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$')


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


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
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Active superusers have all permissions.
        if self.is_active and self.is_admin:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        if self.is_active and self.is_admin:
            return True
        return _user_has_module_perms(self, app_label)

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
