# checkmk-fritzbox-dsl

A Checkmk special agent that pulls **detailed DSL line metrics** from an AVM
FRITZ!Box over TR-064 — the values the built-in FRITZ!Box agent does not expose:
SNR margin, line attenuation, current/attainable sync rates and the line error
counters (FEC/CRC/HEC, errored seconds, link retrains).

Built for the modern Checkmk plugin API (`cmk_addons`, tested on 2.5). Works
alongside the built-in `fritzbox` special agent on the same host.

## Services

| Service          | Contents                                                        |
|------------------|-----------------------------------------------------------------|
| `DSL Line`       | Link status, current & attainable sync rates (down/up)          |
| `DSL SNR Margin` | SNR margin down/up, with configurable lower levels              |
| `DSL Line Errors`| Attenuation, plus FEC/CRC/HEC, ES/SES and link-retrain **rates** (per second) and cumulative counters |

Error counters are cumulative since the last resync; the check derives a
per-second **rate** from them (via `get_rate`) so you can alert on a rising
error rate instead of the meaningless lifetime total. CRC/HEC rates have
configurable upper levels.

## Requirements

- Checkmk 2.3 or newer (developed and run on 2.5).
- Python package [`fritzconnection`](https://pypi.org/project/fritzconnection/)
  in the **site** Python.
- A FRITZ!Box with TR-064 enabled and a dedicated user.

## FRITZ!Box setup

1. **Home Network → Network → Network Settings**: enable
   *Allow access for applications* and *Transmit status information over UPnP*.
2. **System → FRITZ!Box Users**: create a dedicated user with a password and
   grant the **FRITZ!Box Settings** permission. Leave *Access from the Internet*
   disabled — the monitoring host is on the LAN.
3. Under *Login to the home network*, make sure login **with username and
   password** is active (not password-only), otherwise the user-based TR-064
   login fails.

A read-only, LAN-only account is strongly recommended — do not reuse the admin
login.

## Installation

### 1. Install the Python dependency (site Python)

```bash
# as the site user
pip3 install fritzconnection
python3 -c "import fritzconnection; print(fritzconnection.__file__)"
```

The path should live under `~/local/lib/python3/`, i.e. on persistent storage.

> **Docker note:** In the official Checkmk container only `/omd/sites` is a
> persistent volume. A plain `pip3 install` into the version directory is lost
> on container recreation/upgrade. The site pip is pre-configured with a
> `--target` inside `~/local/`, so `pip3 install fritzconnection` (no `--user`)
> lands on the volume. For a fully reproducible setup, bake it into a custom
> image instead:
> ```dockerfile
> FROM checkmk/check-mk-raw:2.5.0p4
> RUN /omd/versions/default/bin/pip3 install fritzconnection
> ```

### 2. Deploy the plugin

Copy the `fritzdsl/` family into your site:

```bash
cp -r fritzdsl ~/local/lib/python3/cmk_addons/plugins/
chmod +x ~/local/lib/python3/cmk_addons/plugins/fritzdsl/libexec/agent_fritzdsl
cmk-validate-plugins        # must report success
cmk -R                      # reload core so the check plugins load
omd reload apache           # reload GUI for rulesets and graphs
```

Or build an MKP for clean distribution (see *Packaging as MKP* below).

## Configuration

1. **Setup → Agents → Other integrations → "FRITZ!Box DSL details"**: create a
   rule with the username, password and (optionally) the TR-064 port, matched to
   your FRITZ!Box host.
2. In the host properties, set *Checkmk agent / API integrations* to
   **"Configured API integrations, no Checkmk agent"** (or the "…and Checkmk
   agent" variant if you also run the built-in agent elsewhere).
3. Discover services:
   ```bash
   cmk -II <fritzbox-host>
   cmk -O
   ```

### Test the agent standalone

```bash
~/local/lib/python3/cmk_addons/plugins/fritzdsl/libexec/agent_fritzdsl \
  --host 192.168.178.1 --user monitoring --password 'PW'
```

Should print a `<<<fritz_dsl>>>` section. `401 Unauthorized` means wrong
credentials; a `500 / not authorized` points to the missing *FRITZ!Box
Settings* permission.

## Thresholds

- **Setup → Service monitoring rules → "FRITZ!Box DSL SNR margin"** — lower
  levels on the SNR margin (default WARN < 6 dB, CRIT < 3 dB).
- **Setup → Service monitoring rules → "FRITZ!Box DSL error rates"** — upper
  levels on CRC/HEC/FEC rate in errors per second (defaults conservative; tune
  against your own baseline).

## Notes and limitations

- **Unit scaling:** SNR margin and attenuation come from TR-064 in 0.1 dB and
  are divided by 10 (`DB_SCALE` in `agent_based/fritz_dsl.py`). If your values
  differ from the FRITZ!Box GUI by a factor of 10, adjust that constant.
- **Rate unit:** error rates are per **second**.
- **No G.INP DTU:** corrected/uncorrected DTU (retransmission counters shown in
  the FRITZ!Box GUI) are **not** available over the clean TR-064 interface and
  are intentionally not scraped from the web UI.
- **Graph order** is controlled via zero-padded graph names in
  `graphing/fritz_dsl.py`, because Checkmk orders graphs alphabetically.

## Troubleshooting

- **`Unimplemented check fritz_dsl_errors`** after an update → the core still
  holds the old plugin. Run `cmk -R` (a plain `omd reload apache` is not
  enough when `agent_based/` changed).
- **401 via Checkmk but the CLI works** → check the password in the rule for a
  trailing space/newline; the server side call passes the real secret via
  `.unsafe()`.

## Packaging as MKP

A ready-to-use manifest ships in [`packaging/fritzbox_dsl.manifest`](packaging/fritzbox_dsl.manifest).
`mkp package` packs files that are already installed under `~/local`, so deploy
first, then package (as the site user):

```bash
# 1. deploy the plugin family
cp -r fritzdsl ~/local/lib/python3/cmk_addons/plugins/
chmod +x ~/local/lib/python3/cmk_addons/plugins/fritzdsl/libexec/agent_fritzdsl

# 2. build the package from the shipped manifest
mkdir -p ~/tmp/check_mk
cp packaging/fritzbox_dsl.manifest ~/tmp/check_mk/fritzbox_dsl.manifest
mkp package ~/tmp/check_mk/fritzbox_dsl.manifest
```

The resulting `fritzbox_dsl-1.0.0.mkp` lands in `~/var/check_mk/packages_local/`.
`version.packaged` is overwritten by the tooling; adjust `version` and
`version.min_required` in the manifest as needed.

## Contributing

Contributions are welcome. Please note the [DCO](DCO) sign-off requirement
(`git commit -s`) — see [CONTRIBUTING.md](CONTRIBUTING.md)
([Deutsch](CONTRIBUTING.de.md)).

## License

Licensed under the **GNU Affero General Public License v3.0 or later**
(AGPL-3.0-or-later). See [LICENSE](LICENSE).
