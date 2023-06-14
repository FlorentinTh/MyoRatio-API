from enum import Enum

from myoratio.task import Analysis, Stage


class Muscles(Enum):
    RECTUS_FEMORIS = "RECTUS FEMORIS"
    RECTUS_ABDOMINIS = "RECTUS ABDOMINIS"
    TENSOR_FASCIAE_LATAE = "TENSOR FASCIAE LATAE"
    GLUTEUS_MAXIMUS = "GLUTEUS MAXIMUS"
    BICEPS_FEMORIS = "BICEPS FEMORIS"
    ADDUCTOR_LONGUS = "ADDUCTOR_LONGUS"
    TIBIALIS_ANTERIOR = "TIBIALIS ANTERIOR"


class Ratio:
    def __init__(self, analysis: str, stage: str) -> None:
        if analysis in [analysis.value for analysis in Analysis]:
            self._analysis = analysis
        else:
            raise ValueError(f"Expected a value from Analysis, but got {analysis}")

        if stage in [stage.value for stage in Stage]:
            self._stage = stage
        else:
            raise ValueError(f"Expected a value from Stage, but got {stage}")

    def get_muscles(self) -> tuple[str | None, str | None]:
        antagonist = None
        agonist = None

        if (
            self._analysis == Analysis.EXTENSION.value
            or self._analysis == Analysis.FLEXION.value
            or self._analysis == Analysis.SIT_STAND.value
        ):
            if self._stage == Stage.CONCENTRIC.value:
                antagonist = Muscles.RECTUS_FEMORIS.value
                agonist = Muscles.BICEPS_FEMORIS.value
            else:
                antagonist = Muscles.BICEPS_FEMORIS.value
                agonist = Muscles.RECTUS_FEMORIS.value

        else:
            raise ValueError(f"Muscles for analysis {self._analysis} are not defined")

        return antagonist, agonist
