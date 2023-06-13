from rest_framework import viewsets

from core.models import Author
from core.pagination import DefaultPagination
from core.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    pagination_class = DefaultPagination
    serializer_class = AuthorSerializer
