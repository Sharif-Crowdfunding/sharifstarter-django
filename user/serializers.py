from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'], username=validated_data['email'], password=validated_data['password'],
                                        first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        return user
