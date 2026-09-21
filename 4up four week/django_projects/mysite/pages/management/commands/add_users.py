from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from pages.models import UserProfile

USERNAMES = [
    "CBF113993", "CBF113994", "CBF113995", "CBF113996", "CBF113997",
    "CBF113998", "CBF113999", "CBF114000", "CBF114002", "CBF114003",
    "CBF114004", "CBF114007", "CBF114009", "CBF114010", "CBF114011",
    "CBF114012", "CBF114013", "CBF114014", "CBF114015", "CBF114016",
    "CBF114017", "CBF114018", "CBF114019", "CBF114020", "CBF114021",
    "CBF114022", "CBF114023", "CBF114024", "CBF114025", "CBF114026",
    "CBF114027", "CBF114028", "CBF114029", "CBF114030", "CBF114031",
    "CBF114032",
]

PASSWORD = "20260920"


class Command(BaseCommand):
    help = "Bulk-create student accounts with a shared default password."

    def handle(self, *args, **options):
        created, skipped = 0, 0
        for username in USERNAMES:
            user, was_created = User.objects.get_or_create(username=username)
            if was_created:
                user.set_password(PASSWORD)
                user.save()
                created += 1
            else:
                skipped += 1
            UserProfile.objects.get_or_create(user=user)

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created {created} new user(s), skipped {skipped} existing."
        ))
