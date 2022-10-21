import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        

        try:

            username = os.environ.get('FIRST_ADMIN_USERNAME')
            email = os.environ.get('FIRST_ADIMIN_EMAIL')
            password = os.environ.get('FIRST_ADMIN_PASSWORD') 
            
            su = User.objects.create_superuser(username=username, email=email, password=password)

            su.save()

        except:

            print("create default admin done already", )

