from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Address


@receiver(post_save, sender=Address)
def update_address_waze_deep_link(sender, instance, created, **kwargs):
    # Add waze deep link
    if not instance.waze_url:
        if instance.latitude and instance.longitude:
            instance.waze_url = f"https://www.waze.com/ul?ll={instance.latitude}%2C{instance.longitude}&navigate=yes&zoom=17"
            instance.save()