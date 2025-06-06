from django import forms

from tests.base import DJANGO_VERSION, BootstrapTestCase


class CheckboxTestForm(forms.Form):
    test = forms.BooleanField()


class InputTypeCheckboxTestCase(BootstrapTestCase):
    def test_input_type_checkbox(self):
        """Test field with checkbox widget."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": CheckboxTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<div class="form-check">'
                '<input class="form-check-input" id="id_test" name="test" required type="checkbox">'
                '<label class="form-check-label" for="id_test">Test</label>'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_checkbox_is_invalid(self):
        """Test field with checkbox widget."""
        html = self.render(
            "{% bootstrap_field form.test %}",
            context={"form": CheckboxTestForm(data={})},
        )
        if DJANGO_VERSION >= "5":  # TODO: Django 4.2
            html = html.replace(' aria-invalid="true"', "")
        if DJANGO_VERSION >= "5.2":  # TODO: Django 5.1
            html = html.replace(' aria-describedby="id_test_error"', "")
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-err django_bootstrap5-req mb-3">'
                '<div class="form-check">'
                '<input class="form-check-input is-invalid" id="id_test" name="test" required type="checkbox">'
                '<label class="form-check-label" for="id_test">Test</label>'
                '<div id="id_test_error">'
                '<div class="invalid-feedback">This field is required.</div>'
                "</div>"
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_checkbox_is_valid(self):
        """Test field with checkbox widget."""
        self.assertHTMLEqual(
            self.render(
                "{% bootstrap_field form.test %}",
                context={"form": CheckboxTestForm(data={"test": "on"})},
            ),
            (
                '<div class="django_bootstrap5-success django_bootstrap5-req mb-3">'
                '<div class="form-check">'
                '<input checked class="form-check-input is-valid" id="id_test" name="test" required type="checkbox">'
                '<label class="form-check-label" for="id_test">Test</label>'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_checkbox_style_switch(self):
        """Test field with checkbox widget, style switch."""
        self.assertHTMLEqual(
            self.render(
                '{% bootstrap_field form.test checkbox_style="switch" %}',
                context={"form": CheckboxTestForm()},
            ),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<div class="form-check form-switch">'
                '<input class="form-check-input" id="id_test" name="test" required type="checkbox">'
                '<label class="form-check-label" for="id_test">Test</label>'
                "</div>"
                "</div>"
            ),
        )

    def test_bootstrap_field_checkbox_horizontal(self):
        """Test field with checkbox widget, layout horizontal."""
        self.assertHTMLEqual(
            self.render(
                "{% bootstrap_field form.test layout='horizontal' %}",
                context={"form": CheckboxTestForm()},
            ),
            (
                '<div class="django_bootstrap5-req mb-3 row">'
                '<div class="col-sm-10 offset-sm-2">'
                '<div class="form-check">'
                '<input class="form-check-input" id="id_test" name="test" required type="checkbox">'
                '<label class="form-check-label" for="id_test">Test</label>'
                "</div>"
                "</div>"
            ),
        )
