from enum import StrEnum, auto


class ServiceEnum(StrEnum):
    AUTH = auto()
    UGC = auto()
    SCHEDULER = auto()
    ADMIN_PANEL = auto()


ALLOWED_SERVICES = [
    ServiceEnum.AUTH,
    ServiceEnum.SCHEDULER,
    ServiceEnum.ADMIN_PANEL,
    ServiceEnum.UGC,
]
