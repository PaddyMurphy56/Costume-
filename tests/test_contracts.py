import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from costume.validate import load_document, main, validate_document, validate_file

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
SITE_SCHEMA = SCHEMAS / "site.schema.json"
EXAMPLE_REGISTRY = SCHEMAS / "examples" / "sites.example.yaml"


def load_schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("schema_path", sorted(SCHEMAS.glob("*.schema.json")), ids=lambda p: p.name)
def test_schemas_are_valid_json_schema(schema_path):
    Draft202012Validator.check_schema(load_schema(schema_path))


def test_brief_matches_schema():
    assert validate_file(ROOT / "config" / "brief.yaml", SCHEMAS / "brief.schema.json") == []


def test_brief_budget_and_items():
    brief = load_document(ROOT / "config" / "brief.yaml")
    assert brief["budget"]["total_max"] == 75
    assert brief["budget"]["includes_shipping"] and brief["budget"]["includes_tax"]
    assert {item["id"] for item in brief["needed"]} == {"briefcase", "axe", "blood"}
    assert brief["dates"]["buy_by"] == "2026-10-15"
    assert brief["runs"]["planned"] == [20, 30]
    assert "tough" in brief["extras"]["want"]


def test_example_registry_matches_site_schema():
    assert validate_file(EXAMPLE_REGISTRY, SITE_SCHEMA) == []


def _example_record() -> dict:
    return copy.deepcopy(load_document(EXAMPLE_REGISTRY)["sites"][0])


def test_single_record_validates_against_def():
    assert validate_document(_example_record(), load_schema(SITE_SCHEMA), "SiteRecord") == []


@pytest.mark.parametrize(
    ("mutate", "expected"),
    [
        (lambda r: r.pop("sources"), "'sources' is a required property"),
        (lambda r: r.update(segments=["mall"]), "segments/0"),
        (lambda r: r.update(id="Not A Slug"), "id"),
        (lambda r: r["search"].update(url_template="https://x.test/search"), "search/url_template"),
        (lambda r: r.update(last_verified="yesterday"), "last_verified"),
    ],
)
def test_bad_records_are_rejected(mutate, expected):
    record = _example_record()
    mutate(record)
    errors = validate_document(record, load_schema(SITE_SCHEMA), "SiteRecord")
    assert any(expected in error for error in errors), errors


def test_each_mode_reports_item_index(tmp_path):
    good = _example_record()
    bad = _example_record()
    bad["tier"] = "Z"
    jsonl = tmp_path / "raw.jsonl"
    jsonl.write_text("\n".join(json.dumps(r) for r in (good, bad)), encoding="utf-8")
    errors = validate_file(jsonl, SITE_SCHEMA, "SiteRecord", each=True)
    assert len(errors) == 1 and errors[0].startswith("[1] tier")


def test_cli_exit_codes(tmp_path, capsys):
    assert main([str(EXAMPLE_REGISTRY), str(SITE_SCHEMA)]) == 0
    broken = tmp_path / "broken.json"
    broken.write_text(json.dumps({"schema_version": "0.1", "sites": [{}]}), encoding="utf-8")
    assert main([str(broken), str(SITE_SCHEMA)]) == 1
    assert main([str(broken), str(SITE_SCHEMA), "--def", "NoSuchDef"]) == 2
