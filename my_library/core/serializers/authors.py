from rest_framework import serializers

from core.models import Author


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = (
            "pk",
            "first_name",
            "last_name",
        )
