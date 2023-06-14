from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from core.const import BookStatus
from core.models import Book, Reader


class BookSerializer(serializers.ModelSerializer):
    meta = serializers.SerializerMethodField()

    @extend_schema_field(
        {
            "type": "dict",
            "description": "Мета информация о книге (по автору и названию)",
            "example": {
                "remainder_count": 2, "refund_date": "2023-01-01T00:00:00"
            }
        }
    )
    def get_meta(self, instance):
        return {
            "remainder_count": instance.remainder_count,
            "refund_date": instance.refund_date
        }

    class Meta:
        model = Book
        fields = (
            "pk",
            "name",
            "authors",
            "release_year",
            "status",
            "meta"
        )


class BookEventSerializer(serializers.ModelSerializer):
    reader = serializers.PrimaryKeyRelatedField(queryset=Reader.objects.all(), allow_null=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['reader'] = getattr(instance.current_history_row.reader, "id", None)
        return data

    def validate_status(self, status):
        if self.instance.status == status:
            raise serializers.ValidationError(f"Книга уже и так в статусе {status}")
        return status

    def validate_reader(self, reader):
        if self.initial_data.get("status") in (BookStatus.ON_READING, BookStatus.RESERVED) and not reader:
            raise serializers.ValidationError(
                "При выборе статуса 'На прочтении' или 'Зарезервирована' должен быть выбран читатель"
            )
        if self.initial_data.get("status") == BookStatus.AVAILABLE and reader:
            raise serializers.ValidationError("При выборе статуса 'В наличии' читатель не может быть выбран")
        return reader

    class Meta:
        model = Book
        fields = (
            "pk",
            "reader",
            "status",
        )



