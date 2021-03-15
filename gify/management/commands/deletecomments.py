from django.core.management.base import BaseCommand, CommandError
from gify.models import Comment


class Command(BaseCommand):
    help = 'Deletes all comments'

    def handle(self, *args, **options):
        try:
            comments = Comment.objects.all()

            for comment in comments:
                comment.delete()
        except:
            self.stdout.write(self.style.ERROR('Error deleting comments'))
        else:
            self.stdout.write(self.style.SUCCESS('Succesfully deleted all comments'))
