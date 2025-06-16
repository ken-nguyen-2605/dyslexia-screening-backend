from enum import Enum

class TestStatus(Enum):
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    
class ParticipantType(Enum):
    USER = 'USER'
    GUEST = 'GUEST'
    
class Gender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'