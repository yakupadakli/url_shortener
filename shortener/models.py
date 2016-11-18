from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext as _

from url_shortener.utils import create_unique_slug


class Link(models.Model):
    original_url = models.URLField(verbose_name=_(u"Original URL"))
    slug = models.SlugField(verbose_name=_(u"Slug"))
    click_count = models.IntegerField(verbose_name=_(u"Click Count"), default=0)
    is_active = models.BooleanField(verbose_name=_(u"Is Active?"), default=True)
    created_at = models.DateTimeField(verbose_name=_(u"Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_(u"Updated At"))

    def __unicode__(self):
        return "%s - %s " % (self.original_url, self.slug)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = create_unique_slug(self, get_random_string(length=getattr(settings, "SLUG_LENGTH", 8)))
        self.updated_at = datetime.datetime.now()
        return super(Link, self).save()
