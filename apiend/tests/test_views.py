import os
from django.test import TestCase,Client
from django.test.utils import override_settings
from rest_framework import status
import haystack
from haystack.utils.loading import ConnectionHandler, UnifiedIndex
from company.models import CompanyModel, ReportingEntityModel
from company.search_indexes import CompanyModelIndex, ReportingEntityIndex
from uhcapp.settings.base import BASE_DIR

client = Client()

WHOOSH_TEST = os.path.join(BASE_DIR, 'apiend','tests',"whoosh_test")

TEST_INDEX = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_TEST ,
    },
}

@override_settings(HAYSTACK_CONNECTIONS=TEST_INDEX)
class SearchCompanyViewTestCase(TestCase):
    def setUp(self) -> None:
        haystack.connections.reload('default')

        connections = ConnectionHandler(TEST_INDEX)

        self.reporting_entity_1 = ReportingEntityModel.objects.create(
            entity_name = "entity name one",
            entity_type = "entity_type one"
        )

        self.company_model_1 = CompanyModel.objects.create (
            company_name = "Company name one",
            entity = self.reporting_entity_1,
            plan_name = "plan name one",
            plan_id = 468552554,
            plan_id_type = "EIN",
            plan_market_type = "plan market",
            network_files = "[{'description': 'somedescription', 'location':'https://url.com'}]"
        )
        self.old_unified_index = connections['default']._index
        self.unified_index = UnifiedIndex()
        self.company_index = CompanyModelIndex()
        self.reporting_entity_index = ReportingEntityIndex()
        self.unified_index.build(indexes=[self.company_index, self.reporting_entity_index])
        
        connections['default']._index = self.unified_index

        backend = connections['default'].get_backend()
        backend.clear()
        backend.update(self.company_index, CompanyModel.objects.all())
        backend.update(self.reporting_entity_index, ReportingEntityModel.objects.all())

        self.valid_company_kwargs = {
            'company_name': "Company name one"
        }

        self.valid_company_auto_complete_kwargs = {
            'q': 'com'
        }

        self.valid_reporting_entity_kwargs = {
            'name': "entity name one"
        }
        self.valid_reporting_entity_auto_complete_kwargs = {
            'q': 'entity'
        }



        super(SearchCompanyViewTestCase, self).setUp()

    def test_search_company(self):

        response = client.get(
            '/api/v1/company/search/', kwargs=self.valid_company_kwargs
        )
       
        self.assertIn(self.company_model_1.company_name,response.data[0]['company_name'])

    def test_auto_company_auto_complete(self):

        response = client.get(
            '/api/v1/company/auto-search/', kwargs=self.valid_company_auto_complete_kwargs
        )
        
        self.assertIn(self.company_model_1.company_name, response.data[0]['company_name'])

    def test_entity_search(self):
        
        response = client.get (
            '/api/v1/entity/search/', kwargs=self.valid_reporting_entity_kwargs


        )

        self.assertIn(self.company_model_1.company_name, response.data["companies"][0]['company_name'] )

    def test_entity_auto_complete(self):

        response = client.get("/api/v1/entity/auto-search/", kwargs=self.valid_reporting_entity_auto_complete_kwargs) 

        self.assertIn(self.reporting_entity_1.entity_name, response.data[0]['name'])

    # def tearDown(self) -> None:
    #     connections = ConnectionHandler(TEST_INDEX )
    #     connections['default']._index = self.old_unified_index
    #     super(SearchCompanyViewTestCase).tearDown()
