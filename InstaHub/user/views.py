from django.http import JsonResponse
from django.shortcuts import render
from drf_multiple_model.views import FlatMultipleModelAPIView, ObjectMultipleModelAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.generics import RetrieveAPIView, get_object_or_404, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from user import utils, service, fake_serializers
from user.models import User, User_instagram_account
from user.paginators import GatAllUsersPagination
from user.permissions import IsAdminOrOwnerPermission, IsOwnerProfilePermission, IsOwnerInstagamPermission
from user.serializers import UserSerializer, RetrieveUserSerializer, UserUpdateDataSerializer, \
    UserUpdatePasswordSerializer, ResetPasswordSerializer, GetAllUserSerializer, DestroyOrDeactivateSerializer, \
    UserInstagramAccountSerializer

@extend_schema
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
    """Возвращает детальную информацию о зарегистрированном пользователе отправившим запрос."""

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
    permission_classes = (IsAuthenticated, IsAdminOrOwnerPermission)


class UdpadeUserDataAPIView(UpdateAPIView):
    """Изменяет информацию о пользователе."""

    queryset = User
    serializer_class = UserUpdateDataSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwnerPermission)


class UpdatePasswordAPIView(UpdateAPIView):
    """Изменяет пароль пользователя."""
    queryset = User
    serializer_class = UserUpdatePasswordSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwnerPermission)

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

                if user.email == serializer_data.validated_data['email']:
                        password :str = utils.PasswordGeneration.get_random_password(10)
                        user_message = service.MessagesSender(user=user)
                        res :str = user_message.send_email_reset_password(password=password)
                        user.set_password(password)
                        user.save()
                        return Response({'ok': 'password is reset'}, status=status.HTTP_200_OK)
                else:
                    raise ValueError('Invalid email')

            except User.DoesNotExist as e:
                return Response({
                                 'error': f'DoesNotExist: {str(e)}',
                                 'message': 'User not found'
                                 }, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({
                                'Error': 'ValueError',
                                'message': 'Invalid email'
                                })
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)



class GetAllUsersAPIView(ListAPIView):
    """Предоставляет список все пользователей."""
    queryset = User.objects.all()
    serializer_class = GetAllUserSerializer
    pagination_class = GatAllUsersPagination
    permission_classes = (IsAuthenticated, IsAdminUser )

@extend_schema_view(delete=extend_schema(request=DestroyOrDeactivateSerializer))
class DestroySelfAPIView(DestroyAPIView):
    """Удаление аккаунта пользователем."""
    queryset = User
    serializer_class = DestroyOrDeactivateSerializer
    pagination_class = (IsAuthenticated, IsOwnerProfilePermission)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj
    def destroy(self, request, *args, **kwargs):

        serializer_data = self.serializer_class(data=request.data)
        serializer_data.is_valid()
        password = serializer_data.validated_data.get('password', None)

        if not password:
            return Response({"PasswordError": "Enter your password"}, status=status.HTTP_409_CONFLICT)
        elif request.user.check_password(password):
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"PasswordError": "Wrong password"}, status=status.HTTP_423_LOCKED)


class DeactivateSelfAPIView(DestroySelfAPIView):
    """Деактивация аккаунта пользователем."""
    def perform_destroy(self, instance):
        instance.is_activ = False
        instance.save()


class DestroyUserAPIView(DestroyAPIView):
    """Удаление аккаунта пользователя администратором."""
    queryset = User
    pagination_class = (IsAuthenticated, IsAdminUser)


class DeactivateUserAPIView(DestroyUserAPIView):
    """Деактивация аккаунта пользователя администратором."""

    def perform_destroy(self, instance):
        instance.is_activ = False
        instance.save()



class UserInstagramAccountViewSet(viewsets.ModelViewSet):
    """Сохраняет, изменяет, удаляет, представляет для чтения пользовательские данные авторизации в instagram"""

    queryset = User_instagram_account.objects.all()
    serializer_class = UserInstagramAccountSerializer
    permission_classes = (IsAuthenticated,  IsOwnerInstagamPermission)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, user_id=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=False, methods=['patch', 'put'], url_name='change', url_path='change',)
    def change_inst_data(self,request,pk=None):
        """Изменяет пользовательские данные авторизации в instagram"""
        return super().partial_update(request, pk)

    @action(detail=False, methods=['delete'], url_name='delete', url_path='delete')
    def delete_inst_data(self,request, pk=None):
        """Удаляет пользовательские данные авторизации в instagram"""
        return super().destroy(request, pk)

@extend_schema(responses=fake_serializers.ResponseFakeSerializer)
class RetrieveSelfAllUserDataAPIView(FlatMultipleModelAPIView):
    """
    Возвращает все данные пользователя, а так же данные его учетной записи в instagram, если они были предоставлены.
    """
    permission_classes = (IsAuthenticated, IsOwnerInstagamPermission, IsOwnerProfilePermission )


    def get_querylist(self):
        """
        Динамическое формирование и объединение двух queryset:
        Личные данные пользователя и данные о его аккаунте instagram.
        Сериализация полученных данных.
        """

        querylist = (
            {'queryset': User.objects.filter(id=self.request.user.pk),
             'serializer_class':RetrieveUserSerializer,
             'label': 'User'
             },
            {'queryset': User_instagram_account.objects.filter(user_id=self.request.user.pk),
             'serializer_class': UserInstagramAccountSerializer,
             'label': 'Instagram'
             },
        )
        return querylist