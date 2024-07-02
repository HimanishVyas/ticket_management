from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

User = get_user_model()


@receiver(post_save, sender=User)
def user_field_changed(sender, instance, **kwargs):
    # Check if the 'email' field has changed
    print("here is i am brooo")
    if (
        instance._state.db is not None
        and instance.user_role != instance._state.fields.get("user_role")
    ):
        # If 'email' has changed, update the 'details_last_updated' field
        instance.details_last_updated = timezone.now()
        instance.save()
