from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company, WatchList


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta: 
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data.get('email'),
            password = validated_data.get('password')
        )
        return user   


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class WatchlistSerializer(serializers.ModelSerializer):
    
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True) 
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = WatchList
        # fields = ['id', 'company', 'user']
        fields = ['id', 'company', 'company_id', 'user']