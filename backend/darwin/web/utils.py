from enum import Enum


class MembershipEnum(Enum):
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
