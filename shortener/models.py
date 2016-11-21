from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext as _

from url_shortener.utils import create_unique_slug


class Link(models.Model):
    ONE_DAY = 1
    ONE_WEEK = 2
    ONE_MONTH = 3
    ONE_YEAR = 4

    EXPIRED_IN = (
        (ONE_DAY, _(u"One Day")),
        (ONE_WEEK, _(u"One Week")),
        (ONE_MONTH, _(u"One Month")),
        (ONE_YEAR, _(u"One Year")),
    )

    original_url = models.URLField(verbose_name=_(u"Original URL"))
    slug = models.SlugField(verbose_name=_(u"Slug"))
    user = models.ForeignKey(User, verbose_name=_(u"User"), null=True, blank=True)
    click_count = models.IntegerField(verbose_name=_(u"Click Count"), default=0)
    expired_in = models.PositiveIntegerField(_(u"Expired In"), choices=EXPIRED_IN)
    is_active = models.BooleanField(verbose_name=_(u"Is Active?"), default=True)
    created_at = models.DateTimeField(verbose_name=_(u"Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_(u"Updated At"))

    def __unicode__(self):
        return "%s - %s " % (self.original_url, self.slug)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = create_unique_slug(self, get_random_string(length=getattr(settings, "SLUG_LENGTH", 8)))
        self.updated_at = datetime.datetime.now()
        return super(Link, self).save()

    def get_remain_expiry_day(self):
        now = datetime.datetime.now()
        return self.get_expiry_day() - (now.day - self.created_at.day)

    def get_remain_expiry_hour(self):
        now = datetime.datetime.now()
        return now.hour - self.created_at.hour

    def get_expiry_day(self):
        if self.expired_in == self.ONE_DAY:
            return 1
        elif self.expired_in == self.ONE_WEEK:
            return 7
        elif self.expired_in == self.ONE_MONTH:
            return 30
        elif self.expired_in == self.ONE_YEAR:
            return 365
        return 0

    def get_expiry_date(self):
        return self.created_at + datetime.timedelta(days=self.get_expiry_day())

    @property
    def is_expired(self):
        now = timezone.now()
        expire_date = self.get_expiry_date()
        return now > expire_date

    @property
    def short_url(self):
        return "%s/%s" % (getattr(settings, "BASE_URL"), self.slug)
