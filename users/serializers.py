from rest_framework import serializers
from users.models import CustomUser

class UserItemSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'full_name', 'email', 'is_superuser', 'is_staff')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"