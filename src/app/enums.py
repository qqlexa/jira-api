import enum


class StatusEnum(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class PriorityEnum(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RoleEnum(enum.Enum):
    MANAGER = "MANAGER"
    DEVELOPER = "DEVELOPER"
