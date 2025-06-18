from enum import StrEnum

class TestStatus(StrEnum):
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    
class ParticipantType(StrEnum):
    USER = 'USER'
    GUEST = 'GUEST'
    
class Gender(StrEnum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    
class QuestionCategory(StrEnum):
    AUDITORY = 'auditory'
    VISUAL = 'visual'
    LANGUAGE = 'language'
    
class AuditoryQuestionType(StrEnum):
    FREQ_4_CARDS = 'FREQ_4_CARDS'
    FREQ_6_CARDS = 'FREQ_6_CARDS'
    LEN_4_CARDS = 'LEN_4_CARDS'
    LEN_6_CARDS = 'LEN_6_CARDS'
    RISE_4_CARDS = 'RISE_4_CARDS'
    RISE_6_CARDS = 'RISE_6_CARDS'
    RHY_4_CARDS = 'RHY_4_CARDS'
    RHY_6_CARDS = 'RHY_6_CARDS'
    
class VisualQuestionType(StrEnum):
    SYMBOL_4_CARDS = 'SYMBOL_4_CARDS'
    SYMBOL_6_CARDS = 'SYMBOL_6_CARDS'
    Z_4_CARDS = 'Z_4_CARDS'
    Z_6_CARDS = 'Z_6_CARDS'
    REC_4_CARDS = 'REC_4_CARDS'
    REC_6_CARDS = 'REC_6_CARDS'
    FACE_4_CARDS = 'FACE_4_CARDS'
    FACE_6_CARDS = 'FACE_6_CARDS'
    
class LanguageQuestionType(StrEnum):
    VOWELS = 'VOWELS'
    CONSONANTS = 'CONSONANTS'
    LETTERS = 'LETTERS'
    REMOVE_1_LETTER = 'REMOVE_1_LETTER'
    ADD_1_LETTER = 'ADD_1_LETTER'
    REPLACE_1_LETTER = 'REPLACE_1_LETTER'
    
class AuditoryProgress(StrEnum):
    FREQ_4_CARDS = AuditoryQuestionType.FREQ_4_CARDS
    FREQ_6_CARDS = AuditoryQuestionType.FREQ_6_CARDS
    LEN_4_CARDS = AuditoryQuestionType.LEN_4_CARDS
    LEN_6_CARDS = AuditoryQuestionType.LEN_6_CARDS
    RISE_4_CARDS = AuditoryQuestionType.RISE_4_CARDS
    RISE_6_CARDS = AuditoryQuestionType.RISE_6_CARDS
    RHY_4_CARDS = AuditoryQuestionType.RHY_4_CARDS
    RHY_6_CARDS = AuditoryQuestionType.RHY_6_CARDS
    FEEDBACK = "FEEDBACK"
    COMPLETED = "COMPLETED"
    
class VisualProgress(StrEnum):
    SYMBOL_4_CARDS = VisualQuestionType.SYMBOL_4_CARDS
    SYMBOL_6_CARDS = VisualQuestionType.SYMBOL_6_CARDS
    Z_4_CARDS = VisualQuestionType.Z_4_CARDS
    Z_6_CARDS = VisualQuestionType.Z_6_CARDS
    REC_4_CARDS = VisualQuestionType.REC_4_CARDS
    REC_6_CARDS = VisualQuestionType.REC_6_CARDS
    FACE_4_CARDS = VisualQuestionType.FACE_4_CARDS
    FACE_6_CARDS = VisualQuestionType.FACE_6_CARDS
    FEEDBACK = "FEEDBACK"
    COMPLETED = "COMPLETED"
    
class LanguageProgress(StrEnum):
    VOWELS = LanguageQuestionType.VOWELS
    CONSONANTS = LanguageQuestionType.CONSONANTS
    LETTERS = LanguageQuestionType.LETTERS
    REMOVE_1_LETTER = LanguageQuestionType.REMOVE_1_LETTER
    ADD_1_LETTER = LanguageQuestionType.ADD_1_LETTER
    REPLACE_1_LETTER = LanguageQuestionType.REPLACE_1_LETTER
    FEEDBACK = "FEEDBACK"
    COMPLETED = "COMPLETED"