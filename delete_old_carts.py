from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from cart.models import Cart

@shared_task
def delete_old_anonymous_carts():
    time_threshold = now() - timedelta(hours=24)
    Cart.objects.filter(user__isnull=True, created_at__lt=time_threshold).delete()

