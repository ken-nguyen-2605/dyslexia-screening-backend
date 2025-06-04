import enum

class TestStatusEnum(enum.Enum):
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    
class ParticipantTypeEnum(enum.Enum):
    USER = 'USER'
    GUEST = 'GUEST'