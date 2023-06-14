from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from core.models import Reader
from core.pagination import DefaultPagination
from core.serializers.readers import ReaderSerializer


@extend_schema(tags=['Читатели'])
class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    pagination_class = DefaultPagination
    serializer_class = ReaderSerializer
