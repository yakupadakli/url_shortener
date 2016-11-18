from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from shortener.views import IndexView
from url_shortener.decorators import anonymous_required

urlpatterns = [
    url(r'^$', anonymous_required(IndexView.as_view()), name="index"),
    url(r'^home/$', login_required(IndexView.as_view()), name="home"),
]
