from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Shorturl
from .serializers import ShortSerializer, UrlSerializer
from .permissions import IsOwnerOrReadOnly
import short_url
from random import randint
from django.http import HttpResponse, HttpResponseRedirect
import sqlite3


def redirect_view(request):
    path = request.path
    domain = 'localhost:8000'
    shorts = "http://{}{}".format(domain,path)
    url =  shorts
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        res = cursor.execute('SELECT url FROM shorturl_shorturl WHERE short=?', [shorts])
        try:
            short = res.fetchone()
            if short is not None:
                url = short[0]
            else:
                url = "http://www.url-not-found.com"
        except Exception as e:
            print(e)
    return HttpResponseRedirect(url)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def get_post_shorturl(request):
    # get all movies
    if request.method == 'GET':
        puppies = Shorturl.objects.all()
        serializer = ShortSerializer(puppies, many=True)
        return Response(serializer.data)

    # create a new movie
    elif request.method == 'POST':
        idr = randint(1,99)
        domain = 'localhost:8000'
        shortened_url = "http://{}/{}".format(
                                             domain,
                                             short_url.encode_url(idr)
                                       )
        dict = request.data
        dict["short"] = shortened_url
        serializer = ShortSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
