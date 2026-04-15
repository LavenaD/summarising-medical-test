from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length = 8,  style={'input_type': 'password'}) # Ensure password is write-only so it cannot be retrieved in the get operation
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        # User.objects.create = save the password in plain text, which is not secure. Instead, we should use the create_user method which hashes the password.
        # User.objects.create_user = this method will hash the password and save the user securely.
        user = User.objects.create_user(**validated_data)
        return user