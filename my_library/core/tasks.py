import datetime
import logging

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from core.const import BookStatus
from core.models import Author, Book, Notification
from my_library.celery_app import app

logger = logging.getLogger("celery")


@app.task()
def upload_book_to_db(line) -> None:
    line = line.strip()
    if not line:
        return
    decoded_row = line.decode("utf-8")
    book_name, year, authors = decoded_row.split(";")
    authors_instances = []
    for author in authors.split(","):
        first_name, last_name = author.split()
        instance, created = Author.objects.get_or_create(first_name=first_name, last_name=last_name)
        authors_instances.append(instance)
    new_book = Book.objects.create(name=book_name, release_year=int(year))
    new_book.authors.set(authors_instances)
    new_book.save()


@app.task()
def books_refund_checker():
    books_to_refund = Book.objects.prefetch_related("history", "notifications").filter(
        status=BookStatus.ON_READING,
        history__start_datetime__lte=timezone.now() - relativedelta(days=14),
        history__end_datetime__isnull=True,
    ).exclude(notifications__is_sent=False)
    if books_to_refund.exists():
        for book in books_to_refund:
            Notification.objects.create(
                book=book,
                reader=book.current_history_row.reader,
                refund_datetime=book.current_history_row.start_datetime + relativedelta(days=14)
            )