from django.conf.urls.i18n import i18n_patterns
from django.urls import path

from portfolio import views

urlpatterns = [
    path("robots.txt", views.robots, name="robots"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
]

urlpatterns += i18n_patterns(
    path("", views.home, name="home"),
    prefix_default_language=False,
)
