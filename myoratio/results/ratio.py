from myoratio.task import Analysis


class Ratio:
    def __init__(self, analysis: str) -> None:
        if analysis in [analysis.value for analysis in Analysis]:
            self._analysis = analysis
        else:
            raise ValueError(f"Expected a value from Analysis, but got {analysis}")

    def get_muscles(self) -> tuple[str | None, str | None]:
        antagonist = None
        agonist = None

        if self._analysis == Analysis.EXTENSION.value:
            antagonist = "BICEPS FEMORIS"
            agonist = "RECTUS FEMORIS"

        return antagonist, agonist
