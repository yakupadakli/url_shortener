from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from shortener.models import Link


class LinkMixin(object):

    def get_context_data(self, **kwargs):
        context = super(LinkMixin, self).get_context_data(**kwargs)
        if self.request.GET.get("errors"):
            messages.warning(self.request, _(u"There is an error. Please Check Your Url"))
        context["expired_in"] = Link.EXPIRED_IN
        return context


class IndexView(LinkMixin, TemplateView):
    template_name = "shortener/index.html"


class CreateLinkView(CreateView):
    model = Link
    fields = ("original_url", "expired_in", "user")
    success_url = reverse_lazy("index")

    def get_success_url(self):
        form = self.get_form()
        return reverse_lazy("detail-link", kwargs={"slug": form.instance.slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            if self.request.user.is_authenticated():
                return redirect("%s?errors=1" % reverse_lazy("home"))
            return redirect("%s?errors=1" % self.success_url)
        if self.request.user.is_authenticated():
            form.instance.user = self.request.user
            form.save()
        return super(CreateLinkView, self).post(request, *args, **kwargs)


class DetailLinkView(DetailView):
    model = Link
    template_name = "shortener/link_detail.html"


class LinkRedirectView(RedirectView, DetailView):
    model = Link

    def get_redirect_url(self, *args, **kwargs):
        link = self.get_object()
        if link.is_expired:
            messages.warning(self.request, _(u"Link is expired"))
            return reverse_lazy("index")
        Link.objects.filter(id=link.id).update(click_count=link.click_count + 1)
        return link.original_url


class LinkListView(LinkMixin, ListView):
    ordering = "-created_at"
    queryset = Link.objects.filter(is_active=True)
    template_name = "shortener/link_list.html"

    def get_queryset(self):
        queryset = super(LinkListView, self).get_queryset()
        return queryset.filter(user=self.request.user)
