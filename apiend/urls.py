from django.urls import path

from rest_framework import routers
from apiend.views import AutocompleteCompanyView, AutocompleteReportingEntityView, FileUploadViewset, SearchReportingEntityView,SearchCompanyView


app_name = 'apiend'

router = routers.DefaultRouter()

router.register("company/search", SearchCompanyView, basename='company-search')
router.register("company/auto-search",AutocompleteCompanyView, basename="company-auto-search"  )
router.register("entity/search", SearchReportingEntityView, basename='entity-search')
router.register("entity/auto-search", AutocompleteReportingEntityView, basename="entity-auto-search")
router.register("company/file", FileUploadViewset, basename="company-file-upload")
# urlpatterns = [
    
#     path("file/", UploadOneFileView.as_view(), name='one-file-upload')
# ]

