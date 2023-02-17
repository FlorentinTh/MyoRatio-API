from enum import Enum


class Analysis(Enum):
    EXTENSION = "extension"
    FLEXION = "flexion"

class Stage(Enum):
    CONCENTRIC = "concentric"
    ECCENTRIC = "eccentric"