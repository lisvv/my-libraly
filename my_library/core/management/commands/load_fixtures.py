from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Be careful when changing command execution order.
    It's necessary because database models has dependencies of each other.
    And different execution order may lead to failure fixture load.
    """

    help = "Upload fixtures to database"

    def handle(self, *args, **options):
        fixtures = (
            "authors",
            "books",
            "readers",
            "book_history",
            "users"
        )
        for fixture in fixtures:
            management.call_command("loaddata", f"{settings.BASE_DIR}/fixtures/{fixture}.json")
