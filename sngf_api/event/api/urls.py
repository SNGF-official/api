from django.urls import path

from sngf_api.event.api.views import GetEventByIdView
from sngf_api.event.api.views import GetListEventView

urlpatterns = [
    path("events/", GetListEventView.as_view(), name="get-list-event"),
    path("events/<uuid:id>/", GetEventByIdView.as_view(), name="get-event-by-id"),
]
