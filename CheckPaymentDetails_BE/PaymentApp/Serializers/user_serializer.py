from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ..Models.user import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'name', 'registration_number', 'joined_at']


class SignupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)
    registration_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'password', 'name', 'registration_number']

    def validate(self, data):
        # ID 중복 체크
        if User.objects.filter(id=data['id']).exists():
            raise serializers.ValidationError({"id": "This ID is already taken."})

        # 주민번호 중복 체크
        if User.objects.filter(registration_number=data['registration_number']).exists():
            raise serializers.ValidationError({"registration_number": "This registration number already exists."})

        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # 비밀번호 해시화
        return User.objects.create(**validated_data)