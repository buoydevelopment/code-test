
from django.contrib import admin
from django.conf.urls import include, url
from .views import RegisterView
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', RegisterView.as_view()),
    url(r'^test/', RedirectView.as_view(url='http://www.google.com')),
    url(r'^', include('shorturl.urls')),
]
