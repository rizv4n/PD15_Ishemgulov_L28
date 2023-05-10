import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView

from ads.models import Ad, Category
from ads.serializers import AdListSerializer
from users.models import User
from users.views import UserListView

TOTAL_ON_PAGE = 5


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer

    def get(self, request, *args, **kwargs):
        ad_text = request.GET.get('text', None)
        ad_categories = request.GET.getlist('cat', None)
        ad_price_from = request.GET.get('price_from', None)
        ad_price_to = request.GET.get('price_to', None)
        ad_location = request.GET.get('loc', None)

        if ad_text:
            self.queryset = self.queryset.filter(
                name__contains=ad_text
            )

        if ad_price_from and ad_price_to:
            self.queryset = self.queryset.filter(
                price__gte=ad_price_from,
                price__lte=ad_price_to
            )

        if ad_location:
            self.queryset = self.queryset.filter(
                author_id__name__icontains=ad_location
            )

        ad_cat_q = None

        for cat in ad_categories:
            if ad_cat_q is None:
                ad_cat_q = Q(category__id__icontains=cat)
            else:
                ad_cat_q |= Q(category__id__icontains=cat)

        if ad_cat_q:
            self.queryset = self.queryset.filter(ad_cat_q)

        return super().get(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        ads_data = json.loads(request.body)
        author = get_object_or_404(User, pk=ads_data.pop('author_id'))
        category = get_object_or_404(Category, pk=ads_data.pop('category'))
        ad = Ad.objects.create(author=author, category=category, **ads_data)
        return JsonResponse(ad.serialize())


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_object().serialize())


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        if 'name' in ad_data:
            self.object.name = ad_data.get('name')
        if 'price' in ad_data:
            self.object.name = ad_data.get('price')
        if 'author_id' in ad_data:
            author = get_object_or_404(User, pk=ad_data.get('author_id'))
            self.object.name = author
        if 'category' in ad_data:
            category = get_object_or_404(Category, name=ad_data.get('category'))
            self.object.name = category

        return JsonResponse(self.object.serialize())


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'})


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadView(UpdateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)
        self.object.image = request.FILES.get('image')
        self.object.save()
        return JsonResponse(self.object.serialize())
