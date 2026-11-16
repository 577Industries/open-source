## Summary

<!-- 1-3 sentences: what does this PR do and why. -->

## Related

- HELIOS program: <https://github.com/577Industries/open-source/tree/main/programs/helios/helios-program>
- Closes #
- OSF pre-registration template: https://github.com/577Industries/open-source/blob/main/programs/helios/helios-program/orchestration/osf_preregistration.template.md
- Kill-gate decision rules: §9 of the OSF pre-registration template

## Quality

- [ ] Tests added or updated
- [ ] `ruff check .` and `ruff format --check .` pass
- [ ] `mypy --strict` passes (or `# type: ignore[...]` added with a justification)
- [ ] `pytest --cov` coverage threshold maintained
- [ ] CHANGELOG.md entry added under `[Unreleased]`
- [ ] Conventional-commit message in PR title (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`)
- [ ] Coverage maintained ≥85% line+branch
- [ ] Hypothesis property test added if invariants exist
- [ ] EvalReport shape preserved (per OSF pre-reg template)
- [ ] Calibrator/conformal state-dict round-trip tested if persistence touched

## Backwards compatibility

<!-- Any breaking changes to public API, JSON Schema, on-disk format, env vars? If yes, document the migration path. -->

## Provenance

- [ ] Any new data flow emits a `helios_provenance.HeliosModelOutputRecord` (or downstream equivalent) per the [provenance spec](https://github.com/577Industries/helios-provenance-spec).
