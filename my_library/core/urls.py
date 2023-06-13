from django.urls import include, path
from rest_framework.routers import SimpleRouter

from core.views import AuthorViewSet, BookViewSet, ReaderViewSet

books_router = SimpleRouter(trailing_slash=False)
reader_router = SimpleRouter(trailing_slash=False)
author_router = SimpleRouter(trailing_slash=False)

books_router.register("books", BookViewSet, basename="books")
author_router.register("authors", AuthorViewSet, basename="authors")
reader_router.register("readers", ReaderViewSet, basename="readers")

urlpatterns = [
    path("", include(books_router.urls)),
    path("", include(author_router.urls)),
    path("", include(reader_router.urls)),
    ]