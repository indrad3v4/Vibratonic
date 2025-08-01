from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from enum import Enum

class MVPStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    FUNDED = "funded"
    COMPLETED = "completed"

class FundingTier(Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

@dataclass
class MediaFile:
    url: str
    type: str  # 'image', 'video', 'demo'
    title: str
    description: str = ""

@dataclass
class FundingGoal:
    tier: FundingTier
    amount: float
    description: str
    rewards: List[str]

@dataclass
class MVP:
    id: str
    hackathon_id: str
    creator_id: str
    title: str
    description: str
    tech_stack: List[str]
    github_url: str = ""
    demo_url: str = ""
    media_files: List[MediaFile] = None
    funding_goals: List[FundingGoal] = None
    current_funding: float = 0.0
    backers_count: int = 0
    status: MVPStatus = MVPStatus.DRAFT
    submission_datetime: Optional[datetime] = None
    
    def __post_init__(self):
        if self.media_files is None:
            self.media_files = []
        if self.funding_goals is None:
            self.funding_goals = []
        if self.tech_stack is None:
            self.tech_stack = []
    
    def get_funding_percentage(self) -> float:
        total_goal = sum(goal.amount for goal in self.funding_goals)
        if total_goal == 0:
            return 0.0
        return min((self.current_funding / total_goal) * 100, 100.0)
    
    def get_platform_fee(self, amount: float) -> float:
        return amount * 0.20  # 20% platform fee
    
    def get_creator_amount(self, amount: float) -> float:
        return amount - self.get_platform_fee(amount)
