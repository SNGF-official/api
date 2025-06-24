from django.urls import path

from sngf_api.contact.api.views import ContactCreateAPIView

urlpatterns = [
    path("feedback/", ContactCreateAPIView.as_view(), name="feedback"),
    path("quick-contact/", ContactSimpleAPIView.as_view(), name="quick-contact"),
]
