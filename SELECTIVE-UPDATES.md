# Selective app updates

The publishing workflow now only publishes apps that need updates. This avoids Home Assistant offering an update for every installed app whenever just one wrapper is changed.

## Triggers

| Event | Behavior |
| --- | --- |
| Scheduled check (every 6 hours) | Rebuild only apps whose upstream image digest changed |
| Push affecting `aiometadata/` | Rebuild AIOMetadata, not AIOStreams or Redis |
| Push affecting multiple app directories | Rebuild only the changed apps |
| Manual Run workflow with `force_app: none` | Rebuild only upstream digest changes |
| Manual Run workflow with `force_app: redis` | Force a Redis rebuild; also rebuild any app with an upstream digest change |

The workflow does **not** issue updates solely because the GitHub Actions workflow file changes. To republish a specific app after a build system change, use **Run workflow** and choose that app from `force_app`.

The workflow also updates `upstream-digest.txt` and the relevant `config.yaml` version only **after** an app image successfully publishes. The bot commit is excluded from triggering another publishing run.

## Existing pending updates

If every app already has an available update due to earlier workflow runs, those version numbers have already been published. This workflow prevents further spurious updates but cannot retract updates already offered by Home Assistant. You can install the current versions or leave them until the next real release.

## Testing

1. Push a harmless edit to `aiometadata/DOCS.md` only.
2. View the build log: AIOStreams, AIOManager, Redis, and PostgreSQL should say `SKIP` unless their upstream digests really changed.
3. Check the commit produced by GitHub Actions: only `aiometadata/config.yaml` and `aiometadata/upstream-digest.txt` (if changed) should be modified.

## Notes

If the upstream images of several apps change between checks, a run legitimately publishes several updates. The workflow is image-digest based and does not prevent real upstream updates.
