import json
import os
import typing as t
from collections import OrderedDict

from flask import current_app, flash, redirect, request

try:
    from flask_admin import BaseView, expose
except ImportError as exc:
    raise ImportError(
        "Flask-Admin extension must be installed to use this integration with it."
    ) from exc

from ..globals import settings
from .form import SettingForm

with open(
    os.path.join(
        os.path.relpath(os.path.dirname(__file__)),
        "templates/settings.html.j2",
    ),
    "rt",
) as fh:
    _TEMPLATE = fh.read()


class ConstanceAdminView(BaseView):
    """Flask-Admin view."""

    #: Table headers column names.
    column_headers: t.Tuple[str, str, str] = (
        "Setting name",
        "Setting value",
        "Default value",
    )
    #: Template string used when update succeeded.
    success_update_template: str = "Setting '{name}' successfully updated."
    #: Template string used when update failed.
    failed_update_template: str = "Setting '{name}' update failed: {errors}"
    #: Submit button text.
    submit_button_label: str = "Save"
    #: Form class for settings updating.
    form_class: t.Type[SettingForm] = SettingForm
    #: Reset button label.
    reset_button_label: str = "Reset"
    #: Success reset template.
    success_reset_template: str = "Setting '{name}' successfully reset."
    #: JSON indent.
    json_indent: t.Optional[int] = 2

    @expose("/", methods=["POST", "GET"])
    def index(self):
        """Index view.

        :return: Redirect or rendered page.
        """
        form = self.form_class()

        if form.validate_on_submit():
            if form.submit.data:
                setattr(settings, form.name.data, json.loads(form.value.data))
            elif form.reset.data:
                delattr(settings, form.name.data)
            flash(
                self.success_update_template.format(name=form.name.data)
                if form.submit.data
                else self.success_reset_template.format(name=form.name.data),
                "success",
            )
            return redirect(request.url)

        if form.errors:
            flash(
                self.failed_update_template.format(
                    name=form.name.data,
                    errors=", ".join(form.errors["value"]),
                ),
                "error",
            )
            return redirect(request.url)

        return self.render(
            current_app.jinja_env.from_string(_TEMPLATE),
            settings=OrderedDict(
                {
                    k: json.dumps(getattr(settings, k), indent=self.json_indent)
                    for k in dir(settings)
                }
            ),
            form=form,
            defaults={
                k: json.dumps(v, indent=self.json_indent)
                for k, v in current_app.config["CONSTANCE_PAYLOAD"].items()
            },
        )
