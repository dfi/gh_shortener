from django.db import models
from django.conf import settings

from django.core.urlresolvers import reverse

from .utils import create_shortcode
from .validators import validate_url


SHORTCODE_MAX = getattr(settings, 'SHORTCODE_MAX', 15)


# Create your models here.

class WinURLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs_original = super().all(*args, **kwargs)
        qs = qs_original.filter(active=True)
        return qs


    def refresh_all_shortcodes(self, items=None):
        qs = WinURL.objects.filter(id__gte=1)
        if items is not None and isinstance(items, int):
            qs = qs.order_by('-id')[:items]
        new_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            q.save()
            print(q.id)
            new_codes += 1
        return 'New codes made: {i}'.format(i=new_codes)


class WinURL(models.Model):
    winurl = models.CharField(max_length=220,
                           validators=[validate_url])

    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    objects = WinURLManager()


    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == '':
            self.shortcode = create_shortcode(self)
        url_exists = WinURL.objects.filter(winurl=self.winurl).exists()
        if not url_exists:
            super().save(*args, **kwargs)
        else:
            print('URL already exists in the database!')


    def __str__(self):
        return str(self.winurl)


    def get_short_url(self):
        # url_path = reverse(
        #     'scode',
        #     kwargs={'shortcode': self.shortcode},
        #     host='www',
        #     scheme='http',
        #     port='8000'
        # )
        short_url = reverse('scode', args=(self.shortcode,))
        return short_url