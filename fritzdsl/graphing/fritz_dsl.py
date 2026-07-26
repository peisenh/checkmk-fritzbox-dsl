#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Peter Eisenhauer <github@peter-e.de>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Graphing for "DSL Line Errors": one dedicated single graph per metric.

Checkmk orders graphs alphabetically by their internal name. The zero-padded
gNN prefix forces the desired order:

  attenuation -> rates (crc, fec, hec, ES, SES, retrain)
              -> counters (same order)

Attenuation and counters are rendered as a filled area (compound_lines),
the rates as a plain line (simple_lines).
"""

from cmk.graphing.v1 import Title
from cmk.graphing.v1 import graphs


def _single(order: str, metric: str, title: str, filled: bool = False) -> graphs.Graph:
    name = f"fritz_dsl_g{order}_{metric}"
    title_obj = Title(title)  # type: ignore[arg-type]
    if filled:
        return graphs.Graph(name=name, title=title_obj, compound_lines=[metric])
    return graphs.Graph(name=name, title=title_obj, simple_lines=[metric])


# 1) attenuation (filled)
graph_g01 = _single("01", "att_down", "Attenuation downstream", filled=True)
graph_g02 = _single("02", "att_up", "Attenuation upstream", filled=True)

# 2) rates (line)
graph_g03 = _single("03", "crc_rate", "CRC error rate")
graph_g04 = _single("04", "fec_rate", "FEC error rate")
graph_g05 = _single("05", "hec_rate", "HEC error rate")
graph_g06 = _single("06", "errored_secs_rate", "Errored seconds rate")
graph_g07 = _single("07", "severely_errored_secs_rate", "Severely errored seconds rate")
graph_g08 = _single("08", "link_retrain_rate", "Link retrain rate")

# 3) cumulative counters (filled, same order)
graph_g09 = _single("09", "crc", "CRC errors total", filled=True)
graph_g10 = _single("10", "fec", "FEC errors total", filled=True)
graph_g11 = _single("11", "hec", "HEC errors total", filled=True)
graph_g12 = _single("12", "errored_secs", "Errored seconds total", filled=True)
graph_g13 = _single("13", "severely_errored_secs", "Severely errored seconds total", filled=True)
graph_g14 = _single("14", "link_retrain", "Link retrains total", filled=True)
