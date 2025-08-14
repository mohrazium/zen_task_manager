import enum


class StatusEnum(str, enum.Enum):
    active = "active"
    suspended = "suspended"
    pending = "pending"
