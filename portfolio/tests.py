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
