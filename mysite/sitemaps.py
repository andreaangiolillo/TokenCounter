from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class HomePageSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['calculate_tokens']

    def location(self, item):
        return reverse(item)

class AboutPageSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['about']

    def location(self, item):
        return reverse(item)
