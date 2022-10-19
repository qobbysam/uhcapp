
import json
from drf_haystack.serializers import HaystackSerializer
from company.models import CompanyModel

from company.search_indexes import CompanyModelIndex, ReportingEntityIndex
from rest_framework import serializers

from company.tasks import consume_one_file

class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return data
    def to_representation(self, value):
        return json.loads (value)

class CompanyIndexSerializer(HaystackSerializer):

    network_files = JSONSerializerField()
    class Meta:
        index_classes = [CompanyModelIndex]
        fields = ["text","company_name", 'entity','plan_name',"plan_id",'plan_id_type', 'network_files']

class CompanyResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CompanyModel
        fields = ["company_name", 'entity','plan_name',"plan_id",'plan_id_type', 'network_files']


class CompanyAutocompleteSerializer(HaystackSerializer):

    class Meta:
        index_classes = [CompanyModelIndex]
        fields = ["company_name", "autocomplete"]
        ignore_fields = ["autocomplete"]
        field_aliases = {
            "q": "autocomplete"
        }


# class ReportingEntityIndexSerializer(HaystackSerializer):

#     companies = JSONSerializerField()
#     class Meta:
#         index_classes = [ReportingEntityIndex]
#         fields = ["companies"]


class ReportingEntityAutocompleteSerializer(HaystackSerializer):

    class Meta:
        index_classes = [ReportingEntityIndex]
        fields = ["name", "autocomplete"]
        ignore_fields = ["autocomplete"]
        field_aliases = {
            "q": "autocomplete"
        }

class FileUploadSerializer(serializers.Serializer):
    file_upload = serializers.FileField()
    
    class Meta:
        fields = ['file']
    
        
