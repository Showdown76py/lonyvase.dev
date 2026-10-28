# lonyvase.dev

Source of [lonyvase.dev](https://lonyvase.dev), my personal site. Django, no database, English at `/` and French at `/fr/`.

The look comes from [showdown.boo](https://github.com/Showdown76py/showdown.boo): Satoshi, violet accent, dark and light themes kept in a cookie.

## Run it

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
PORT=8000 .venv/bin/python main.py
```

`main.py` collects static files and serves the app with waitress on `SERVER_PORT` (set by Pelican) or `PORT`. Set `DJANGO_DEBUG=1` to get Django's debug pages.

## Translations

```bash
python manage.py makemessages -l fr --ignore=.venv
python manage.py compilemessages --ignore=.venv
```

The compiled `.mo` is committed so the server doesn't need gettext.

## Tests

```bash
python manage.py test
```

## Hosting

A Pelican Python server clones this repo and pulls it on every start, then a Cloudflare tunnel routes `lonyvase.dev` and `www.lonyvase.dev` to it. `www` redirects to the apex.
