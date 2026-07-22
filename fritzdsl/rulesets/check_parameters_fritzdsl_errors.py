#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Peter Eisenhauer <github@peter-e.de>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Check parameter ruleset: upper levels for the DSL error rates."""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _levels(title: str, prefill: tuple[float, float]) -> DictElement:
    return DictElement(
        parameter_form=SimpleLevels(
            title=Title(title),  # type: ignore[arg-type]
            level_direction=LevelDirection.UPPER,
            form_spec_template=Float(unit_symbol="/s"),
            prefill_fixed_levels=DefaultValue(prefill),
        ),
    )


def _parameter_form() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Upper levels for the DSL error rates (errors per second, derived "
            "from the cumulative TR-064 counters). The defaults are "
            "deliberately conservative - tune them against your own baseline."
        ),
        elements={
            "crc_rate": _levels("CRC error rate", (5.0, 20.0)),
            "hec_rate": _levels("HEC error rate", (5.0, 20.0)),
            "fec_rate": _levels("FEC error rate (usually benign)", (100.0, 500.0)),
        },
    )


rule_spec_fritz_dsl_errors = CheckParameters(
    name="fritz_dsl_errors",
    title=Title("FRITZ!Box DSL error rates"),
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    condition=HostCondition(),
)
