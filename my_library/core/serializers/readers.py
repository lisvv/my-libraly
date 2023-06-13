from rest_framework import serializers

from core.models import Reader


class ReaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reader
        fields = (
            "pk",
            "first_name",
            "last_name",
        )
