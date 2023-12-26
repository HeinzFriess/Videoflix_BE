from rest_framework import serializers
from users.models import CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from content.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'  # You can specify specific fields if needed

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email',  'id') #'first_name', 'last_name',
        extra_kwargs = {
            'first_name': {'required': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            #first_name=validated_data['first_name'],
            #last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email'] #, 'first_name', 'last_name'

class EmailSerializer(serializers.Serializer):
    to = serializers.EmailField()
    subject = serializers.CharField()
    message = serializers.CharField()