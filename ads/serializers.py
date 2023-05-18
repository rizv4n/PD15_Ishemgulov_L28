from rest_framework import serializers

from ads.models import Ad, Selection


class AdListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = 'id', 'name'


class AdCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = '__all__'



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
