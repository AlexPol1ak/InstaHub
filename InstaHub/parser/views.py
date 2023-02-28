from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from parser.instagram_parser.inst_parser import InstagramParser
from parser.models import InstaHubInstagramAccounts, TrackedUsers
from parser.paginators import InstagramAccountsPagination
from parser.serializers import ServiceInstagramAccountSerializer, ServiceInstagramAccountBlockedSerializer, \
    AddTrackedUserSerializer
from user.models import User_instagram_account


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
        """Добавляет пользователя instagram в список отслеживаемых."""
        pass


class DeleteTrackedUserAPIView():
    """Удаляет пользователя instagram из списка отслеживаемых."""
    pass


class MyListTrackedUsersAPIView():
    """Возвращает список отслеживаемых."""
    pass


class NewFollowersAndUnfollowersAPIView():
    """
    Возвращает список новых подписчиков и тех кто отписался отслеживаемого пользователя instagram.
    """
    pass


class NewFollowingAndUnFollowingAPIView():
    """
    Возвращает список новых подписок и отписок отслеживаемого пользователя instagram.
    """
    pass


class SharedFollowersAPIView():
    """Возвращает список общих подписчиков между двумя пользователями Instagram."""
    pass


class SharedFollowingAPIView():
    """Возвращает список общих подписок между двумя пользователями."""
    pass


class SharedFollowersAndFollowingAPIView():
    """
    Возвращает список общих подписок и подписчиков между двумя пользователями instagram.
    """
    pass


class DownloadPhotoAPIView():
    """Возвращает фото из публикации."""
    pass


class DownloadVideoAPIView():
    """Возвращает видео Reels из публикации."""
    pass

class LikedPublicationsAPIView():
    """Возвращает количество лайков и список лайкнувших публикацию"""
    pass

class CommentPublicationsAPIView():
    """Возвращает количество коменатриев к публикации и комментаторов."""
    pass
