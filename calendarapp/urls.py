from django.urls import path

from .views import ICSFileUploadView

urlpatterns = [
    path("upload/", ICSFileUploadView.as_view(), name="ics-file-upload"),
]
