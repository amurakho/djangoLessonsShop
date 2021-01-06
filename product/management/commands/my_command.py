from django.core.management.base import  BaseCommand


class Command(BaseCommand):
    help = 'Some help'

    def handle(self, *args, **kwargs):

         print('Hello')