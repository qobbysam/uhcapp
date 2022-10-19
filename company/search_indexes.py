
from django.utils import timezone
from haystack import indexes
from company.models import CompanyModel, ReportingEntityModel


class ReportingEntityIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='entity_name')
    entity_type = indexes.CharField(model_attr='entity_type')
    autocomplete = indexes.EdgeNgramField()


    @staticmethod
    def prepare_autocomplete(obj):
        return obj.entity_name


    def get_model(self):
        return ReportingEntityModel
    

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            created_at__lte=timezone.now()
        )

class CompanyModelIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    company_name = indexes.CharField(model_attr = 'company_name')
    entity = indexes.CharField(model_attr='entity__entity_name')
    plan_id = indexes.IntegerField(model_attr='plan_id')
    plan_name = indexes.CharField(model_attr='plan_name')
    plan_id_type = indexes.CharField(model_attr = 'plan_id_type')
    plan_market_type = indexes.CharField(model_attr = 'plan_market_type')
    network_files = indexes.CharField(model_attr='hs_network_files')
    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return obj.company_name

    def get_model(self):
        return CompanyModel

    # @staticmethod
    # def prepare_network_files(obj):

    #     return json.dumps(serializers.DictField(obj.network_files).data)
    
    # def prepare_entity(self, obj):
    #     return obj.entity.entity_name
    
    def index_queryset(self, using=None):
        # return self.get_model().objects.filter(
        #     created_at__lte=timezone.now()
        # )
        return self.get_model().objects.all()