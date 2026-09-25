import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class StaticSiteTests(unittest.TestCase):
    def test_main_pages_exist(self):
        for path in ["index.html", "download.html", "help.html", "about.html", "contact.html"]:
            self.assertTrue((REPO_ROOT / path).exists(), f"Missing {path}")

    def test_pages_do_not_use_absolute_filter_routes(self):
        for path in ["index.html", "download.html", "help.html", "about.html", "contact.html"]:
            content = (REPO_ROOT / path).read_text(encoding="utf-8")
            self.assertNotIn('href="/filter/', content)
            self.assertNotIn("href='/filter/", content)
            self.assertNotIn('src="/filter/', content)
            self.assertNotIn("src='/filter/", content)

    def test_pages_workflow_exists(self):
        self.assertTrue((REPO_ROOT / ".github/workflows/pages.yml").exists())


if __name__ == "__main__":
    unittest.main()
