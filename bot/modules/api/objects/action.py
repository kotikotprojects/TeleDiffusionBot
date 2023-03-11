import dataclasses


@dataclasses.dataclass
class Action:
    chat_id: int
    action_module: str
    action: str
    overload: str = None
