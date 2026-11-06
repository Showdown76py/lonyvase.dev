from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.templatetags.static import static


def home(request):
    return render(request, "portfolio/index.html")


def robots(request):
    body = f"User-agent: *\nAllow: /\nSitemap: https://{settings.CANONICAL_HOST}/sitemap.xml\n"
    return HttpResponse(body, content_type="text/plain")


def sitemap(request):
    base = f"https://{settings.CANONICAL_HOST}"
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"<url><loc>{base}/</loc></url>\n"
        f"<url><loc>{base}/fr/</loc></url>\n"
        "</urlset>\n"
    )
    return HttpResponse(body, content_type="application/xml")


def favicon(request):
    return HttpResponseRedirect(static("portfolio/img/favicon.ico"))
