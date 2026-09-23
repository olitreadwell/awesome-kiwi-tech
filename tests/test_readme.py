"""Invariants for this list: the data, the readme, and the engine agree."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from awesome_list.config.load_list_config import load_list_config
from awesome_list.parse.parse_readme import parse_readme
from awesome_list.rules.run_rules import run_rules
from awesome_list.toc.sync_contents import sync_contents

ROOT = Path(__file__).resolve().parents[1]


def config() -> object:
    return load_list_config(ROOT / "awesome.toml")


def document() -> tuple[object, str]:
    loaded = config()
    text = (ROOT / loaded.readme).read_text(encoding="utf-8")
    return parse_readme(text, vocabulary=loaded.tags), text


def test_no_rule_errors() -> None:
    loaded = config()
    parsed, text = document()
    violations = run_rules(
        parsed,
        text,
        loaded.tags,
        file=loaded.readme,
        entry_sections=loaded.sections,
    )
    errors = [
        violation.render()
        for violation in violations
        if violation.severity == "error"
    ]

    assert errors == []


def test_data_is_valid_json() -> None:
    data = json.loads((ROOT / "data" / "resources.json").read_text(encoding="utf-8"))

    assert data["categories"]


def test_readme_matches_the_data() -> None:
    """Regenerate from the data and compare, so the two cannot drift apart."""
    scratch = ROOT / ".state" / "readme.test.md"
    scratch.parent.mkdir(exist_ok=True)
    subprocess.run(
        ["python3", "scripts/generate_readme.py", "--out", str(scratch)],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    generated, _changed = sync_contents(
        scratch.read_text(encoding="utf-8"), parse_readme(scratch.read_text(encoding="utf-8"))
    )
    scratch.unlink()

    assert generated == (ROOT / "README.md").read_text(encoding="utf-8")


def test_entry_count_does_not_shrink() -> None:
    parsed, _text = document()

    assert len(parsed.entries) >= 15


def test_no_duplicate_urls() -> None:
    parsed, _text = document()
    urls = [entry.url for entry in parsed.entries]

    assert len(urls) == len(set(urls))
