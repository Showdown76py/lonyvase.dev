from django.conf import settings
from django.urls import translate_url
from django.utils.translation import get_language


def site(request):
    lang = get_language()
    other = "en" if lang == "fr" else "fr"
    theme = request.COOKIES.get("theme")
    return {
        "theme": theme if theme in ("dark", "light") else "dark",
        "other_lang": other,
        "other_lang_url": translate_url(request.path, other),
        "canonical_base": f"https://{settings.CANONICAL_HOST}",
        "email": "me@showdown.boo",
        "github": "https://github.com/Showdown76py",
    }
