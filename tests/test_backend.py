import re

from pathlib import Path
from unittest import mock

from django.template import TemplateSyntaxError
from django.template import TemplateDoesNotExist

from django.forms import CharField, Form, Media
from django.http import HttpRequest, HttpResponse

from django.middleware.csrf import CsrfViewMiddleware

try:
    from django.middleware.csrf import _compare_masked_tokens as equivalent_tokens
except ImportError:
    from django.middleware.csrf import _compare_salted_tokens as equivalent_tokens

from django.middleware.csrf import get_token

from django.test import SimpleTestCase
from django.test import RequestFactory

import liquid
from django_liquid.liquid import Liquid


class LiquidTests(SimpleTestCase):

    engine_class = Liquid
    backend_name = "liquid"
    options = {
        "context_processors": [
            "django.template.context_processors.static",
        ],
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        params = {
            "DIRS": ["tests/templates/"],
            "APP_DIRS": True,
            "NAME": cls.backend_name,
            "OPTIONS": cls.options,
        }
        cls.engine = cls.engine_class(params)

    def test_from_string(self):
        template = self.engine.from_string("Hello!\n")
        content = template.render()
        self.assertEqual(content, "Hello!\n")

    def test_get_template(self):
        template = self.engine.get_template("template_backends/hello.html")
        content = template.render({"name": "world"})
        self.assertEqual(content, "Hello world!\n")

    def test_get_template_nonexistent(self):
        with self.assertRaises(TemplateDoesNotExist) as e:
            self.engine.get_template("template_backends/nonexistent.html")
        self.assertEqual(e.exception.backend, self.engine)

    def test_get_template_syntax_error(self):
        with self.assertRaises(TemplateSyntaxError):
            self.engine.get_template("template_backends/syntax_error.html")

    def test_no_directory_traversal(self):
        with self.assertRaises(TemplateDoesNotExist):
            self.engine.get_template("../forbidden/template_backends/hello.html")

    def test_non_ascii_characters(self):
        template = self.engine.get_template("template_backends/hello.html")
        content = template.render({"name": "Jérôme"})
        self.assertEqual(content, "Hello Jérôme!\n")

    def test_html_escaping(self):
        # Liquid does not have an auto escape feature.
        template = self.engine.get_template("template_backends/hello.html")
        context = {"name": '<script>alert("XSS!");</script>'}
        content = template.render(context)

        self.assertIn("&lt;script&gt;", content)
        self.assertNotIn("<script>", content)

    def test_explicit_html_escaping(self):
        template = self.engine.get_template("template_backends/hello_escape.html")
        context = {"name": '<script>alert("XSS!");</script>'}
        content = template.render(context)

        self.assertIn("&lt;script&gt;", content)
        self.assertNotIn("<script>", content)

    def test_django_html_escaping(self):
        class TestForm(Form):
            test_field = CharField()

        media = Media(js=["my-script.js"])
        form = TestForm()
        template = self.engine.get_template("template_backends/django_escaping.html")
        content = template.render({"media": media, "test_form": form})

        expected = "{}\n\n{}\n\n{}".format(media, form, form["test_field"])

        self.assertHTMLEqual(content, expected)

    def test_csrf_token(self):
        request = HttpRequest()
        CsrfViewMiddleware(lambda req: HttpResponse()).process_view(
            request, lambda r: None, (), {}
        )

        template = self.engine.get_template("template_backends/csrf.html")
        content = template.render(request=request)

        expected = '<input type="hidden" name="csrfmiddlewaretoken" value="([^"]+)">'
        match = re.match(expected, content) or re.match(
            expected.replace('"', "'"), content
        )
        self.assertTrue(match, "hidden csrftoken field not found in output")
        self.assertTrue(equivalent_tokens(match[1], get_token(request)))

    def test_origin(self):
        template = self.engine.get_template("template_backends/hello.html")
        self.assertTrue(template.origin.name.endswith("hello.html"))
        self.assertEqual(template.origin.template_name, "template_backends/hello.html")

    def test_origin_from_string(self):
        template = self.engine.from_string("Hello!\n")
        self.assertEqual(template.origin.name, "<template>")
        self.assertIsNone(template.origin.template_name)

    def test_exception_debug_info_min_context(self):
        with self.assertRaises(TemplateSyntaxError) as e:
            self.engine.get_template("template_backends/syntax_error.html")
        debug = e.exception.template_debug
        self.assertEqual(debug["after"], "")
        self.assertEqual(debug["before"], "")
        self.assertEqual(debug["during"], "{% for %}")
        self.assertEqual(debug["bottom"], 1)
        self.assertEqual(debug["top"], 0)
        self.assertEqual(debug["line"], 1)
        self.assertEqual(debug["total"], 1)
        self.assertEqual(len(debug["source_lines"]), 1)
        self.assertTrue(debug["name"].endswith("syntax_error.html"))
        self.assertIn("message", debug)

    def test_exception_debug_info_max_context(self):
        with self.assertRaises(TemplateSyntaxError) as e:
            self.engine.get_template("template_backends/syntax_error2.html")

        debug = e.exception.template_debug

        test_cases = [
            ("after", ""),
            ("before", ""),
            ("during", "{% for %}"),
            ("bottom", 26),
            ("top", 5),
            ("line", 16),
            ("total", 31),
        ]

        for key, expect in test_cases:
            with self.subTest(msg=key):
                self.assertEqual(debug[key], expect)

        with self.subTest(msg="source_lines"):
            self.assertEqual(len(debug["source_lines"]), 21)

        with self.subTest(msg="name"):
            self.assertTrue(debug["name"].endswith("syntax_error2.html"))

        with self.subTest(msg="message"):
            self.assertIn("message", debug)

    def test_context_processors(self):
        request = RequestFactory().get("/")
        template = self.engine.from_string("Static URL: {{ STATIC_URL }}")
        content = template.render(request=request)
        self.assertEqual(content, "Static URL: /static/")
        with self.settings(STATIC_URL="/s/"):
            content = template.render(request=request)
        self.assertEqual(content, "Static URL: /s/")

    def test_dirs_pathlib(self):
        engine = Liquid(
            {
                "DIRS": [Path(__file__).parent / "templates" / "template_backends"],
                "APP_DIRS": False,
                "NAME": "liquid",
                "OPTIONS": {},
            }
        )
        template = engine.get_template("hello.html")
        self.assertEqual(template.render({"name": "Joe"}), "Hello Joe!\n")

    def test_template_render_nested_error(self):
        template = self.engine.get_template(
            "template_backends/syntax_error_include.html"
        )
        with self.assertRaises(TemplateSyntaxError) as err:
            template.render(context={})

        debug = err.exception.template_debug

        test_cases = [
            ("after", ""),
            ("before", ""),
            ("during", "{% for %}"),
            ("bottom", 1),
            ("top", 0),
            ("line", 1),
            ("total", 1),
        ]

        for key, expect in test_cases:
            with self.subTest(msg=key):
                self.assertEqual(debug[key], expect)

        with self.subTest(msg="source_lines"):
            self.assertEqual(len(debug["source_lines"]), 1)

        with self.subTest(msg="name"):
            self.assertTrue(debug["name"].endswith("syntax_error.html"))

        with self.subTest(msg="message"):
            self.assertIn("message", debug)

    def test_template_render_error_nonexistent_source(self):
        template = self.engine.get_template("template_backends/hello.html")
        with mock.patch(
            "liquid.template.BoundTemplate.render",
            side_effect=liquid.exceptions.LiquidSyntaxError(
                "", linenum=1, filename="nonexistent.html"
            ),
        ):
            with self.assertRaises(TemplateSyntaxError) as err:
                template.render(context={})

        debug = err.exception.template_debug

        test_cases = [
            ("after", ""),
            ("before", ""),
            ("during", ""),
            ("bottom", 0),
            ("top", 0),
            ("line", 1),
            ("total", 0),
        ]

        for key, expect in test_cases:
            with self.subTest(msg=key):
                self.assertEqual(debug[key], expect)

        with self.subTest(msg="source_lines"):
            self.assertEqual(len(debug["source_lines"]), 0)

        with self.subTest(msg="name"):
            self.assertTrue(debug["name"].endswith("nonexistent.html"))

        with self.subTest(msg="message"):
            self.assertIn("message", debug)
