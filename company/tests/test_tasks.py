
from html import entities
import os
import json
from django.test.utils import override_settings
from django.test import TestCase
from company.models import CompanyModel
from uhcapp.settings.base import BASE_DIR
from company.task_helpers import check_regex, extract_name_path, data_to_company

NEW_BASE = os.path.join(BASE_DIR, 'company', 'tests')

from django.test.utils import override_settings

@override_settings(BASE_DIR=NEW_BASE)
class TaskBaseTest(TestCase):

    def setUp(self) -> None:
        self.valid_dir = 'test_fol'
        self.valid_file_name = '2022-10-01_1-BETTER-LLC_index.json'
        self.path_one_file = os.path.join(NEW_BASE, 'test_fol',self.valid_file_name)

    def test_check_regex(self):

        val = check_regex(self.valid_file_name)

        self.assertEqual(val, True)

    
    def test_extract_name(self):

        val = extract_name_path(self.path_one_file)

        self.assertEqual(val, "1 BETTER LLC")

    def test_data_dic_to_company(self):
        print(self.path_one_file)
        f = open(self.path_one_file)

        dic = json.load(f)
        f.close()

        name = '1 BETTER LLC'
        entities = {}

        company = CompanyModel(
            plan_id = "341988392"
        )

        val = data_to_company(dic, name, entities)

        self.assertEqual(company.plan_id, val.plan_id)
