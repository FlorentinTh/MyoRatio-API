from typing import Optional

from emgtrigno.task import Analysis


class Results:
    def __init__(self, areas: dict, analysis: str):
        self._areas = areas

        if analysis in [analysis.value for analysis in Analysis]:
            self._analysis = analysis
        else:
            raise ValueError(f"Expected a value from ResponseStatus, but got {analysis}")

    def get_ratios(self, iteration: Optional[int] = None) -> dict:

        if iteration is None:
            area = self._areas["mean"]
        else:
            area = self._areas[f"iteration_{iteration}"]

        muscles = list(area.keys())
        areas = list(area.values())

        ratios = {"nb_iteration": len(self._areas) - 1, "data": []}

        for i in range(len(muscles)):
            for j in range(i + 1):
                exists = None

                for item in ratios["data"]:
                    if "muscle" in item and item["muscle"] == muscles[i]:
                        exists = item

                if self._analysis == Analysis.EXTENSION.value:
                    ratio = areas[i] / areas[j]
                elif self._analysis == Analysis.FLEXION.value:
                    ratio = 1 / (areas[i] / areas[j])
                else:
                    raise ReferenceError("Analysis parameter is not valid")

                if ratio == 1:
                    ratio = int(ratio)
                else:
                    ratio = float(format(ratio, ".2f"))

                values = None

                if exists is None:
                    values = [None] * len(muscles)
                    ratios["data"].append({"muscle": muscles[i], "values": values})
                else:
                    values = exists["values"]

                values[j] = ratio  # type: ignore

        return ratios
