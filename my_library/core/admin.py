from django.contrib import admin
from core.models import Book, Author, Notification, Reader, BookHistory


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "status")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("pk", "first_name", "last_name")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("pk", "book", "reader", "is_sent")


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ("pk", "first_name", "last_name")


@admin.register(BookHistory)
class BookHistory(admin.ModelAdmin):
    list_display = ("pk", "book", "reader")
