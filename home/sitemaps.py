from typing import Any, Dict, List, Optional, Union
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from django.contrib.sites.requests import RequestSite
from . models import Post
from django.urls import reverse


def create_custom_tags(obj, tags):
    custom_tags = {}
    for tag in tags:
        if hasattr(obj, tag) and (getattr(obj, tag) is not None):
            custom_tags[tag] = eval(f'obj.{tag}')
    return custom_tags

class PostSitemap(Sitemap):

    priority = '0.7'  # between '0' to '1'
    changefreq = 'daily' # always, hourly, daily, weekly, monthly, yearly, never

    def items(self):
        return Post.objects.all()
    

    




    def get_custom_tags(self, obj):
        return create_custom_tags(obj, [
            'name', 'phone_number', 'description', 'image', 'txt_file', 'pdf_file', 'voice_file'
        ])


    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page=page, site=site, protocol=protocol)
        for url_info in urls:
            obj = url_info['item']
            tags = self.get_custom_tags(obj)
            url_info.update(tags)

        return urls


