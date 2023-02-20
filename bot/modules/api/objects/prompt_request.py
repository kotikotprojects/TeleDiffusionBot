import dataclasses


@dataclasses.dataclass
class Prompt:
    prompt: str
    negative_prompt: str = None
    steps: int = 20
    cfg_scale: int = 7
    width: int = 768
    height: int = 768
    restore_faces: bool = True
    sampler: str = "Euler a"
    creator: int = None
