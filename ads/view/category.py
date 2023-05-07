import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView

from ads.models import Category


def root(request):
    return JsonResponse({'status': 'ok'})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    queryset = Category.objects.order_by('name')

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return JsonResponse([cat.serialize() for cat in categories], safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        category = Category.objects.create(**category_data)
        return JsonResponse(category.serialize())


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_object().serialize())


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        category_data = json.loads(request.body)

        self.object.name = category_data.get('name')

        return JsonResponse(self.object.serialize())


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'})
