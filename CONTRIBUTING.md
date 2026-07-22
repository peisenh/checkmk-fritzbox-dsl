# Contributing

*English · [Deutsch](CONTRIBUTING.de.md)*

Thanks for your interest in this project. This is a small, self-hosted
hobby/portfolio project; contributions are welcome but kept lightweight.

## License of contributions

This project is licensed under the **GNU Affero General Public License v3.0**
(AGPL-3.0, see [LICENSE](LICENSE)). By contributing, you agree that your
contribution is provided under the same license.

## Sign-off (Developer Certificate of Origin)

To keep the provenance of the code clear, contributions must be **signed off**
under the [Developer Certificate of Origin](DCO) (DCO 1.1). The sign-off is a
simple statement that you have the right to submit the code under the project
license — it does **not** transfer any rights to a single person or company
(there is no CLA).

Add the sign-off line to each commit by committing with `-s`:

    git commit -s -m "Your message"

This appends a line like:

    Signed-off-by: Your Name <you@example.com>

Use your real name (or a stable pseudonym) and a reachable e-mail address. By
signing off you certify the points listed in the [DCO](DCO) file.

## Practical notes

- Validate any plugin change on a Checkmk site with `cmk-validate-plugins`
  before submitting — it is the authoritative check that the plugin APIs are
  happy.
- The shipped thresholds and defaults (SNR margin levels, error-rate levels,
  `DB_SCALE`) are deliberately conservative placeholders. Pull requests that
  re-tune them for one specific line are unlikely to be merged — everyone
  tunes those against their own baseline. Improvements to the *mechanism*
  (new metrics, better rate handling, additional TR-064 values) are welcome.
- The plugin targets the modern Checkmk plugin API (`cmk_addons`, 2.3+).
  Please keep changes compatible with that layout and avoid the legacy API.
- Keep changes focused and explain the "why" in the commit message.
- For larger changes, opening an issue first to discuss is appreciated.

No guarantees about review speed — this is a spare-time project.
