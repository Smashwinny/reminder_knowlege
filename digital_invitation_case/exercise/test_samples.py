import unittest
from html.parser import HTMLParser
from pathlib import Path


class SampleInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.editable = 0
        self.external = []
        self.viewport = False
        self.fixed_note = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set(attrs.get("class", "").split())
        if "edit" in classes:
            if attrs.get("contenteditable") == "true" and attrs.get("role") == "textbox":
                self.editable += 1
        if tag in {"script", "img", "iframe", "link"}:
            self.external.append(tag)
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = True

    def handle_data(self, data):
        if "固定模板项" in data:
            self.fixed_note = True


class SampleTests(unittest.TestCase):
    def inspect(self, filename):
        inspector = SampleInspector()
        inspector.feed(Path(__file__).with_name("samples").joinpath(filename).read_text(encoding="utf-8"))
        return inspector

    def test_wedding_has_six_real_editable_fields(self):
        self.assertEqual(self.inspect("wedding-sample.html").editable, 6)

    def test_baby_has_four_real_editable_fields(self):
        self.assertEqual(self.inspect("baby100-sample.html").editable, 4)

    def test_samples_have_mobile_viewport(self):
        for filename in ["wedding-sample.html", "baby100-sample.html"]:
            self.assertTrue(self.inspect(filename).viewport)

    def test_samples_have_no_external_active_or_media_resources(self):
        for filename in ["wedding-sample.html", "baby100-sample.html"]:
            self.assertEqual(self.inspect(filename).external, [])

    def test_fixed_template_scope_is_visible(self):
        for filename in ["wedding-sample.html", "baby100-sample.html"]:
            self.assertTrue(self.inspect(filename).fixed_note)


if __name__ == "__main__":
    unittest.main()
