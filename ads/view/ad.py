import json

from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad
from ads.permissions import AdChangePermission
from ads.serializers import AdListSerializer, AdCreateSerializer, AdDetailSerializer, AdDeleteSerializer, \
    AdUpdateSerializer
from authentication.models import User


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    permission_classes = [IsAuthenticated]


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated, AdChangePermission]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fact_ad_count(request):
    ads_count = Ad.objects.all().aggregate(Count('price'))
    return JsonResponse({'ads_count': ads_count})


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, AdChangePermission]


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDeleteSerializer
    permission_classes = [IsAuthenticated, AdChangePermission]


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadView(UpdateView):
    model = Ad

    fields = '__all__'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.image = request.FILES.get('image')
        self.object.save()
        return JsonResponse(self.object.serialize())
