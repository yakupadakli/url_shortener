from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from shortener.views import IndexView, CreateLinkView, DetailLinkView, LinkRedirectView, LinkListView
from url_shortener.decorators import anonymous_required

urlpatterns = [
    url(r'^$', anonymous_required(IndexView.as_view()), name="index"),
    url(r'^home/$', login_required(LinkListView.as_view()), name="home"),
    url(r'^create/$', CreateLinkView.as_view(), name="create-link"),
    url(r'^link/(?P<slug>[^/]+)/$', DetailLinkView.as_view(), name="detail-link"),
    url(r'^(?P<slug>[^/]+)/$', LinkRedirectView.as_view(), name="link"),
]
