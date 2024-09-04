from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth.password_validation import validate_password

class UserItemSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'full_name', 'email', 'is_active')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data