# AGENTS.md

## Cursor Cloud specific instructions

This repo is a **Shopify theme** (Veltrus Commerce Stack — Halothemes Ella 7.2.0 fork).
It is plain Liquid/CSS/JS with **no build step** (nothing is compiled/bundled). The
tooling is the **Shopify CLI** (`shopify`), which also provides Theme Check.

### Tooling / setup
- The Shopify CLI is installed globally into `~/.npm-global` and that bin dir is on
  `PATH` via `~/.bashrc` (`export PATH="$HOME/.npm-global/bin:$PATH"`). The startup
  update script reinstalls the CLI; it does not touch `PATH`. If `shopify` is ever
  not found, re-source `~/.bashrc` or add `~/.npm-global/bin` to `PATH`.
- There is no `package.json`/`Gemfile`. Theme Check is built into the CLI — **no Ruby
  is required** (ignore the older `theme-check` gem mentioned in some docs).
- `config/settings_data.json` and `.shopify` are gitignored, so store-specific
  settings are not in the repo.

### Lint (offline, no auth)
- `shopify theme check` — runs fully offline against the theme (currently 411 files,
  0 offenses). Config lives in `.theme-check.yml`. This is the primary automated check.

### Build
- N/A — Shopify themes are not built/compiled.

### Run / preview (REQUIRES store auth)
- `shopify theme dev` uploads a development theme to a connected store and serves a
  live preview at `http://127.0.0.1:9292`. It **cannot render offline** — it needs a
  real store.
- Interactive login uses a device code (`accounts.shopify.com/activate-with-code`).
  For headless/cloud runs use a **Theme Access app password** (or Admin API token):
  - `shopify theme dev --store <store> --password <token>`
  - or env vars: `SHOPIFY_FLAG_STORE=<store>` and `SHOPIFY_CLI_THEME_TOKEN=<token>`
- Target store: `emporiosaibai.myshopify.com` (admin store handle: `byinbz-0k`).
  If the storefront is password-protected, also pass `--store-password <pw>`.

### Smoke test / QA
- Manual QA checklist: `docs/SMOKE_TEST_v1.2.4.md`. Deploy/ops notes:
  `docs/DESPACHO_SAIBAI.md`.

### Code conventions (Saibai customizations)
- Saibai-authored files are prefixed `saibai-*`. Brand color is hardcoded `#F78D1F`
  (do not use `var(--color_highlight)` for buttons). See `README.md` for the file map.
