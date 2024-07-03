from rest_framework import serializers
from .models import LeaveType


class LeaveTypeSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = LeaveType
        fields = ["type", "description"]

    def create(self, validated_data):
        return super().create(validated_data)
