from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from parser.models import InstaHub_instagram_accounts
from parser.paginators import InstagramAccountsPagination
from parser.serializers import ServiceInstagramAccountSerializer, ServiceInstagramAccountBlockedSerializer


@api_view(['GET'])
def test_view_parser(request):
    print(request.user)
    return Response({'test_pages_parser': str(request.user)})


class ServiceInstagramAccountViewSet(viewsets.ModelViewSet):
    """
    Сохраняет, изменяет, удаляет, представляет для чтения данные авторизации в instagram,
    аккаунтов сервиса.
    """

    queryset = InstaHub_instagram_accounts.objects.all()
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



