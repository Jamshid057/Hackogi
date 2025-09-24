from django.contrib import admin

from .models import Event, Idea, IdeaUpvote, EventRequest

@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "start_date", "end_date", "is_approved")
    actions = ["approve_requests"]

    def approve_requests(self, request, queryset):
        for req in queryset:
            Event.objects.create(
                organizer=req.user,
                title=req.title,
                overview=req.overview,
                start_date=req.start_date,
                end_date=req.end_date,
                is_approved=True
            )
            req.is_approved = True
            req.save()
        self.message_user(request, "Selected requests approved and converted to Events.")



class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organizer",
        "start_date",
        "end_date",
        "is_approved",
    )


class IdeaAdmin(admin.ModelAdmin):
    pass

class IdeaUpvoteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event, EventAdmin)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaUpvote, IdeaUpvoteAdmin)
