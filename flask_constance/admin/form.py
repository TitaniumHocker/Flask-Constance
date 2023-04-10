try:
    from flask_wtf import FlaskForm
except ImportError as exc:
    raise ImportError(
        "Flask-WTF must be installed to use integration with Flask-Admin."
    ) from exc
import json

from wtforms import ValidationError, fields


class SettingForm(FlaskForm):
    """Form to update settings."""

    #: Setting name field.
    name = fields.HiddenField("Name")
    #: Setting value field.
    value = fields.TextAreaField("Value")
    #: Submit button.
    submit = fields.SubmitField("Submit")
    #: Reset button.
    reset = fields.SubmitField("Reset")

    def validate_value(self, field):
        """Validate value field.

        :param field: Field to validate.
        :raises ValidationError: If validation failed.
        """
        try:
            json.loads(field.data)
        except json.JSONDecodeError as exc:
            raise ValidationError(str(exc)) from exc
