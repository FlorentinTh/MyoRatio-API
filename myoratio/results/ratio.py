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

    def get_muscles(self) -> tuple[str, str]:
        antagonist = None
        agonist = None

        if self._stage == Stage.CONCENTRIC.value:
            if self._analysis == Analysis.FLEXION.value:
                antagonist = Muscles.RECTUS_FEMORIS.value
                agonist = Muscles.BICEPS_FEMORIS.value
            else:
                antagonist = Muscles.BICEPS_FEMORIS.value
                agonist = Muscles.RECTUS_FEMORIS.value
        else:
            if self._analysis == Analysis.FLEXION.value:
                antagonist = Muscles.BICEPS_FEMORIS.value
                agonist = Muscles.RECTUS_FEMORIS.value
            else:
                antagonist = Muscles.RECTUS_FEMORIS.value
                agonist = Muscles.BICEPS_FEMORIS.value

        if antagonist is None and agonist is None:
            raise ValueError(f"Muscles cannot be determined")

        return antagonist, agonist
