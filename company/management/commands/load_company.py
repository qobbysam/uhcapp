import logging
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from django_q.tasks import async_task 
from company.tasks import consume_local_folder


logger = logging.getLogger(__name__)
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--folder_path", '-fp' ,type=str,  nargs='+', help="folder containing company json files")

    def handle(self, *args, **options):

        folder_path = options["folder_path"][0]

        tocheck = os.path.join(settings.BASE_DIR, folder_path)



        if os.path.isdir(tocheck):
            logger.info("directory exists")
            task_id = async_task(consume_local_folder, folder_path)
            msg = "started consuming with task id  %s " % (task_id)
            logger.info(msg)
        else:
            msg = "folder does not exist in base directory : %s" %(folder_path)
            logger.error(msg)




