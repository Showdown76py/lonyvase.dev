import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lonyvase.settings")

import django
from django.core.management import call_command
from waitress import serve

django.setup()
# whitenoise serves from STATIC_ROOT so rebuild it on every boot (pulls may change assets)
call_command("collectstatic", interactive=False, verbosity=0)

from lonyvase.wsgi import application

if __name__ == "__main__":
    # SERVER_PORT is injected by pelican, PORT kept for local runs
    port = int(os.environ.get("SERVER_PORT") or os.environ.get("PORT") or 8000)
    serve(application, host="0.0.0.0", port=port, threads=8, trusted_proxy="*",
          trusted_proxy_headers={"x-forwarded-proto"}, clear_untrusted_proxy_headers=True)
