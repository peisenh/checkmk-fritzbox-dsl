#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Peter Eisenhauer <github@peter-e.de>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Server-side call: map rule parameters to the special agent command line."""

from collections.abc import Iterator, Sequence

from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


class Params(BaseModel):
    user: str
    password: Secret
    port: int = 49000


def _commands(params: Params, host_config: HostConfig) -> Iterator[SpecialAgentCommand]:
    args: Sequence[str | Secret] = [
        "--host", host_config.primary_ip_config.address,
        "--user", params.user,
        "--password", params.password.unsafe(),
        "--port", str(params.port),
    ]
    yield SpecialAgentCommand(command_arguments=args)


special_agent_fritzdsl = SpecialAgentConfig(
    name="fritzdsl",
    parameter_parser=Params.model_validate,
    commands_function=_commands,
)
