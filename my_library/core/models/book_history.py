from django.db import models

from core.models.book_statuses import BookStatus


class BookHistory(models.Model):
    reader = models.ForeignKey(
        "core.Reader",
        verbose_name="Читатель",
        help_text="Выберите читателя",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="history"
    )
    book = models.ForeignKey(
        "core.Book",
        verbose_name="Книга",
        help_text="Укажите книгу",
        on_delete=models.PROTECT,
        related_name="history"
    )
    status = models.CharField(
        max_length=20,
        choices=BookStatus.choices,
        verbose_name="Статус книги",
        help_text="Укажите статус книги"
    )

    start_datetime = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата и время начала действия статуса",
        help_text="Укажите дату и время начала действия статуса"

    )
    end_datetime = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата и время окончания действия статуса",
        help_text="Укажите дату и время окончания действия статуса"
    )

    class Meta:
        verbose_name = "История учета"
        verbose_name_plural = "Истории учета"
