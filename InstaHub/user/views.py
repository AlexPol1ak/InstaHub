from django.http import JsonResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserSerializer, RetrieveUserSerializer


@api_view(['GET'])
def test_view(request):
    return Response({'test': 'test page'}, status=status.HTTP_200_OK)


class CreateUserAPIView(APIView):
    """Регистрация нового пользвателя"""

    permission_classes = (AllowAny,)

    @extend_schema(request=UserSerializer, responses=UserSerializer, )
    def post(self, request):
        """Запрос для регистрации нового пользователя."""

        serializer_user = UserSerializer(data=request.data)
        if serializer_user.is_valid(raise_exception=True):
            serializer_user.save()
            serializer_user.validated_data.pop('password')
            return  Response(serializer_user.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveSelfUserAPIView(RetrieveAPIView):
    """Возвращает детальную информацию о зарегистрированном пользователе отправившим запрос"""
    queryset = User
    serializer_class = RetrieveUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        # self.check_object_permissions(self.request, obj)
        return obj


class RetrieveUserAPIView():
    pass

class UdpadeUserDataAPIView():
    pass

class UpdatePasswordAPIView():
    pass

class ResetPasswordAPIView():
    pass

class GetAllUserAPIView():
    pass

class DeactivateUserAPIView():
    pass

class AddAccountInstagramAPIView(): # Реализовать шифрование
    pass

class UpdateAccountInstgramAPIView(): # Реализовать шифрование
    pass

class DeleteAccountInstagramAPIView():
    pass