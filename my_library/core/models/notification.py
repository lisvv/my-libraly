from django.db import models


class Notification(models.Model):
    book = models.ForeignKey(
        "core.Book",
        verbose_name="Книга, подлежащая возврату",
        help_text="Укажите книгу, подлежащую возврату",
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    reader = models.ForeignKey(
        "core.Reader",
        verbose_name="Читатель, имеющий долг по возврату",
        help_text="Укажите читателя, имеющего долг по возврату",
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    refund_datetime = models.DateTimeField(
        verbose_name="Дата возврата книги",
        help_text="Укажите дату возврата книги"
    )
    is_sent = models.BooleanField(
        verbose_name="Отправлено уведомление",
        help_text="Укажите, отправлено ли уведомление",
        default=False
    )
