from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Photo
from .serializers import SignUpUserSerializer, PhotoSerializer


class SignUpView(APIView):
    permission_classes = {permissions.AllowAny, }
    serializer_class = SignUpUserSerializer

    def post(self, request, format=None):
        userSerializer = self.serializer_class(data=request.data)
        if userSerializer.is_valid():
            user = userSerializer.save()
            token = RefreshToken.for_user(user)
            res = {
                "user": userSerializer.data,
                "token": {
                    "refresh": str(token),
                    "access": str(token.access_token)
                }
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoView(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()

# Create your views here.
