# Legacy WordPress media migration

The source site is `leapforceexamhelp.wordpress.com`; destination is AI Rater Insider.

Run `python scripts/migrate_legacy_media.py` to inventory external images referenced in `editorial/pages/*.html`. This is a dry run and requires no credentials.

**Privacy gate:** Before migrating rating-platform screenshots, review every original and crop out the entire obscured-ID area, not merely overlay a new mask. The script intentionally refuses uploads without `--allow-sensitive`; this flag does **not** crop or inspect images. Do not use it until originals are verified and safe. For sensitive screenshots, manually upload cropped copies and map their source URLs to destination URLs in `editorial/media-migration.json`.

After approved images are ready, run `WP_USER=... WP_APP_PASSWORD=... python scripts/migrate_legacy_media.py --apply --allow-sensitive` in a trusted environment. It uploads only referenced legacy images, records a URL mapping, and updates local HTML. Review the diff, commit the changed HTML and mapping, then publish with the established editorial process. It does not edit WordPress pages automatically.

Existing mapped images are not uploaded again. Keep credentials in GitHub Actions secrets, never commit them. This is an incremental on-demand workflow, not a wholesale migration of unrelated media.
