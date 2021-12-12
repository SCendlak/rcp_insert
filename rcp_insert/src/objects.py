from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BasePayload:
    email: str = field(init=False)
    password: str = field(init=False)
    request_verification_token: Optional[str] = field(init=False)

    def auth_tuple(self) -> tuple:
        return self.email, self.password

    def to_dict(self):
        return {
            "Email": self.email,
            "Password": self.password,
            "__RequestVerificationToken": self.request_verification_token
        }

    @classmethod
    def set_instance(cls, insert_dict: dict):
        new = cls()
        for key, val in insert_dict.items():
            setattr(new, key, val)
        return new


@dataclass
class FirstPayload(BasePayload):
    time_zone: str = field(init=False)
    time_utc_unix: str = field(init=False)

    @staticmethod
    def set_time_zone() -> str:
        return str(int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()))

    @classmethod
    def set_instance(cls, insert_dict: dict):
        new = cls()
        for key, val in insert_dict.items():
            setattr(new, key, val)
        return new

    def to_dict(self):
        return {
            "UserEmail": self.email,
            "Password": self.password,
            "TimeZone": self.time_zone,
            "TimeUtcUnix": self.time_utc_unix
        }

    def __post_init__(self):
        self.time_zone = "Europe/Warsaw"
        self.time_utc_unix = self.set_time_zone()


@dataclass
class SecondPayload:
    status_id: str = field(init=False)
    qr: str = field(init=False)
    is_end: str = field(init=False)
    time_local_unix: str = field(init=False)
    time_utc_unix: str = field(init=False)
    time_zone_id: str = field(init=False)

    @classmethod
    def set_instance(cls, insert_dict: dict):
        new = cls()
        for key, val in insert_dict.items():
            setattr(new, key, val)
        return new

    def to_dict(self):
        return {
                "StatusId": self.status_id,
                "QrCode": self.qr,
                "TimeUtcUnix": self.time_utc_unix,
                "TimeLocalUnix": self.time_local_unix,
                "IsEnd": self.is_end,
                "TimeZoneId": self.time_zone_id
                    }
