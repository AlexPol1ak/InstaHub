from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_view_parser(request):
    print(request.user)
    return Response({'test_pages_parser': str(request.user)})

