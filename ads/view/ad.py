import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad, Category
from users.models import User

TOTAL_ON_PAGE = 5


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    queryset = Ad.objects.order_by('-price')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        ads = paginator.get_page(page_number)
        return JsonResponse({
            'total': paginator.count,
            'num_pages': paginator.num_pages,
            'items': [ad.serialize() for ad in ads]
        }, safe=False)


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
