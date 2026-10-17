# AIOStreams native Home Assistant app (GitHub Actions builds)

> Unofficial wrapper maintained by The-IcEDFiRE. Not affiliated with AIOStreams or Home Assistant.

## What this does

- Every six hours, GitHub Actions checks `ghcr.io/viren070/aiostreams:latest` for a changed image digest.
- On a change (or source-code push or manual run), it builds both amd64 and aarch64 images and publishes them to GHCR.
- **Only after both images exist** does the workflow commit a new `version` in `aiostreams/config.yaml`.
- HAOS sees an update on a subsequent app-store refresh. Turn on **Automatic updates** for this app in Home Assistant to have HAOS install it automatically.
- HAOS manages the app and its data, including backups. `backup: cold` requests a stop during backup for SQLite consistency.

## FIRST-TIME SETUP (do this in order)

1. Create a **public** repository `The-IcEDFiRE/home-assistant-aiostreams` and push these files to the `main` branch.
2. In GitHub repository Settings → Actions → General, allow Actions and set workflow permissions to **Read and write permissions** if needed. The workflow itself declares `contents: write` and `packages: write`. Ensure `main` rules permit the Actions bot's automated version commit (or amend the workflow to use a PR instead).
3. Go to Actions → **Publish AIOStreams Home Assistant app** → **Run workflow** (choose force). Wait for it to finish green. **Do not add the repository to HA before the first successful run**; the first run creates published `1.0.N` images and updates the version.
4. GitHub → your profile → Packages: make **`ha-aiostreams` public**, and ideally the two architecture-specific packages public too. A public repo does *not* automatically guarantee that the image package is public.
5. Add `https://github.com/The-IcEDFiRE/home-assistant-aiostreams` as a custom repository in Home Assistant's **Settings → Apps → App store** menu, then reload the store.
6. You will see another AIOStreams app (repo-backed), **not** an in-place upgrade of `local_aiostreams`. Follow `MIGRATION.md` before starting the new one.
7. On the repo-backed AIOStreams app page, enable **Automatic updates** and **Start on boot** after validating the migration.
8. Verify future releases via `ha apps info <new_app_slug>` (new slug is repository-specific), or the app's Info page.

## Configuration

Set `base_url`, the original `secret_key` (64 hex characters), and optional `operator_auth` in the Home Assistant Configuration tab. `operator_auth` is passed to `AIOSTREAMS_AUTH` and must use comma-separated `username:password` entries. Never commit credentials into this Git repository.

The image builds from an upstream digest rather than a floating tag during CI, so a single run cannot accidentally use two different upstream images on amd64 and aarch64. The workflow tracks **the multi-platform manifest digest**, not the upstream application release version. GitHub scheduled workflows can be delayed, and Supervisor's update polling adds delay; updates are not instantaneous.

## Important limitations

- This is a template prepared for your repository, not an already deployed or CI-tested release. Verify the first Action run, installation, startup and restored data before enabling unattended updates.
- `latest` upstream image updates may include breaking schema changes. **Maintain working backups**, and consider enabling automated app updates only after successful manual migration and one successful app update.
- GitHub Action `GITHUB_TOKEN` commits normally do not trigger `push` workflows, avoiding a self-trigger loop.
- GitHub build actions in this template use major-version refs for readability; pin to reviewed commit SHAs for stronger supply-chain security.
- The workflow's app version scheme is `1.0.<GitHub Actions run number>`; workflow run numbers grow monotonically. If the workflow is replaced or repo reset, check version monotonicity.
- A private GHCR package cannot be pulled anonymously by Supervisor.

Documentation: https://contributors.home-assistant.io/apps/guides/publishing/ and https://contributors.home-assistant.io/apps/guides/repository/
