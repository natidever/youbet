from enum import Enum


class UserRole(str,Enum):
    ADMIN="admin"
    CASINO="casino"
    AGENT="agent"