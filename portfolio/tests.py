from django.test import SimpleTestCase, override_settings


@override_settings(STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}})
class SiteTests(SimpleTestCase):
    def test_home_en(self):
        r = self.client.get("/", HTTP_HOST="lonyvase.dev")
        self.assertContains(r, "Lony Vase")
        self.assertContains(r, 'lang="en"')
        self.assertContains(r, 'href="/fr/"')

    def test_home_fr(self):
        r = self.client.get("/fr/", HTTP_HOST="lonyvase.dev")
        self.assertContains(r, 'lang="fr"')
        self.assertContains(r, "Projets")
        self.assertContains(r, 'href="/"')

    def test_accept_language_does_not_switch_root(self):
        r = self.client.get("/", HTTP_HOST="lonyvase.dev", HTTP_ACCEPT_LANGUAGE="fr")
        self.assertContains(r, 'lang="en"')

    def test_www_redirects_to_apex(self):
        r = self.client.get("/fr/?a=1", HTTP_HOST="www.lonyvase.dev")
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r["Location"], "https://lonyvase.dev/fr/?a=1")

    def test_theme_cookie(self):
        self.client.cookies["theme"] = "light"
        r = self.client.get("/", HTTP_HOST="lonyvase.dev")
        self.assertContains(r, 'data-theme="light"')

    def test_bad_theme_cookie_falls_back(self):
        self.client.cookies["theme"] = '"><script>'
        r = self.client.get("/", HTTP_HOST="lonyvase.dev")
        self.assertContains(r, 'data-theme="dark"')

    def test_robots_and_sitemap(self):
        self.assertContains(self.client.get("/robots.txt", HTTP_HOST="lonyvase.dev"), "Sitemap:")
        self.assertContains(self.client.get("/sitemap.xml", HTTP_HOST="lonyvase.dev"), "/fr/")

    def test_404(self):
        r = self.client.get("/nope", HTTP_HOST="lonyvase.dev")
        self.assertEqual(r.status_code, 404)

    def test_email_not_in_html(self):
        r = self.client.get("/", HTTP_HOST="lonyvase.dev")
        body = r.content.decode()
        self.assertNotIn("vaselony", body)
        self.assertNotIn("mailto", body)
        self.assertNotIn("@protonmail", body)
        self.assertContains(r, "data-m=")

    def test_favicon_redirect(self):
        r = self.client.get("/favicon.ico", HTTP_HOST="lonyvase.dev")
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r["Location"].endswith("favicon.ico"))

    def test_site_name_jsonld(self):
        import json, re
        r = self.client.get("/fr/", HTTP_HOST="lonyvase.dev")
        raw = re.search(r'<script type="application/ld\+json">(.*?)</script>', r.content.decode(), re.S).group(1)
        graph = json.loads(raw)["@graph"]
        self.assertEqual(graph[0]["name"], "Lony Vase")
        self.assertEqual(graph[1]["jobTitle"], "Élève ingénieur en informatique")
