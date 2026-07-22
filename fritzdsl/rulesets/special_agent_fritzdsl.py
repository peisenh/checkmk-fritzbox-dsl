#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Peter Eisenhauer <github@peter-e.de>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Ruleset for the special agent (Setup > Agents > Other integrations)."""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    Password,
    String,
)
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _parameter_form() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Queries detailed DSL line metrics (SNR margin, attenuation, "
            "sync rates, FEC/CRC/HEC errors) from an AVM FRITZ!Box over "
            "TR-064. On the FRITZ!Box, 'Allow access for applications' and "
            "UPnP must be enabled, and a user with a password is required."
        ),
        elements={
            "user": DictElement(
                parameter_form=String(title=Title("Username")),
                required=True,
            ),
            "password": DictElement(
                parameter_form=Password(title=Title("Password")),
                required=True,
            ),
            "port": DictElement(
                parameter_form=Integer(
                    title=Title("TR-064 port"),
                    prefill=DefaultValue(49000),
                ),
            ),
        },
    )


rule_spec_fritzdsl = SpecialAgent(
    name="fritzdsl",
    title=Title("FRITZ!Box DSL details"),
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
)
