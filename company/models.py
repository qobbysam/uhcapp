from email.policy import default
import json
from django.db import models

# Create your models here.



class ReportingEntityModel(models.Model):
    entity_name = models.CharField(max_length = 255)
    entity_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "%s" %(self.entity_name)
    # @property
    # def company(self):
    #     return json.dumps(CompanyModel.objects.filter(self))
#plan to get one to many relationship with entity name




class CompanyModel(models.Model):
    company_name = models.CharField(max_length=255)
    #entity_name = models.CharField(max_length=255)
    
    entity = models.ForeignKey(ReportingEntityModel, null=True ,related_name="reporting_entity", on_delete=models.SET_NULL)
    
    plan_name = models.CharField(max_length=50)
    plan_id = models.IntegerField(blank=True, null=True, default=0)
    plan_id_type = models.CharField(max_length=15)
    plan_market_type = models.CharField(max_length=15)
    network_files = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return "%s" % (self.company_name)

    
    @property
    def hs_network_files(self):
        return json.dumps(self.network_files)