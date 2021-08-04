from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Photo

class SignUpUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=128)
    password = serializers.CharField(required=True, min_length=8, max_length=32, write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'image', 'filename', 'added', 'owner')
        extra_kwargs = {
            'image': {'write_only': True}
        }