from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Count, Exists, OuterRef

from events.forms import CreateIdeaForm, EventRequestForm
from events.models import Event, Idea, IdeaUpvote


def request_event(request):
    if request.method == "POST":
        form = EventRequestForm(request.POST)
        if form.is_valid():
            event_request = form.save(commit=False)
            if request.user.is_authenticated:
                event_request.user = request.user
            event_request.save()
            return redirect("events:event-list")
    else:
        form = EventRequestForm()

    return render(request, "events/request_event.html", {"form": form})


def event_list(request):
    events = Event.objects.filter(is_approved=True)

    if request.method == "POST":
        form = EventRequestForm(request.POST)
        if form.is_valid():
            event_request = form.save(commit=False)
            if request.user.is_authenticated:
                event_request.user = request.user
            event_request.save()
            return redirect("events:event-list")
    else:
        form = EventRequestForm()

    return render(
        request,
        "events/event_list.html",
        {"events": events, "form": form},
    )

class EventDetailView(View):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return HttpResponse("Event does not exist")

        ideas_qs = event.ideas.annotate(
            like_count=Count('upvote')
        ).order_by('-like_count')

        if request.user.is_authenticated:
            ideas_qs = ideas_qs.annotate(
                is_liked=Exists(
                    IdeaUpvote.objects.filter(user=request.user, idea=OuterRef('pk'))
                )
            )

        context = {
            "event": event,
            "ideas": ideas_qs,
            "idea_form": CreateIdeaForm() if request.user.is_authenticated else None
        }

        return render(request, "events/event_detail.html", context)


class CreateEventIdeaView(LoginRequiredMixin, View):
    def post(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return HttpResponse("Event does not exist")

        form = CreateIdeaForm(request.POST)

        if form.is_valid():
            Idea.objects.create(
                owner=request.user,
                event=event,
                title=form.cleaned_data["title"],
                overview=form.cleaned_data["overview"],
            )

        return redirect("events:event-detail", event_id=event.id)


class UpvoteIdeaView(LoginRequiredMixin, View):
    def post(self, request, event_id, idea_id):
        try:
            idea = Idea.objects.get(id=idea_id, event__id=event_id)
        except Idea.DoesNotExist:
            return HttpResponse("Idea does not exist")

        upvote, created = IdeaUpvote.objects.get_or_create(idea=idea, user=request.user)
        if not created:
            # Agar oldin like bosgan bo‘lsa → o‘chiramiz (toggle)
            upvote.delete()

        return redirect("events:event-detail", event_id=event_id)
