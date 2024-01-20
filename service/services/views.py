from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscribtion
from services.serializer import SubscribtionSerializer
from django.db.models import Prefetch, F, Sum


class SubscribtionView(ReadOnlyModelViewSet):
    # queryset = Subscribtion.objects.all().prefetch_related('client__user')

    queryset = Subscribtion.objects.all().prefetch_related(
        'plan',
        Prefetch('client',
        queryset=Client.objects.all().select_related('user').only('company_name',
                                                                  'user__email'))

        )
    serializer_class = SubscribtionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        response_data = {'result': response.data}
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
        response.data = response_data

        return response