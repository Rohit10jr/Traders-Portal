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
    """
    Serializer for the Company model.
    Used for creating, retrieving, and updating company information.
    """
    company_name = serializers.CharField(
        max_length=255,
        help_text="The full legal name of the company. Example: `Tata Motors Ltd`"
    )
    symbol = serializers.CharField(
        max_length=50,
        help_text="The unique stock exchange ticker symbol for the company. Example: `TATAMOTORS`"
    )
    scripcode = serializers.CharField(
        max_length=50,
        help_text="A specific code used to identify the company on a particular exchange. Example: `500570`"
    )
    class Meta:
        model = Company
        fields = '__all__'

    # def validate_company_name(self, value):
    #     if not value.isalpha():
    #         raise serializers.ValidationError("Company name should only contain letters.")
    #     return value


class WatchlistSerializer(serializers.ModelSerializer):
    """
    Serializer for the WatchList model.
    Handles adding companies to a user's watchlist and retrieving/managing watchlist entries.
    """
    company = CompanySerializer(read_only=True, help_text="Details of the company in the watchlist.")
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        help_text="The ID of the user who owns this watchlist entry (automatically set)."
    )
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        write_only=True,
        error_messages={
            'required': 'Please provide a company_id',
            'does_not_exist': 'Company with the given ID does not exist.'
        },
        help_text="The ID of the company to add or modify in the watchlist."
    )

    # company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = WatchList
        fields = ['id', 'company', 'company_id', 'user']
        # extra_kwargs = {'id': {'read_only': True}}

    # def validate(self, data):
    #     if 'company_id' not in data:
    #         raise serializers.ValidationError("company_id is required.")
    #     return data
