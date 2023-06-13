import datetime

from django.db import models
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from core.const import BookStatus
from core.models import Book, BookHistory
from core.pagination import DefaultPagination
from core.serializers import BookSerializer
from core.serializers.books import BookEventSerializer
from core.tasks import upload_book_to_db


class BookViewSet(viewsets.ModelViewSet):
    pagination_class = DefaultPagination
    serializer_class = BookSerializer

    def get_queryset(self):
        remainders = Book.objects.filter(
            name=models.OuterRef("name"),
            authors=models.OuterRef("authors__id")
        ).order_by().annotate(
            count=models.Func(models.F('id'), function='Count')
        ).values('count')

        refund_date = BookHistory.objects.filter(
            book__name=models.OuterRef("name"),
            book__authors=models.OuterRef("authors__id"),
            status=BookStatus.ON_READING,
            end_datetime__isnull=True,
        ).order_by("start_datetime").annotate(
            refund_date=models.ExpressionWrapper(
                models.F("start_datetime") + datetime.timedelta(days=14),
                output_field=models.DateTimeField()
            )
        ).values("refund_date")[:1]

        return Book.objects.all().annotate(
            remainder_count=models.Subquery(remainders),
            refund_date=models.Subquery(refund_date, output_field=models.DateTimeField())
        )

    @action(methods=["POST"], url_path="set-status", detail=True)
    def change_book_status(self, request: Request, pk: int):
        book = self.get_object()
        serializer = BookEventSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)

        book.status = serializer.validated_data.get('status')
        book.save()

        current_history = book.current_history_row
        current_history.end_datetime = timezone.now()
        current_history.save()

        BookHistory.objects.create(
            status=serializer.validated_data.get("status"),
            reader=serializer.validated_data.get("reader"),
            book_id=pk
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id='upload_file',
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
        responses={200: None}
    )
    @action(methods=["POST"], url_path="upload-books", detail=False)
    def upload_books(self, request: Request) -> Response:
        input_file = request.FILES['file']
        book_counter = 0
        while True:
            book_counter += 1
            line = input_file.readline()
            upload_book_to_db(line)
            if not line:
                break
        return Response({"message": f"Accept to upload {book_counter} books"})

    def get_serializer_class(self):
        if self.action == "change_book_status":
            return BookEventSerializer
        return BookSerializer
