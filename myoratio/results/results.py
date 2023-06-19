import json
import os
from typing import Optional

import pandas as pd

from myoratio.task import Analysis, Stage


class Results:
    def __init__(
        self, areas: Optional[dict] = None, analysis: Optional[str] = None
    ) -> None:
        if areas is not None and analysis is not None:
            self._areas = areas

            if analysis in [analysis.value for analysis in Analysis]:
                self._analysis = analysis
            else:
                raise ValueError(
                    f"Expected a value from ResponseStatus, but got {analysis}"
                )

    def get_ratios(self, data_path: str, stage: str) -> pd.DataFrame:
        json_ratios_file_path = os.path.join(data_path, f"ratios_{stage}.json")

        try:
            return pd.read_json(json_ratios_file_path, encoding="utf-8")
        except pd.errors.ParserError as error:
            raise pd.errors.ParserError(error)

    def compute_ratios(self, stage: str) -> dict:
        ratios = {"nb_iteration": len(self._areas) - 1}

        for area in self._areas.keys():
            if area not in ratios:
                ratios[area] = []  # type: ignore

            muscles = list(self._areas[area].keys())
            areas = list(self._areas[area].values())

            for i in range(len(muscles)):
                if stage == Stage.CONCENTRIC.value:
                    if self._analysis == Analysis.FLEXION.value:
                        range_start = i
                        range_stop = len(muscles)
                    else:
                        range_start = 0
                        range_stop = i + 1
                else:
                    if self._analysis == Analysis.FLEXION.value:
                        range_start = 0
                        range_stop = i + 1
                    else:
                        range_start = i
                        range_stop = len(muscles)

                for j in range(range_start, range_stop):
                    exists = None

                    for item in ratios[area]:  # type: ignore
                        if "muscle" in item and item["muscle"] == muscles[i]:
                            exists = item

                    ratio = areas[i] / areas[j]

                    if ratio == 1:
                        ratio = int(ratio)
                    else:
                        ratio = float(format(ratio, ".2f"))

                    values = None

                    if exists is None:
                        values = [None] * len(muscles)
                        ratios[area].append({"muscle": muscles[i], "values": values})  # type: ignore
                    else:
                        values = exists["values"]

                    values[j] = ratio  # type: ignore

        return ratios

    def write_ratios(self, data_path: str, stage: str, data: dict) -> None:
        path = os.path.join(data_path, f"ratios_{stage}.json")

        try:
            with open(path, "w") as write_file:
                json.dump(data, write_file)
        except Exception as error:
            raise Exception(
                f"Error occurs while trying to write ratios into {path}.Reason: {error}"
            )
