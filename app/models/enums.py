from enum import StrEnum


class PredictDyslexia(StrEnum):
    YES = "YES"
    NO = "NO"
    MAYBE = "MAYBE"


class TestResult(StrEnum):
    DYSLEXIC = "DYSLEXIC"
    MAYBE_DYSLEXIC = "MAYBE_DYSLEXIC"
    NON_DYSLEXIC = "NON_DYSLEXIC"


class TestStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TestType(StrEnum):
    AUDITORY = "AUDITORY"
    VISUAL = "VISUAL"
    LANGUAGE = "LANGUAGE"


class OfficialDyslexiaDiagnosis(StrEnum):
    YES = "YES"
    NO = "NO"
    UNKNOWN = "UNKNOWN"


class AccountRole(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"


class ProfileType(StrEnum):
    PARENT = "PARENT"
    CHILD = "CHILD"


class Gender(StrEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
