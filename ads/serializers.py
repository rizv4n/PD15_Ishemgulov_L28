from rest_framework import serializers

from ads.models import Ad


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