import base64

from django.conf import settings
from django.urls import translate_url
from django.utils.translation import get_language

EMAIL = "vaselony@protonmail.com"


def site(request):
    lang = get_language()
    other = "en" if lang == "fr" else "fr"
    theme = request.COOKIES.get("theme")
    return {
        "theme": theme if theme in ("dark", "light") else "dark",
        "other_lang": other,
        "other_lang_url": translate_url(request.path, other),
        "canonical_base": f"https://{settings.CANONICAL_HOST}",
        # address never appears in the html, js decodes it (see site.js)
        "email_enc": base64.b64encode(EMAIL[::-1].encode()).decode(),
        "github": "https://github.com/Showdown76py",
    }
