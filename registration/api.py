from django.contrib.auth import authenticate, login, logout
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_406_NOT_ACCEPTABLE
from rest_framework.views import APIView

from registration.serializers import LoginSerializer


class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        if request.user.is_authenticated:
            return Response({'message': 'Already logged in'}, status=HTTP_406_NOT_ACCEPTABLE)

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        user = authenticate(username=data['username'], password=data['password'])

        if user:
            login(request, user)
            return Response()
        else:
            return Response({'message': 'Invalid username or password'}, status=HTTP_403_FORBIDDEN)


class LogoutView(APIView):
    permission_classes = []

    def post(self, request: Request):
        if not request.user.is_authenticated:
            return Response({'message': 'Already logged out'}, status=HTTP_406_NOT_ACCEPTABLE)

        logout(request)
        return Response()
