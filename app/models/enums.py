from enum import StrEnum

class TestStatus(StrEnum):
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    
class TestDifficulty(StrEnum):
    BASIC = "BASIC"
    ADVANCED = "ADVANCED"
    
class ProfileType(StrEnum):
    PARENT = 'PARENT'
    CHILD = 'CHILD'
    
class Gender(StrEnum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'