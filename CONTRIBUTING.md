# Contributing

This is a personal workshop repo, worked on by its owner and AI agents. The rules below keep parallel work
from clashing and keep the shared numbers trustworthy. Issues and pull requests from others are welcome.

## What goes where

| You have… | Put it in | How |
|---|---|---|
| a new small project | `projects/<name>/` | `tools/new-project.sh <name>`. Straight to main is fine, once `check.sh` passes (it checks every part has a committed picture shown in the README) |
| a big or long-running project | its own repo, made from `templates/project/` | pin `workshop@vX.Y.Z`, add a row to `projects/README.md` |
| a measurement of a fit or material | `materials/*.md` (with date and part) **and** `src/workshop/fits.py` | PR, because fits.py is code |
| a lesson (something that went wrong, or a number) | `methods/lessons.md`, under its heading, tagged [M]/[C]/[O]/[U] with date and source | straight to main |
| a new machine | `equipment/<make-model>/` from `equipment/_template/`, plus a row in `equipment/README.md` | straight to main |
| a new print profile | a **new** directory beside the others, with a README saying what it's for and what it was first used on | straight to main |
| a helper two projects need | `src/workshop/…` with a test in `tests/` | PR |

## Never edit a proven profile

A print profile that a made part's record points to is history.
To change one, copy it to a new directory with a new name, such as `pla-fast-0.4` → `pla-fast-0.4-v2`
or `pla-quiet-0.4`, and say in its README why it differs. Delete a profile only when no record points
to it.

## The library: versions and changes

`src/workshop` is versioned with [semver](https://semver.org) tags `vX.Y.Z`. Other repos pin a tag, so
a change here never breaks them silently.

- **While at 0.x:** bump the minor version (0.1 → 0.2) for anything that changes or removes an existing function's
  behaviour, and the patch version (0.1.0 → 0.1.1) for fixes and additions.
- **Every library change goes through a pull request** with green CI. Add an entry under `## Unreleased` in
  `CHANGELOG.md`, and say "breaking" when it is.
- **Projects inside this repo** use the workspace copy, so a breaking change must fix them in the same PR.
  CI builds them all.
- **To release:** move `Unreleased` to a version heading, set `__version__` in `src/workshop/__init__.py` and
  `version` in `pyproject.toml`, tag `vX.Y.Z` on main, and push the tag. Then bump the pin in the external projects
  you are responsible for.

Knowledge files (`equipment/`, `materials/`, `methods/`) are not versioned. They are dated
inside: each number carries the date it was measured. Fix them on main whenever reality disagrees.

## Licence

Code is MIT; project design files carry their own licence (see `LICENSE` and each project's README).
By contributing you agree to those terms.

## Pull requests

- Use a branch named after the change (`fits-petg`, `preview-fix`).
- Run `uv run pytest` and `uv run ws-check-file-sizes` locally first. CI runs both and the pictures check; it
  does not rebuild projects, so run a changed project's `check.sh` yourself.
- Review: one other person, or the person responsible for the area (listed in each equipment and project README).
  A library PR from an agent needs a person to approve it.
- Commit messages say what changed and why, in one line, with detail below if needed. Agents add
  their `Co-Authored-By` line.

## Ownership

Every `equipment/<machine>/README.md` and every `projects/<name>/README.md` starts with `Owner:`. The owner
answers questions about it and approves changes to its rules. Anyone may add a measurement or a lesson.

## Safety rules are not for discussion in a PR

A rule in an equipment README that needs a person's word (start a print) changes only
when the machine's owner says so, recorded in `log/decisions.md`.
