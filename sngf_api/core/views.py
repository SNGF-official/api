from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view()
@permission_classes([AllowAny])
def ping(request):
    return Response("pong")
