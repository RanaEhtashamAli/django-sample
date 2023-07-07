from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from rest_framework import viewsets, permissions, status
from .serializer import UserSerializer, UserAuthedSerializer
from .permissions import CustomPermission
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action in ('authed', 'retrieve', 'list'):
            return UserAuthedSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'authed':
            self.permission_classes = [permissions.IsAuthenticated, ]
        elif self.action in ('list', 'create'):
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        elif self.action in ('retrieve', 'update'):
            self.permission_classes = [permissions.IsAuthenticated, CustomPermission]
        return super(self.__class__, self).get_permissions()

    @action(detail=False, methods=['get'])
    def authed(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
