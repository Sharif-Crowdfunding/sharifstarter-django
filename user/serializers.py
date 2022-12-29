from rest_framework import serializers

from wallet.models import create_wallet
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        wallet = create_wallet(validated_data['password'])
        user = User.objects.create_user(email=validated_data['email'], username=validated_data['username'],
                                        password=validated_data['password'],
                                        first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                                        wallet=wallet)
        return user
