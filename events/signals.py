# events/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EventRequest, Event


@receiver(post_save, sender=EventRequest)
def move_request_to_event(sender, instance, created, **kwargs):
    if instance.is_approved:
        Event.objects.get_or_create(
            title=instance.title,
            overview=instance.overview,
            start_date=instance.start_date,
            end_date=instance.end_date,
            is_approved=True,
            organizer=instance.user  # agar user ham kerak bo‘lsa
        )
        instance.delete()

