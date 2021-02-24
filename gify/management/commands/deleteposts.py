from django.core.management.base import BaseCommand, CommandError
from gify.models import Post


class Command(BaseCommand):
    help = 'Deletes all posts'

    def handle(self, *args, **options):
        try:
            posts = Post.objects.all()

            for post in posts:
                post.delete()
        except:
            self.stdout.write(self.style.ERROR('Error deleting posts'))
        else:
            self.stdout.write(self.style.SUCCESS('Succesfully deleted all posts'))
