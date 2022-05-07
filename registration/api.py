from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_406_NOT_ACCEPTABLE
from rest_framework.views import APIView

from registration.serializers import LoginSerializer


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'message': 'Already logged in'}, status=HTTP_406_NOT_ACCEPTABLE)
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        user = authenticate(username=data['username'], password=data['password'])

        if user:
            login(request, user)
            return Response(status=HTTP_200_OK)
        else:
            return Response({'message': 'Invalid username or password'}, status=HTTP_403_FORBIDDEN)
