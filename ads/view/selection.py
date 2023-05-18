from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad, Selection
from ads.permissions import AdChangePermission
from ads.serializers import SelectionListSerializer, SelectionCreateSerializer, SelectionDetailSerializer, \
    SelectionUpdateSerializer, SelectionDeleteSerializer


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer
    permission_classes = [IsAuthenticated]


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated, AdChangePermission]


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer
    permission_classes = [IsAuthenticated, AdChangePermission]


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionUpdateSerializer
    permission_classes = [IsAuthenticated, AdChangePermission]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDeleteSerializer
    permission_classes = [IsAuthenticated, AdChangePermission]
