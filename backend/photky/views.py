from django.http import HttpResponse

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
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
    permission_classes = {permissions.IsAuthenticated, }
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    @action(methods=['get'], detail=True)
    def image(self, request, pk=None):
        try:
            photo = Photo.objects.get(id=pk)
        except:
            return Response("Photo not found", status=status.HTTP_404_NOT_FOUND)

        if photo.owner == self.request.user:
            return HttpResponse(photo.image, content_type=photo.content_type)
        else:
            return Response("Access to the photo is forbidden.", status=status.HTTP_403_FORBIDDEN)

    @action(methods=['get'], detail=True)
    def thumbnail(self, request, pk=None):
        try:
            photo = Photo.objects.get(id=pk)
        except:
            return Response("Photo not found", status=status.HTTP_404_NOT_FOUND)

        if photo.owner == self.request.user:
            if not photo.thumbnail:
                photo.create_thumbnail()
            return HttpResponse(photo.thumbnail, content_type="image/jpeg")
        else:
            return Response("Access to the photo is forbidden.", status=status.HTTP_403_FORBIDDEN)
