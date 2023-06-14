from django.db import models


class BookStatus(models.TextChoices):
    AVAILABLE = "В наличии", "В наличии"
    ON_READING = "На прочтении", "На прочтении"
    RESERVED = "Зарезервирована", "Зарезервирована"
