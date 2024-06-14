from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from api.models import Libro, Preferiti

class UserSerializer(serializers.ModelSerializer):
    
    """
    The Meta class within a serializer is used to configure the behavior of the serializer, 
    specifying which fields are to be included, excluded, or other configuration options.    
    """
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')

    def create(self, validated_data):
        #validated_data contains the data validated by the serializer
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        """
        The ** operator is used to pass data as separate arguments (username and password) to authenticate.
        """
        user = authenticate(**data)
        
        if user and user.is_active:
            return user
        
        raise serializers.ValidationError("Incorrect Credentials")

class LibroSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Libro
        fields = "__all__"
        
class PreferitoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Preferiti
        fields = '__all__'
        