from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers

from ads.models import Ad, Selection, Category


class AdListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = 'id', 'name'


class AdCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[MinLengthValidator(10)])

    class Meta:
        model = Ad
        fields = '__all__'

    def create(self, validate_data):
        ad = super().create(validate_data)
        ad.author = self.context['request'].user
        ad.is_published = False
        ad.save()

        return ad


class AdDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = '__all__'


class AdDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = '__all__'


class AdUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = ['name', 'price', 'description', 'address', 'category']


class SelectionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = '__all__'

    def create(self, validate_data):
        selection = super().create(validate_data)
        selection.owner = self.context['request'].user
        selection.save()

        return selection


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = 'name'


class CategoryCreateSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(validators=[MinLengthValidator(5), MaxLengthValidator(10)])
    class Meta:
        model = Category
        fields = '__all__'
