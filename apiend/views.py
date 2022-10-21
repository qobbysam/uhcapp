
from django.core.files.storage import FileSystemStorage

from django_q.tasks import async_task 

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ViewSet
from rest_framework.parsers import  MultiPartParser


from drf_haystack.viewsets import HaystackViewSet
from drf_haystack.filters import HaystackAutocompleteFilter

from company.models import CompanyModel, ReportingEntityModel
from company.serializers import CompanyIndexSerializer, CompanyResultSerializer, FileUploadSerializer
from company.serializers import CompanyAutocompleteSerializer,  ReportingEntityAutocompleteSerializer
from company.tasks import consume_one_file
from company.task_helpers import check_regex

# Create your views here.


class SearchCompanyView(HaystackViewSet):
    index_models = [CompanyModel]
    serializer_class = CompanyIndexSerializer



class AutocompleteCompanyView(HaystackViewSet):
    index_models = [CompanyModel]
    serializer_class = CompanyAutocompleteSerializer
    filter_backends=[HaystackAutocompleteFilter]

class SearchReportingEntityView(ViewSet, LimitOffsetPagination):

    default_limit = 10
    serializer_class = CompanyResultSerializer

    
    def list(self, request):
        param = request.GET.get("name")
        #sqs = SearchQuerySet.models(CompanyModel)
        sqs = CompanyModel.objects.all()
        if param:
            sqs = sqs.filter(entity__entity_name=param)
        
        page = self.paginate_queryset(sqs, request, view=self)
        company_serialize = self.serializer_class(page, many=True, context={"request": request})
        summary = self.prepare_summary(sqs)
        data = {"companies": company_serialize.data, "summary": summary }
        return Response(data, status=HTTP_200_OK)
    def prepare_summary(self, sqs):
        # return the summary of the search results
        summary = {
            "total": sqs.count(),
            "next_page": self.get_next_link(),
            "previous_page": self.get_previous_link(),
        }
        return summary
class AutocompleteReportingEntityView(HaystackViewSet):
    index_models = [ReportingEntityModel]
    serializer_class = ReportingEntityAutocompleteSerializer
    filter_backends = [HaystackAutocompleteFilter]



class FileUploadViewset(ViewSet):
    parser_classes = (MultiPartParser,)
    serialzer_class = FileUploadSerializer
    
    def create(self, request):
        #for the upload I will only check for the name before I consume.
        #if there content is not right I will push that to the logs

        fs = FileSystemStorage()

        file_upload = request.FILES.get('file')

        file_name = file_upload.name

        print(file_name)
        if check_regex(file_name):
            fs.save(file_name,file_upload)
        
            async_task(consume_one_file, file_name)

            data = {}
            data["name"] = file_name
            data["consume"] = True
            
            return Response(data, HTTP_201_CREATED)

        else:
            data = {}
            data["name"] =file_name
            data["consume"] = False
            data["message"] = "filename not in correct format"
            
            return Response(data, HTTP_400_BAD_REQUEST)

