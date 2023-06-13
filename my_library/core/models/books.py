from django.db import models

from core.models.book_statuses import BookStatus


class Book(models.Model):
    name = models.CharField(
        max_length=255,
        help_text="Укажите наименование",
        verbose_name="Наименование",
        db_index=True
    )
    authors = models.ManyToManyField(
        "core.Author",
        help_text="Авторы",
        verbose_name="Выберите авторов",
        related_name="books"
    )
    release_year = models.PositiveIntegerField(
        verbose_name="Год выпуска",
        help_text="Укажите год выпуска"
    )
    status = models.CharField(
        max_length=20,
        choices=BookStatus.choices,
        verbose_name="Статус книги",
        help_text="Укажите статус книги",
        default=BookStatus.AVAILABLE
    )

    @property
    def current_history_row(self):
        return self.history.latest("start_datetime")

    def __str__(self):
        return f"{self.name}, {self.release_year}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ("name",)
