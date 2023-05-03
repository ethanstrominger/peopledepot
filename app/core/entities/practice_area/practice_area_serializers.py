from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from core.models import PracticeArea


class PracticeAreaSerializer(serializers.ModelSerializer):
    """Used to retrieve user info"""

    class Meta:
        model = PracticeArea
        fields = (
            "uuid",
            "created_at",
            "updated_at",
            "name",
            "description",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )
