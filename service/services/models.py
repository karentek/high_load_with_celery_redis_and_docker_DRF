from django.core.validators import MaxValueValidator
from django.db import models
from clients.models import Client
from services.tasks import set_price


class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()
    def __str__(self):
        return f"Service {self.name}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, save_model=True, **kwargs):
        if self.__full_price != self.full_price:
            for subskribe in self.subscribtion.all():
                set_price.delay(subskribe.id)
                return super().save(*args, **kwargs)


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0,
                                                   validators=[
                                                       MaxValueValidator(100)
                                                   ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def save(self, *args, save_model=True, **kwargs):
        if self.discount_percent != self.__discount_percent:
            for subskribe in self.subscribtion.all():
                set_price.delay(subskribe.id)
                return super().save(*args, **kwargs)




    # def __str__(self):
    #     return f"Plan {self.plan_type}"


class Subscribtion(models.Model):
    client = models.ForeignKey(Client, related_name='subscribtion', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='subscribtion', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='subscribtion', on_delete=models.PROTECT)
    price = models.PositiveIntegerField(default=0)

    # def save(self, *args, save_model=True, **kwargs):
    #     if save_model:
    #         set_price.delay(self.id)
    #     return super().save(*args, **kwargs)
    # не правильное решение так как будет сохранять новый правйс только при сохранении субскрибшона , а если поменяется модель plan или скидка?


    def __str__(self):
        return f"Subscribtion {self.client} to {self.service} on {self.plan}"