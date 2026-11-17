# Contributing

Thank you for your interest in this HELIOS artifact. We welcome issues, design feedback,
and well-scoped pull requests.

## Before opening a substantive PR

Open an issue first. We'd rather discuss the change at design level than have you write
code that doesn't fit the architecture. For typos, small docstring fixes, or obvious bugs,
just send the PR.

## Development setup

```bash
git clone https://github.com/577Industries/open-source.git
cd open-source/programs/helios/helios-spaceweather-connectors
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pre-commit install
pytest -m "not live"        # the PR suite — see "Test suites and live-test policy"
```

## Test suites and live-test policy

Two suites, never conflated:

```bash
pytest -m "not live"                      # PR gate: hermetic, fixtures only (what CI runs on pull requests)
pytest -m live --no-cov --timeout=300     # live: real NASA/NOAA/CCMC endpoints; nightly 06:17 UTC + workflow_dispatch only
```

No workflow runs in this repository. The pull-request gate and the nightly run described here belonged to the
standalone repository, which is archived: run the first suite yourself before opening a pull request.

- A live failure is an upstream-drift signal, not a flaky test. Never `xfail`, `skip`,
  mute or loosen an assertion to get green — fix the adapter, re-capture the fixture
  (note the capture date and any hand edit in the fixture docstring), and record the
  change in `CHANGELOG.md` and the adapter's docs page.
- Per-test budgets are `@pytest.mark.timeout(N)` with N = 2.5× the wall clock measured
  in an active-Sun period; the job cap is `timeout-minutes: 45` in
  `.github/workflows/ci.yml`. Re-measure with `pytest -m live --no-cov --durations=0 -k <name>`
  and update the marker and its docstring together.
- Don't run a bare `pytest` from a laptop: it runs the live suite (plus coverage)
  against public NASA/NOAA/CCMC endpoints.

## Style

- `ruff check` and `ruff format` (config in `pyproject.toml`)
- `mypy --strict` for `src/`
- Tests required for new functionality; aim for ≥80% line coverage
- Conventional commit messages (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`)

## Provenance discipline

Any new connector, transformation, or fused output that produces a value must emit a
`ProvenanceRecord` per [`helios-provenance-spec`](https://github.com/577Industries/helios-provenance-spec).
PRs that produce values without a provenance record will be sent back for revision.

A provenance reference that is a URL must be absolute, host included: a relative path cannot be followed from a
record. The CDDIS GIM adapter records the path of the cached file it read, not the file's address; that is a known
gap.

## Versions

The version is `__version__` in `src/helios_connectors/__init__.py`. Change `version:` in `CITATION.cff` and the
product token of `DEFAULT_USER_AGENT` in `src/helios_connectors/http.py` in the same commit; a test compares the
last with `__version__`. Two literals in `src/helios_connectors/adapters/sep_scoreboards.py` (in
`to_helios_model_output`) repeat the version and no test compares them: change them too.

## License

By contributing, you agree your contributions will be licensed under the project's
Apache 2.0 license.
