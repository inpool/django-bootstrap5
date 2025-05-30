from django import forms
from django.forms import TextInput

from tests.base import DJANGO_VERSION, BootstrapTestCase


class CharFieldTestForm(forms.Form):
    test = forms.CharField()


class CharFieldRequiredTestForm(forms.Form):
    test = forms.CharField(min_length=1)


class InputTypeTextTestCase(BootstrapTestCase):
    """Test for TextInput widgets that only differ in `input_type`."""

    def test_input_type_text(self):
        """Test field with default CharField widget."""
        form = CharFieldTestForm()

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": form}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

        form = CharFieldTestForm(data={})
        html = self.render("{% bootstrap_field form.test %}", context={"form": form})
        if DJANGO_VERSION >= "5":  # TODO: Django 4.2
            html = html.replace(' aria-invalid="true"', "")
        if DJANGO_VERSION >= "5.2":  # TODO: Django 5.1
            html = html.replace(' aria-describedby="id_test_error"', "")

        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-err django_bootstrap5-req mb-3">'
                '<label class="form-label" for="id_test">Test</label>'
                '<input type="text" name="test"'
                ' class="form-control is-invalid" placeholder="Test" required id="id_test">'
                '<div id="id_test_error">'
                '<div class="invalid-feedback">This field is required.</div>'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_text_more(self):
        """Test field with default CharField widget."""
        form = CharFieldTestForm()

        self.assertHTMLEqual(
            self.render(
                '{% bootstrap_field form.test addon_before="foo" %}',
                context={"form": form},
            ),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<div class="input-group">'
                '<span class="input-group-text">foo</span>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render(
                '{% bootstrap_field form.test addon_before="foo" addon_before_class="input-group-text-baz" %}',
                context={"form": form},
            ),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<div class="input-group">'
                '<span class="input-group-text-baz">foo</span>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render(
                '{% bootstrap_field form.test addon_before="<div>Test Before</div>" addon_before_class=None %}',
                context={"form": form},
            ),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<div class="input-group">'
                "<div>Test Before</div>"
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render(
                '{% bootstrap_field form.test addon_after="bar" addon_after_class="input-group-text-baz" %}',
                context={"form": form},
            ),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<div class="input-group">'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                '<span class="input-group-text-baz">bar</span>'
                "</div>"
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render(
                '{% bootstrap_field form.test addon_after="<div>Test After</div>" addon_after_class=None %}',
                context={"form": form},
            ),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<div class="input-group">'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "<div>Test After</div>"
                "</div>"
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render(
                '{% bootstrap_field form.test addon_before="foo" layout="floating" %}',
                context={"form": form},
            ),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<div class="input-group">'
                '<span class="input-group-text">foo</span>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
                "</div>"
            ),
        )

        (
            self.assertHTMLEqual(
                self.render(
                    "{% bootstrap_field form.test layout='horizontal' %}",
                    context={"form": form},
                ),
                (
                    '<div class="django_bootstrap5-req mb-3 row">'
                    '<label class="col-form-label col-sm-2" for="id_test">'
                    "Test"
                    '</label><div class="col-sm-10">'
                    '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                    "</div>"
                    "</div>"
                ),
            ),
        )

        self.assertHTMLEqual(
            self.render(
                "{% bootstrap_field form.test layout='floating' %}",
                context={"form": form},
            ),
            (
                '<div class="django_bootstrap5-req mb-3 form-floating">'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                '<label for="id_test" class="form-label">Test</label>'
                "</div>"
            ),
        )

    def test_input_validation_failure(self):
        """Test field with default CharField widget and min-length requirement to trigger validation errors."""
        form = CharFieldRequiredTestForm(data={"test": ""})
        self.assertFalse(form.is_valid())

        html = self.render('{% bootstrap_field form.test addon_before="foo" %}', context={"form": form})
        if DJANGO_VERSION >= "5":  # TODO: Django 4.2
            html = html.replace(' aria-invalid="true"', "")
        if DJANGO_VERSION >= "5.2":  # TODO: Django 5.1
            html = html.replace(' aria-describedby="id_test_error"', "")

        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-err django_bootstrap5-req mb-3">'
                '<label class="form-label" for="id_test">Test</label>'
                '<div class="input-group has-validation">'
                '<span class="input-group-text">foo</span>'
                '<input type="text" name="test" minlength="1" class="form-control'
                ' is-invalid" placeholder="Test" required id="id_test">'
                '<div id="id_test_error">'
                '<div class="invalid-feedback">This field is required.</div>'
                "</div>"
                "</div>"
                "</div>"
            ),
        )

        form = CharFieldRequiredTestForm(data={"test": "a"})
        self.assertTrue(form.is_valid())

        self.assertHTMLEqual(
            self.render(
                '{% bootstrap_field form.test addon_before="foo" %}',
                context={"form": form},
            ),
            (
                '<div class="django_bootstrap5-success django_bootstrap5-req mb-3">'
                '<label class="form-label" for="id_test">Test</label>'
                '<div class="input-group has-validation">'
                '<span class="input-group-text">foo</span>'
                '<input type="text" name="test" value="a" minlength="1" class="form-control'
                ' is-valid" placeholder="Test" required id="id_test">'
                "<div></div>"
                "</div>"
                "</div>"
            ),
        )

    def _test_input_type(self, input_type):
        """Test field with given input type in all layouts."""

        class InputTypeTestForm(forms.Form):
            test = forms.CharField(widget=TextInput(attrs={"type": input_type}))

        form = InputTypeTestForm()
        default_html = (
            '<div class="django_bootstrap5-req mb-3">'
            '<label for="id_test" class="form-label">Test</label>'
            f'<input class="form-control" id="id_test" name="test" placeholder="Test" required type="{input_type}">'
            "</div>"
        )
        horizontal_html = (
            '<div class="django_bootstrap5-req mb-3 row">'
            '<label class="col-form-label col-sm-2" for="id_test">'
            "Test"
            '</label><div class="col-sm-10">'
            f'<input class="form-control" id="id_test" name="test" placeholder="Test" required type="{input_type}">'
            "</div>"
            "</div>"
        )
        floating_html = (
            '<div class="django_bootstrap5-req mb-3 form-floating">'
            f'<input class="form-control" id="id_test" name="test" placeholder="Test" required type="{input_type}">'
            '<label for="id_test" class="form-label">Test</label>'
            "</div>"
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": form}),
            default_html,
        )

        self.assertHTMLEqual(
            self.render(
                "{% bootstrap_field form.test layout='horizontal' %}",
                context={"form": form},
            ),
            horizontal_html,
        )

        self.assertHTMLEqual(
            self.render(
                "{% bootstrap_field form.test layout='floating' %}",
                context={"form": form},
            ),
            floating_html,
        )

    def test_input_types(self):
        """Test field with CharField widget and its type set."""
        self._test_input_type("text")
        self._test_input_type("number")
        self._test_input_type("email")
        self._test_input_type("url")
        self._test_input_type("tel")
        self._test_input_type("date")
        self._test_input_type("time")
        self._test_input_type("password")

    def test_input_type_password(self):
        """Test field with password widget."""

        class PasswordTestForm(forms.Form):
            test = forms.CharField(widget=forms.PasswordInput)

        form = PasswordTestForm()

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": form}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="password">'
                "</div>"
            ),
        )

        (
            self.assertHTMLEqual(
                self.render(
                    "{% bootstrap_field form.test layout='horizontal' %}",
                    context={"form": form},
                ),
                (
                    '<div class="django_bootstrap5-req mb-3 row">'
                    '<label class="col-form-label col-sm-2" for="id_test">'
                    "Test"
                    '</label><div class="col-sm-10">'
                    '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="password">'
                    "</div>"
                    "</div>"
                ),
            ),
        )

        self.assertHTMLEqual(
            self.render(
                "{% bootstrap_field form.test layout='floating' %}",
                context={"form": form},
            ),
            (
                '<div class="django_bootstrap5-req mb-3 form-floating">'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="password">'
                '<label for="id_test" class="form-label">Test</label>'
                "</div>"
            ),
        )
