# Migration to the engine

`awesome-nz-tech` now runs on
[awesome-list-template](https://github.com/olitreadwell/awesome-list-template).
This file records what changed and what is left.

## Fixed

- `data/resources.json` was invalid JSON in two places: a trailing comma before
  the end of the startups array, and a missing comma before `volunteering`. The
  generator could never have run, so the readme had been stuck on its
  placeholder template since the generator landed.
- The readme is regenerated from the data, so the fifteen real entries (Xero,
  Rocket Lab, Sharesies, Hnry, Volpara Health, Silverstripe CMS, NZGOAL, and the
  rest) are in the list rather than a placeholder line.
- The generated Contents section used the category keys as anchors, which
  pointed at nothing. The engine writes that section now, so the links resolve.
- Entries gained a capital and a closing period in the generator, not in the
  data, so the JSON stays plain text.
- `Moxie Sessions` moved from `http` to `https`. The host resolves but does not
  answer, so the weekly link check will report it and you can decide whether it
  moved or is gone.
- `.github/workflows/generate-readme.yml` was retired. `.githooks/pre-commit`
  regenerates the readme and runs the fast checks on this machine instead.

## Left for Oli

- Community Resources and Volunteering Opportunities have no entries. They keep
  their empty arrays and the `*No entries yet*` line until you fill them.
