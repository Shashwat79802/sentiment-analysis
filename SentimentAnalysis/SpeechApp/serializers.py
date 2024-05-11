from rest_framework.serializers import ModelSerializer, ValidationError
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    def validate_login(self, data):
        if 'email' in data:
            if User.objects.filter(email=data['email']).exists():
                if data['password'] == User.objects.get(email=data['email']).password:
                    return data
                raise ValidationError('Password is incorrect')
            raise ValidationError('Email does not exist')
        return data
