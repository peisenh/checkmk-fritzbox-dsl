#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Peter Eisenhauer <github@peter-e.de>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Check parameter ruleset: lower levels for the SNR margin."""

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form() -> Dictionary:
    return Dictionary(
        elements={
            "snr_lower": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Lower levels for SNR margin"),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Float(unit_symbol="dB"),
                    prefill_fixed_levels=DefaultValue((6.0, 3.0)),
                ),
                required=True,
            ),
        },
    )


rule_spec_fritz_dsl_snr = CheckParameters(
    name="fritz_dsl_snr",
    title=Title("FRITZ!Box DSL SNR margin"),
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    condition=HostCondition(),
)
