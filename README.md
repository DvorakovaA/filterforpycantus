# Filter for pycantus

This repository now ships a **fully static** version of Filter for PyCantus for GitHub Pages.

## What it does

The site keeps the original workflow:

1. Fill in the filtration form.
2. Submit to prepare settings.
3. Download the generated YAML file for use with [pycantus](https://github.com/dact-chant/PyCantus).

No Django server is required for normal usage anymore.

## Local usage (no server runtime required)

Open `/home/runner/work/filterforpycantus/filterforpycantus/index.html` in a browser, or serve the repository as static files (for example with `python -m http.server`).

## GitHub Pages deployment

A workflow is included at `.github/workflows/pages.yml`.

- Trigger: pushes to `main` (and manual runs).
- Deployment: uses `actions/configure-pages`, `actions/upload-pages-artifact`, and `actions/deploy-pages`.
- Artifact source: repository contents (`path: .`).

Because links and asset paths are relative, the site works under repository subpaths (project pages), not just domain root.

Expected Pages URL shape:

- `https://<owner>.github.io/filterforpycantus/`

## Repository notes

The original Django code remains in `filter/` as reference/source history, but the deployable app is now static HTML/CSS/JavaScript in the repository root.

## About project

Filter for pycantus (as well as PyCantus itself) is being developed under the Digital Analysis of Chant Transmission ([DACT](https://dact-chant.ca/)). This project, funded by the Social Sciences and Humanities Research Council of Canada, aims to advance the study of chant dissemination using computational tools.

Explore more about the project, its goals and contacts on our [homepage](https://ufal.mff.cuni.cz/grants/dact).
