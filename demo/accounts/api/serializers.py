import asyncio    # ANOTHER OPTION could be use celery that lets you more controlo over done or canceled tasks
from django.conf import  settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

# from smslib import sms_send   # INVENTED library name for the demo

from rest_framework import serializers
from accounts.models import User

loop = asyncio.get_event_loop()


class UserSerializer(serializers.ModelSerializer):
    validated_email = serializers.BooleanField(read_only=True)
    validated_phone = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "name", "surnames", "phone", "password",
                  "hobbies", "validated_email", "validated_phone")

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            surnames=validated_data['surnames'],
            phone=validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.save()
        if settings.DEBUG:
            print("send email")
            print("send SMS")
        else:
            msg = _("Follow this link %s/user/%s/email_validate for confirm your email" % (settings.SERVER_URL,
                                                                                           user.id))
            loop.run_in_executor(send_mail(_("User registered validate email"), msg, settings.FROM_MAIL, user.email))
            phone_sms = _("Follow this link %s/user/%s/phone_validate for confirm your phone" % (settings.SERVER_URL,
                                                                                                 user.id))
            #loop.run_in_executor(sms_send(user.phone, phone_sms))
        return user


class UserEmailValidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "email", "validated_email")

    def update(self, instance, validated_data):
        instance.validated_email = True
        instance.save()
        return instance


class UserPhoneValidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "email", "phone", "validated_phone")

    def update(self, instance, validated_data):
        instance.validated_email = True
        instance.save()
        return instance