from django.core.management.base import BaseCommand, CommandError
from gify.models import Action


class Command(BaseCommand):
    help = 'Deletes all actions'

    def handle(self, *args, **options):
        try:
            actions = Action.objects.all()
            for action in actions:
                action.delete()
        except:
            self.stdout.write(self.style.ERROR('Error deleting actions'))
        else:
            self.stdout.write(self.style.SUCCESS('Succesfully deleted all action'))
