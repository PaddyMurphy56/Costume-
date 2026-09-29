"""Validate a YAML, JSON or JSONL document against a JSON Schema.

Usage:
    uv run costume-validate registry/sites.yaml schemas/site.schema.json
    uv run costume-validate profiles/ebay.json schemas/site.schema.json --def SiteRecord
    uv run costume-validate raw/x.jsonl schemas/site.schema.json --def SiteRecord --each

Exit code 0 when valid, 1 when the document breaks the schema, 2 on usage errors.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


class _StringDateLoader(yaml.SafeLoader):
    """SafeLoader that keeps dates as strings so they validate as JSON Schema strings."""


_StringDateLoader.yaml_implicit_resolvers = {
    first_char: [(tag, regex) for tag, regex in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for first_char, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def load_document(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        return yaml.load(text, Loader=_StringDateLoader)
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    return json.loads(text)


def build_validator(schema: dict[str, Any], definition: str | None = None) -> Draft202012Validator:
    if definition is not None:
        defs = schema.get("$defs", {})
        if definition not in defs:
            available = ", ".join(sorted(defs))
            raise KeyError(f"schema has no $defs/{definition}; available: {available}")
        schema = {"$schema": schema.get("$schema"), "$defs": defs, "$ref": f"#/$defs/{definition}"}
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)


def validate_document(
    document: Any, schema: dict[str, Any], definition: str | None = None, each: bool = False
) -> list[str]:
    """Return human-readable errors; an empty list means the document is valid."""
    validator = build_validator(schema, definition)
    if each:
        if not isinstance(document, list):
            return ["<root>: --each needs a top-level list"]
        items = list(enumerate(document))
    else:
        items = [(None, document)]

    errors = []
    for index, item in items:
        for error in sorted(validator.iter_errors(item), key=lambda e: list(e.absolute_path)):
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            prefix = f"[{index}] " if index is not None else ""
            errors.append(f"{prefix}{location}: {error.message}")
    return errors


def validate_file(
    data_path: Path, schema_path: Path, definition: str | None = None, each: bool = False
) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return validate_document(load_document(data_path), schema, definition, each)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("data", type=Path, help="YAML, JSON or JSONL file to check")
    parser.add_argument("schema", type=Path, help="JSON Schema file")
    parser.add_argument("--def", dest="definition", help="validate against $defs/<NAME> instead")
    parser.add_argument(
        "--each", action="store_true", help="validate each item of a top-level list"
    )
    args = parser.parse_args(argv)

    try:
        errors = validate_file(args.data, args.schema, args.definition, args.each)
    except (OSError, ValueError, KeyError, yaml.YAMLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if errors:
        for line in errors:
            print(f"{args.data}: {line}")
        print(f"{args.data}: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    print(f"{args.data}: valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
