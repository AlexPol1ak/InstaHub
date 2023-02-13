from django.http import JsonResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, get_object_or_404, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from user import utils, service
from user.models import User
from user.paginators import GatAllUsersPagination
from user.permissions import IsAdminOrOwner
from user.serializers import UserSerializer, RetrieveUserSerializer, UserUpdateDataSerializer, \
    UserUpdatePasswordSerializer, ResetPasswordSerializer, GetAllUserSerializer


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
        self.check_object_permissions(self.request, obj)
        return obj


class RetrieveUserAPIView(RetrieveAPIView):
    """
    Возвращает детальную информацию о зарегистрированном пользователе по его id.
    Администратор может просмотреть информацию о любом пользователе.
    Обычный пользователь - только свою.
    """

    queryset = User
    serializer_class = RetrieveUserSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwner)


class UdpadeUserDataAPIView(UpdateAPIView):
    """Изменяет информацию о пользователе."""

    queryset = User
    serializer_class = UserUpdateDataSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwner)


class UpdatePasswordAPIView(UpdateAPIView):
    """Изменяет пароль пользователя."""
    queryset = User
    serializer_class = UserUpdatePasswordSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwner)

    # Запрещает передачу в запросе неполных данных. Например, новый пароль без указания старого.
    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

class ResetPasswordAPIView(APIView):
    """
    Сбрасывает пароль пользователя при предоставлении логина и email.
    Если логин и email совпадает с аккаунтом определенного пользователя, то текущий пароль сбрасывается,
    генерируется и устанавливается случайный пароль,котрый отправляется на email.
    """

    permission_classes = (AllowAny,)

    @extend_schema(responses=ResetPasswordSerializer)
    def post(self, request):
        """Запрос для сброса пароля."""

        serializer_data = ResetPasswordSerializer(data=request.data)
        if serializer_data.is_valid(raise_exception=True):
            try:
                user = User.objects.get(login=serializer_data.validated_data['login'])
            except Exception as e:
                return Response({'Error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

            if user.email == serializer_data.validated_data.get('email', None):
                try:
                    password :str = utils.PasswordGeneration.get_random_password(10)

                    user_message = service.MessagesSender(user=user)
                    res :str = user_message.send_email_reset_password(password=password)
                except Exception as e:
                    return Response({'Error': e.__repr__()})
                else:
                    user.set_password(password)
                    user.save()
                    return Response(res, status=status.HTTP_202_ACCEPTED)

            else:
                return Response({'Error': 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)



class GetAllUsersAPIView(ListAPIView):
    """Предоставляет список все пользователей"""
    queryset = User.objects.all()
    serializer_class = GetAllUserSerializer
    pagination_class = GatAllUsersPagination
    permission_classes = (IsAuthenticated, IsAdminUser )




class DeactivateUserAPIView():
    pass

class AddAccountInstagramAPIView(): # Реализовать шифрование
    pass

class UpdateAccountInstgramAPIView(): # Реализовать шифрование
    pass

class DeleteAccountInstagramAPIView():
    pass