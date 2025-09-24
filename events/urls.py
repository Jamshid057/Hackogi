# events/urls.py
from django.urls import path
from .views import event_list, EventDetailView, CreateEventIdeaView, UpvoteIdeaView

app_name = "events"

urlpatterns = [
    path("", event_list, name="event-list"),
    path("<int:event_id>/", EventDetailView.as_view(), name="event-detail"),
    path("<int:event_id>/ideas/create/", CreateEventIdeaView.as_view(), name="create-idea"),
    path("<int:event_id>/ideas/<int:idea_id>/upvote/", UpvoteIdeaView.as_view(), name="upvote-idea"),
]

