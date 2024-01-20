from celery import shared_task
from django.db.models import F


@shared_task
def set_price(subscribtion_id):
    from services.models import Subscribtion

    subscribtion = Subscribtion.objects.filter(id=subscribtion_id).annotate(
        annotated_price=F('service__full_price') -
              F('service__full_price') *
              F('plan__discount_percent') / 100.00
    ).first()

    subscribtion.price = subscribtion.annotated_price
    subscribtion.save()

