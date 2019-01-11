from rest_framework import serializers
from .models import Shorturl
from django.contrib.auth.models import User



class ShortSerializer(serializers.ModelSerializer): # create classs to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Shorturl
        fields = ('url', 'code', 'creator', 'short')


class UserSerializer(serializers.ModelSerializer): #create class to serealizer usermodel
    shorturl = serializers.PrimaryKeyRelatedField(many=True, queryset=Shorturl.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'shorturl')

class UrlSerializer(serializers.ModelSerializer): # create classs to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Shorturl
        fields = ('url', 'short', 'creator')
