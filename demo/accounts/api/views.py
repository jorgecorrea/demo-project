from django.http import Http404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer, UserEmailValidateSerializer, UserPhoneValidateSerializer
from accounts.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    model = User
    serializer_class = UserSerializer


class UserEmailValidate(APIView):
    queryset = User.objects.all()

    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, user_id):
        # TODO add a hash token in validation to more security
        user = self.get_object(user_id)
        user.validated_email = True
        user.save()
        serializer = UserEmailValidateSerializer(user)
        return Response(serializer.data)


class UserPhoneValidate(APIView):
    queryset = User.objects.all()

    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, user_id):
        # TODO add a hash token in validation to more security
        user = self.get_object(user_id)
        user.validated_phone = True
        user.save()
        serializer = UserPhoneValidateSerializer(user)
        return Response(serializer.data)
