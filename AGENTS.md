# Agent instructions

This repository is a curated list of New Zealand tech resources. The rules it
follows live in the engine at
<https://github.com/olitreadwell/awesome-list-template>.

## Before you change anything

```bash
uv sync --group dev
make hooks-install
make check
```

## How this repo works

- `data/resources.json` holds the entries, and `scripts/generate_readme.py`
  writes `README.md` from it. The data is the source, the readme is the output.
- `make generate` writes the readme and then lets the engine write the Contents
  section. `make generate-check` fails the build when the two have drifted
  apart, so never hand-edit entries in `README.md`.
- Descriptions come from the data. Do not write entry text with a model.

## Rules

- Every entry is `- [Name](https://example.com/) - What it is.` with a capital
  and a closing period. This list does not use tags.
- A section with no entries keeps an empty `entries` array in the JSON and a
  `*No entries yet*` line in the readme. Do not invent entries to fill it.
- `make sources` reports candidates from upstream lists. Candidates are not
  entries.
- The weekly link check is `jobs/links.sh`, run by launchd. There is no hosted
  pipeline.
