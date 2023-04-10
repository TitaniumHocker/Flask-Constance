import json
import sys
import typing as t

import click
from flask.cli import AppGroup

from .globals import settings

cli = AppGroup("constance", help="Dynamic settings manegement.")


@cli.command("get")
@click.argument("name", default=None, required=False)
@click.option("-j", "--as-json", is_flag=True, help="Show values as JSON.")
@click.option("-v", "--value-only", is_flag=True, help="Show only values.")
def _get(name: t.Optional[str], as_json: bool, value_only: bool):
    """Get dynamic settings value."""
    if name is not None and name not in dir(settings):
        click.echo(f"Unknown setting name: {name}", err=True)
        return sys.exit(1)
    entries = (
        [(name, getattr(settings, name))]
        if name
        else [(key, getattr(settings, key)) for key in dir(settings)]
    )
    for key, value in entries:
        click.echo(
            "{}{}".format(
                "" if value_only else f"{key} ",
                json.dumps(value) if as_json else value,
            )
        )


@cli.command("set")
@click.argument("name")
@click.argument("value")
def _set(name: str, value: str):
    """Set dynamic setting value."""
    if name not in dir(settings):
        click.echo(f"Unknown setting name: {name}", err=True)
        sys.exit(1)
    try:
        setattr(settings, name, json.loads(value))
    except json.JSONDecodeError as exc:
        click.echo(f"Failed to update {name} setting: {exc}", err=True)
        sys.exit(1)
    click.echo(f"Setting {name} successfully updated.")


@cli.command("del")
@click.argument("name")
def _del(name: str):
    """Delete dynamic setting value(set it to default value)."""
    if name not in dir(settings):
        click.echo(f"Unknown setting name: {name}", err=True)
        sys.exit(1)

    delattr(settings, name)
    click.echo(f"Setting '{name}' successfully deleted(set to default value).")
