from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from shortener.models import Link


class IndexView(TemplateView):
    template_name = "shortener/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.GET.get("errors"):
            messages.warning(self.request, _(u"There is an error. Please Check Your Url"))
        context["expired_in"] = Link.EXPIRED_IN
        return context


class CreateLinkView(CreateView):
    model = Link
    fields = ("original_url", "expired_in", "user")
    success_url = reverse_lazy("index")

    def get_success_url(self):
        form = self.get_form()
        return reverse_lazy("detail-link", kwargs={"slug": form.instance.slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        import ipdb
        ipdb.set_trace()
        if not form.is_valid():
            return redirect("%s?errors=1" % self.success_url)
        if self.request.user.is_authenticated():
            form.instance.user = self.request.user
        return super(CreateLinkView, self).post(request, *args, **kwargs)


class DetailLinkView(DetailView):
    model = Link
    template_name = "shortener/link_detail.html"


class LinkRedirectView(RedirectView, DetailView):
    model = Link

    def get_redirect_url(self, *args, **kwargs):
        link = self.get_object()
        Link.objects.filter(id=link.id).update(click_count=link.click_count + 1)
        return link.original_url
