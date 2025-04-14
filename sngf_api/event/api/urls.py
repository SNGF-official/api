from django.urls import path

from sngf_api.event.api.views import EventListViews
from sngf_api.event.api.views import EventRetrieveUpdateView

urlpatterns = [
    path("events/", EventListViews.as_view(), name="events"),
    path("events/<uuid:pk>/", EventRetrieveUpdateView.as_view(), name="event-details"),
]
