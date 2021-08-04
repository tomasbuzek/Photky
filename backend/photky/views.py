from django.http import HttpResponse

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Photo
from .serializers import SignUpUserSerializer, PhotoSerializer


class SignUpView(APIView):
    """User registration REST API view."""
    permission_classes = {permissions.AllowAny, }
    serializer_class = SignUpUserSerializer

    def post(self, request, format=None):
        """Signup HTTP POST method which creates new user
        and returns created user data and JWT token.

        Returns code 201 (CREATED) on success
        and code 400 (BAD REQUEST) otherwise."""
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
    """Photo REST API view.

    For authenticated users only."""
    permission_classes = {permissions.IsAuthenticated, }
    serializer_class = PhotoSerializer

    def get_queryset(self):
        """Returns all photos with the owner set to the currently authenticated user."""
        return Photo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Saving Photo and setting the owner to the currently authenticated user."""
        return serializer.save(owner=self.request.user)

    @action(methods=['get'], detail=True)
    def image(self, request, pk=None):
        """Photo image HTTP Get method.

        Returns code 200 (OK) and image data and content type of the Photo with the ID=pk,
        code 404 (NOT FOUND) when the Photo with the ID=pk does not exist
        and code 403 (FORBIDDEN) when the currently authenticated user is not the owner.
        """
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
        """Photo thumbnail HTTP Get method.

        Returns code 200 (OK) and thumbnail data and content type of the Photo with the ID=pk,
        code 404 (NOT FOUND) when the Photo with the ID=pk does not exist
        and code 403 (FORBIDDEN) when the currently authenticated user is not the owner.
        """
        try:
            photo = Photo.objects.get(id=pk)
        except:
            return Response("Photo not found", status=status.HTTP_404_NOT_FOUND)

        if photo.owner == self.request.user:
            # Create the thumbnail if it does not exist.
            if not photo.thumbnail:
                photo.create_thumbnail()
            return HttpResponse(photo.thumbnail, content_type="image/jpeg")
        else:
            return Response("Access to the photo is forbidden.", status=status.HTTP_403_FORBIDDEN)
