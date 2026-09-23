SHELL := /bin/bash
.DEFAULT_GOAL := check

.PHONY: check check-fast generate list-check toc toc-check stats stats-check test links hooks-install

check: generate-check list-check toc-check stats-check test

check-fast: generate-check list-check toc-check

generate:
	python3 scripts/generate_readme.py
	uv run --project . python -m awesome_list.cli.run_toc

# Regenerate to a scratch file and compare, so data and readme cannot drift.
generate-check:
	@mkdir -p .state
	@python3 scripts/generate_readme.py --out .state/readme.generated.md >/dev/null
	@uv run --project . python -m awesome_list.cli.run_toc --readme .state/readme.generated.md --config awesome.toml >/dev/null
	@diff -u .state/readme.generated.md README.md >/dev/null || (echo "README.md is stale: run make generate" && rm -f .state/readme.generated.md && exit 1)
	@rm -f .state/readme.generated.md

list-check:
	uv run --project . python -m awesome_list.cli.run_list_check

toc:
	uv run --project . python -m awesome_list.cli.run_toc

toc-check:
	uv run --project . python -m awesome_list.cli.run_toc --check

stats:
	uv run --project . python -m awesome_list.cli.run_stats

stats-check:
	uv run --project . python -m awesome_list.cli.run_stats --check

test:
	uv run --project . pytest

links:
	lychee --config lychee.toml README.md

hooks-install:
	git config core.hooksPath .githooks
