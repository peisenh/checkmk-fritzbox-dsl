#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Peter Eisenhauer <github@peter-e.de>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Check plugin: parses the <<<fritz_dsl>>> section and creates three services.

  - "DSL Line"        : link status + sync rates (metrics)
  - "DSL SNR Margin"  : SNR margin with levels (ruleset fritz_dsl_snr)
  - "DSL Line Errors" : attenuation + error rates/counters (ruleset fritz_dsl_errors)
"""

import time
from collections.abc import Mapping

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    GetRateError,
    IgnoreResults,
    Metric,
    Result,
    Service,
    State,
    StringTable,
    check_levels,
    get_rate,
    get_value_store,
)

Section = dict[str, str]

# NoiseMargin/attenuation usually come in 0.1 dB -> divide by 10.
# Verify against the FRITZ!Box GUI (Internet > DSL information); set to 1.0 if needed.
DB_SCALE = 10.0


def parse_fritz_dsl(string_table: StringTable) -> Section:
    """Parse the agent section into a key/value mapping."""
    section: Section = {}
    for row in string_table:
        if len(row) >= 2:
            section[row[0]] = " ".join(row[1:])
    return section


agent_section_fritz_dsl = AgentSection(
    name="fritz_dsl",
    parse_function=parse_fritz_dsl,
)


def _f(section: Section, key: str, default: float = 0.0) -> float:
    try:
        return float(section.get(key, default))
    except (TypeError, ValueError):
        return default


def discover_fritz_dsl(section: Section) -> DiscoveryResult:
    """Discover a single service when the section is present."""
    if section:
        yield Service()


# --- DSL Line: status + sync -------------------------------------------------
def check_fritz_dsl_status(section: Section) -> CheckResult:
    """Report link status and current/attainable sync rates."""
    status = section.get("status", "Unknown")
    yield Result(
        state=State.OK if status == "Up" else State.CRIT,
        summary=f"Line is {status}",
    )
    ds, us = _f(section, "sync_down"), _f(section, "sync_up")
    ds_max, us_max = _f(section, "sync_down_max"), _f(section, "sync_up_max")
    yield Result(
        state=State.OK,
        summary=(
            f"Sync down {ds / 1000:.1f} / up {us / 1000:.1f} Mbit/s "
            f"(max {ds_max / 1000:.1f} / {us_max / 1000:.1f})"
        ),
    )
    yield Metric("sync_down", ds)
    yield Metric("sync_up", us)
    yield Metric("sync_down_max", ds_max)
    yield Metric("sync_up_max", us_max)


check_plugin_fritz_dsl_status = CheckPlugin(
    name="fritz_dsl_status",
    sections=["fritz_dsl"],
    service_name="DSL Line",
    discovery_function=discover_fritz_dsl,
    check_function=check_fritz_dsl_status,
)


# --- DSL SNR Margin: with levels ---------------------------------------------
def check_fritz_dsl_snr(params: Mapping[str, object], section: Section) -> CheckResult:
    """Check the SNR margin down/up against the configured lower levels."""
    levels = params.get("snr_lower")
    yield from check_levels(
        _f(section, "snr_down") / DB_SCALE,
        levels_lower=levels,
        metric_name="snr_down",
        label="SNR margin down",
        render_func=lambda v: f"{v:.1f} dB",
    )
    yield from check_levels(
        _f(section, "snr_up") / DB_SCALE,
        levels_lower=levels,
        metric_name="snr_up",
        label="SNR margin up",
        render_func=lambda v: f"{v:.1f} dB",
    )


check_plugin_fritz_dsl_snr = CheckPlugin(
    name="fritz_dsl_snr",
    sections=["fritz_dsl"],
    service_name="DSL SNR Margin",
    discovery_function=discover_fritz_dsl,
    check_function=check_fritz_dsl_snr,
    check_ruleset_name="fritz_dsl_snr",
    check_default_parameters={"snr_lower": ("fixed", (6.0, 3.0))},
)


# --- DSL Line Errors: attenuation + error rates ------------------------------
def check_fritz_dsl_errors(
    params: Mapping[str, object], section: Section
) -> CheckResult:
    """Report attenuation and derive per-second rates from the error counters."""
    value_store = get_value_store()
    now = time.time()

    att_d = _f(section, "att_down") / DB_SCALE
    att_u = _f(section, "att_up") / DB_SCALE
    yield Result(
        state=State.OK,
        summary=f"Attenuation down {att_d:.1f} / up {att_u:.1f} dB",
    )
    # 1) attenuation first
    yield Metric("att_down", att_d)
    yield Metric("att_up", att_u)

    # Order of the error families - applies to both rates AND counters.
    # The graph order in the GUI follows the order of the Metric() output.
    order = ("crc", "fec", "hec", "errored_secs",
             "severely_errored_secs", "link_retrain")
    rated = ("crc", "fec", "hec")  # these get levels

    # Compute rates up front so the output order can be chosen freely.
    rates: dict[str, float | None] = {}
    initializing = False
    for key in order:
        try:
            # raise_overflow=False: a resync resets the counter to 0, which
            # then yields 0 instead of a negative spike.
            rates[key] = get_rate(value_store, f"fritz_dsl.{key}", now,
                                  _f(section, key), raise_overflow=False)
        except GetRateError:
            rates[key] = None
            initializing = True

    # 2) rates in the desired order (each its own graph)
    for key in order:
        rate = rates[key]
        if rate is None:
            continue
        rate_metric = f"{key}_rate"
        if key in rated:
            yield from check_levels(
                rate,
                levels_upper=params.get(rate_metric, ("no_levels", None)),
                metric_name=rate_metric,
                label=f"{key.upper()} rate",
                render_func=lambda v: f"{v:.2f}/s",
                notice_only=True,  # OK in details only, WARN/CRIT in summary
            )
        else:
            yield Metric(rate_metric, rate)

    # 3) cumulative counters in the same order (each its own graph)
    for key in order:
        yield Metric(key, _f(section, key))

    if initializing:
        yield IgnoreResults("Initializing rate counters")

    yield Result(
        state=State.OK,
        notice=(
            f"Totals since resync - CRC {int(_f(section, 'crc'))} / "
            f"FEC {int(_f(section, 'fec'))} / HEC {int(_f(section, 'hec'))}, "
            f"ES {int(_f(section, 'errored_secs'))} / "
            f"SES {int(_f(section, 'severely_errored_secs'))}, "
            f"retrains {int(_f(section, 'link_retrain'))}"
        ),
    )


check_plugin_fritz_dsl_errors = CheckPlugin(
    name="fritz_dsl_errors",
    sections=["fritz_dsl"],
    service_name="DSL Line Errors",
    discovery_function=discover_fritz_dsl,
    check_function=check_fritz_dsl_errors,
    check_ruleset_name="fritz_dsl_errors",
    check_default_parameters={
        "crc_rate": ("fixed", (5.0, 20.0)),
        "hec_rate": ("fixed", (5.0, 20.0)),
        "fec_rate": ("no_levels", None),  # FEC is usually benign
    },
)
