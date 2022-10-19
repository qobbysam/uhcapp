import json
from django.test import TestCase

from company.models import ReportingEntityModel, CompanyModel



class ModelTest(TestCase):
    '''Test for company model and reporting entity'''

    def setUp(self) -> None:
        
        self.reporting_entity_1 = ReportingEntityModel.objects.create(
            entity_name = "entity name one",
            entity_type = "entity_type one"
        )

        company_model_1 = CompanyModel.objects.create (
            company_name = "Company name one",
            entity = self.reporting_entity_1,
            plan_name = "plan name one",
            plan_id = 468552554,
            plan_id_type = "EIN",
            plan_market_type = "plan market",
            network_files = "[{'description': 'somedescription', 'location':'https://url.com'}]"
        )

    def test_reporting_entity(self):

        entity = ReportingEntityModel.objects.get(entity_name="entity name one")

        self.assertEqual(entity.entity_type, "entity_type one")
        self.assertEqual(str(entity), "entity name one")

    def test_company_model(self):
        company = CompanyModel.objects.get(company_name="Company name one")

        self.assertEqual(str(company), "Company name one")
        self.assertEqual(company.company_name, "Company name one")
        self.assertEqual(company.entity, self.reporting_entity_1)
        self.assertEqual(company.hs_network_files, json.dumps("[{'description': 'somedescription', 'location':'https://url.com'}]"))