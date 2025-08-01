from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from datetime import datetime

class UserRole(Enum):
    GUEST = "guest"
    PARTICIPANT = "participant"
    INVESTOR = "investor"
    ORGANIZER = "organizer"
    ADMIN = "admin"

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

@dataclass
class UserProfile:
    id: str
    username: str
    email: str
    full_name: str
    role: UserRole
    status: UserStatus = UserStatus.ACTIVE
    avatar_url: str = ""
    bio: str = ""
    skills: List[str] = None
    github_username: str = ""
    linkedin_url: str = ""
    total_investments: float = 0.0
    total_funded_projects: int = 0
    created_hackathons: int = 0
    joined_hackathons: int = 0
    created_mvps: int = 0
    registration_date: Optional[datetime] = None
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = []
        if self.registration_date is None:
            self.registration_date = datetime.now()
    
    def can_create_hackathon(self) -> bool:
        return self.role in [UserRole.PARTICIPANT, UserRole.ORGANIZER, UserRole.ADMIN]
    
    def can_invest(self) -> bool:
        return self.role in [UserRole.INVESTOR, UserRole.ORGANIZER, UserRole.ADMIN]
    
    def can_admin(self) -> bool:
        return self.role == UserRole.ADMIN
