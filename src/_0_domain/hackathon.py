from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from enum import Enum

class HackathonStatus(Enum):
    DRAFT = "draft"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class Venue:
    name: str
    address: str
    latitude: float
    longitude: float
    capacity: int
    
@dataclass
class Hackathon:
    id: str
    title: str
    description: str
    venue: Venue
    start_datetime: datetime
    end_datetime: datetime
    max_participants: int
    current_participants: int = 0
    status: HackathonStatus = HackathonStatus.DRAFT
    theme: str = ""
    prize_pool: float = 0.0
    organizer_id: str = ""
    tags: List[str] = None
    requirements: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.requirements is None:
            self.requirements = []
    
    def is_full(self) -> bool:
        return self.current_participants >= self.max_participants
    
    def can_join(self) -> bool:
        return self.status == HackathonStatus.OPEN and not self.is_full()
    
    def get_progress_percentage(self) -> float:
        if self.max_participants == 0:
            return 0.0
        return (self.current_participants / self.max_participants) * 100
