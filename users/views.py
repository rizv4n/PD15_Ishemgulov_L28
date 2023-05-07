import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad, Category
from users.models import User, Location

TOTAL_ON_PAGE = 5


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    queryset = User.objects.prefetch_related('locations').annotate(
        total_ads=Count("ad", filter=Q(ad__is_published=True)))

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        users_on_page = paginator.get_page(page_number)
        return JsonResponse({
            'total': paginator.count,
            'num_pages': paginator.num_pages,
            'items': [{**user.serialize(), 'total_ads': user.total_ads} for user in users_on_page]
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        locations = user_data.pop['locations']
        user = User.objects.create(**user_data)
        for loc in locations:
            loc, _ = Location.objects.get_or_create(name=loc)
            user.locations.add(loc)
        return JsonResponse(user.serialize())


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_object().serialize())


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        if 'locations' in user_data:
            locations = user_data.pop['locations']
            self.object.locations.clear()
            for loc in locations:
                loc, _ = Location.objects.get_or_create(name=loc)
                self.object.locations.add(loc)
        if 'username' in user_data:
            self.object.username = user_data['username']
        if 'first_name' in user_data:
            self.object.username = user_data['first_name']
        if 'last_name' in user_data:
            self.object.username = user_data['last_name']
        if 'age' in user_data:
            self.object.username = user_data['age']
        if 'role' in user_data:
            self.object.username = user_data['role']

        return JsonResponse(self.object.serialize())


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'})
