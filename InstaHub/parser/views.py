from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from parser.models import InstaHubInstagramAccounts, TrackedUsers
from parser.paginators import InstagramAccountsPagination
from parser.serializers import ServiceInstagramAccountSerializer, ServiceInstagramAccountBlockedSerializer, \
     AddTrackedUserSerializer


@api_view(['GET'])
def test_view_parser(request):
    print(request.user)
    return Response({'test_pages_parser': str(request.user)})


class ServiceInstagramAccountViewSet(viewsets.ModelViewSet):
    """
    Сохраняет, изменяет, удаляет, представляет для чтения данные авторизации в instagram,
    аккаунтов сервиса.
    """

    queryset = InstaHubInstagramAccounts.objects.all()
    serializer_class = ServiceInstagramAccountSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    pagination_class = InstagramAccountsPagination

    @action(detail=True, methods=['patch', 'put'], url_name='blocked', url_path='blocked', )
    def blocked_instagram(self, request, pk=None):
        """Помечает аккаунт instagram как заблокированный или разблокированный."""

        try:
            account = self.get_object()

            serializer_data = ServiceInstagramAccountBlockedSerializer(data=request.data)
            if serializer_data.is_valid():
                blocked = serializer_data.validated_data['blocked']
                account.blocked = blocked
                account.save()
                response_data = ServiceInstagramAccountBlockedSerializer(account)
            else:
                return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(response_data.data, status=status.HTTP_200_OK)


class AddTrackedUserAPIView(CreateAPIView):
    """
    Добавляет пользователя instagram в список отслеживаемых или получения списка всех отслеживаемых
    """

    queryset = TrackedUsers.objects.all()
    serializer_class = AddTrackedUserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def post(self, request, *args, **kwargs):
        """Добавляет пользователя instagram  в список отслеживаемых."""

        fake_user = self._get_user_instagram()

        data = self.serializer_class(data=request.data)
        if data.is_valid(raise_exception=True):
            try:
                obj = TrackedUsers(id_instagram= fake_user.id,
                                    user_name=data.validated_data['user_name'],
                                    profile_link=fake_user.profile_link,
                                    )
                obj.save()
                obj.user.add(request.user)
                response_data = self.serializer_class(obj).data
            except TypeError as e:
                return Response({
                    'Error': 'Communication setup error',
                    'detail': str(e)
                                 })
            except IntegrityError as e:
                obj = TrackedUsers.objects.get(id_instagram=2487)
                obj.user.add(request.user)
                response_data = self.serializer_class(obj).data

        return Response(response_data)

    def _get_user_instagram(self, user_name: str= ''):
        """Получает данные пользователя instagram."""

        # Временный фальшивый пользователь, заменить позже на парсинг реального
        from parser.utils.fake_data_creation import CreateFakeInstagramProfiles
        user = CreateFakeInstagramProfiles(language='ru', gender='male')
        return user