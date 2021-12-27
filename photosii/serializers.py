from rest_framework import serializers

from .models import Photo


class PhotoListSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(slug_field='name', read_only=True)
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Photo
        fields = ('id', 'image', 'status', 'tag')


class PhotoSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Photo
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('image', 'description', 'status')
