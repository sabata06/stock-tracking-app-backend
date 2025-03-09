from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Enter a secure password."
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirm password",
        style={'input_type': 'password'},
        help_text="Enter the same password again for verification."
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # password2'yi çıkarıyoruz çünkü create_user methodu yalnızca password bekler
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user

from rest_framework import serializers
from .models import CustomUser

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True, 
        style={'input_type': 'password'}, 
        help_text="Enter your current password."
    )
    new_password = serializers.CharField(
        required=True, 
        style={'input_type': 'password'}, 
        help_text="Enter your new password."
    )
    confirm_new_password = serializers.CharField(
        required=True, 
        style={'input_type': 'password'}, 
        help_text="Enter the same password again for verification."
    )

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "The two password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user

class UserStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['is_active']