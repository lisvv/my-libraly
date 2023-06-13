from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Book, BookHistory


@receiver(post_save, sender=Book)
def write_book_history_on_create(sender: Book, *args, **kwargs) -> None:
    if kwargs.get("created"):
        new_book = kwargs.get("instance")
        BookHistory.objects.create(book=new_book, status=new_book.status)
