from django.urls import path
from .views import SendSMSView, CsvBulkSmsView, SendSMSTemplateCSV

urlpatterns = [
    path("send/", SendSMSView.as_view(), name="send-sms"),
    path("send/csv/", CsvBulkSmsView.as_view(), name="csv-bulk-sms"),
    path("send/template-sms/csv/", SendSMSTemplateCSV.as_view(), name="template-sms-csv"),
]
