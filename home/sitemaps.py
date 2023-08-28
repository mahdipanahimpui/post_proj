from django.contrib.sitemaps import Sitemap
from . models import Post
from django.urls import reverse


class PostSitemap(Sitemap):
    priority = '0.7'  # between '0' to '1'
    changefreg = 'daily' # always, hourly, daily, weekly, monthly, yearly, never

    def items(self):
        return Post.objects.all()
    

    # If location isn’t provided, the framework will call the get_absolute_url() method 
    # on each object as returned by items().
    
    # def location(self, item):
    #     print('*'*90)
    #     print(item)
    #     return 


