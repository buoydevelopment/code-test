from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^api/v1/shorturl/$', # urls list all and create new one
        views.get_post_shorturl,
        name='get_post_shorturl'
    ),
    url(
        r'^', # urls list all and create new one
        views.redirect_view,
        name='redirect_view'
    )
]
