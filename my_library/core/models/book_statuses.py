from django.db import models


class BookStatus(models.TextChoices):
    AVAILABLE = "В наличии"
    ON_READING = "На прочтении"
    RESERVED = "Зарезервирована"
