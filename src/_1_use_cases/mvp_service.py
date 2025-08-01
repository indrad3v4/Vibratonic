from typing import List, Optional
from datetime import datetime
from src._0_domain.mvp import MVP, MediaFile, FundingGoal, MVPStatus, FundingTier
from src._0_domain.user import UserProfile

class MVPService:
    def __init__(self):
        self._mvps = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample MVPs for demonstration"""
        sample_mvps = [
            MVP(
                id="mvp001",
                hackathon_id="hack001",
                creator_id="user001",
                title="EcoTrack AI",
                description="AI-powered carbon footprint tracking app that helps individuals and businesses monitor and reduce their environmental impact through smart recommendations.",
                tech_stack=["Python", "TensorFlow", "React", "Node.js", "MongoDB"],
                github_url="https://github.com/creator/ecotrack-ai",
                demo_url="https://ecotrack-demo.app",
                media_files=[
                    MediaFile("https://via.placeholder.com/800x600/00FFE1/FFFFFF?text=EcoTrack+Demo", "image", "App Screenshot"),
                    MediaFile("https://via.placeholder.com/800x450/FF00A8/FFFFFF?text=Demo+Video", "video", "Demo Video")
                ],
                funding_goals=[
                    FundingGoal(FundingTier.BASIC, 5000.0, "MVP Development", ["Early access", "Updates"]),
                    FundingGoal(FundingTier.PREMIUM, 15000.0, "Full App Launch", ["Premium features", "Custom analytics"]),
                    FundingGoal(FundingTier.ENTERPRISE, 50000.0, "Enterprise Solution", ["White-label", "API access", "Priority support"])
                ],
                current_funding=8750.0,
                backers_count=23,
                status=MVPStatus.SUBMITTED,
                submission_datetime=datetime(2025, 8, 16, 14, 30)
            ),
            MVP(
                id="mvp002",
                hackathon_id="hack002",
                creator_id="user002",
                title="CryptoLend",
                description="Decentralized lending platform that connects borrowers and lenders using smart contracts, enabling transparent and secure peer-to-peer lending.",
                tech_stack=["Solidity", "Web3.js", "React", "Node.js", "IPFS"],
                github_url="https://github.com/creator/cryptolend",
                demo_url="https://cryptolend-demo.web3.app",
                media_files=[
                    MediaFile("https://via.placeholder.com/800x600/FFD700/000000?text=CryptoLend+UI", "image", "Platform Interface"),
                    MediaFile("https://via.placeholder.com/800x450/00FFE1/000000?text=Smart+Contract", "image", "Smart Contract Flow")
                ],
                funding_goals=[
                    FundingGoal(FundingTier.BASIC, 10000.0, "Platform Beta", ["Beta access", "Governance tokens"]),
                    FundingGoal(FundingTier.PREMIUM, 25000.0, "Full Launch", ["Premium rates", "Advanced features"]),
                    FundingGoal(FundingTier.ENTERPRISE, 75000.0, "Enterprise Suite", ["White-label", "Custom pools", "Dedicated support"])
                ],
                current_funding=12500.0,
                backers_count=31,
                status=MVPStatus.FUNDED,
                submission_datetime=datetime(2025, 8, 23, 16, 45)
            ),
            MVP(
                id="mvp003",
                hackathon_id="hack003",
                creator_id="user003",
                title="HealthSync",
                description="IoT-based health monitoring system that syncs with wearable devices to provide real-time health insights and emergency alerts.",
                tech_stack=["Python", "IoT", "React Native", "AWS", "TensorFlow"],
                github_url="https://github.com/creator/healthsync",
                demo_url="https://healthsync-demo.app",
                media_files=[
                    MediaFile("https://via.placeholder.com/800x600/FF00A8/FFFFFF?text=HealthSync+App", "image", "Mobile App"),
                    MediaFile("https://via.placeholder.com/800x450/00FFE1/FFFFFF?text=IoT+Dashboard", "image", "IoT Dashboard")
                ],
                funding_goals=[
                    FundingGoal(FundingTier.BASIC, 7500.0, "MVP Launch", ["Early access", "Basic monitoring"]),
                    FundingGoal(FundingTier.PREMIUM, 20000.0, "Advanced Features", ["AI insights", "Emergency alerts"]),
                    FundingGoal(FundingTier.ENTERPRISE, 60000.0, "Healthcare Integration", ["EMR integration", "Compliance", "Multi-user"])
                ],
                current_funding=15750.0,
                backers_count=42,
                status=MVPStatus.FUNDED,
                submission_datetime=datetime(2025, 9, 6, 11, 15)
            )
        ]
        
        for mvp in sample_mvps:
            self._mvps[mvp.id] = mvp
    
    def create_mvp(self, mvp_data: dict, creator: UserProfile) -> MVP:
        """Create a new MVP"""
        mvp_id = f"mvp{len(self._mvps) + 1:03d}"
        
        mvp = MVP(
            id=mvp_id,
            hackathon_id=mvp_data.get("hackathon_id", ""),
            creator_id=creator.id,
            title=mvp_data.get("title", ""),
            description=mvp_data.get("description", ""),
            tech_stack=mvp_data.get("tech_stack", []),
            github_url=mvp_data.get("github_url", ""),
            demo_url=mvp_data.get("demo_url", ""),
            funding_goals=mvp_data.get("funding_goals", [])
        )
        
        self._mvps[mvp_id] = mvp
        return mvp
    
    def get_all_mvps(self) -> List[MVP]:
        """Get all MVPs"""
        return list(self._mvps.values())
    
    def get_mvp(self, mvp_id: str) -> Optional[MVP]:
        """Get MVP by ID"""
        return self._mvps.get(mvp_id)
    
    def get_mvps_by_hackathon(self, hackathon_id: str) -> List[MVP]:
        """Get MVPs for a specific hackathon"""
        return [mvp for mvp in self._mvps.values() if mvp.hackathon_id == hackathon_id]
    
    def get_funded_mvps(self) -> List[MVP]:
        """Get all funded MVPs"""
        return [mvp for mvp in self._mvps.values() if mvp.status == MVPStatus.FUNDED]
    
    def add_funding(self, mvp_id: str, amount: float, backer_id: str) -> bool:
        """Add funding to an MVP"""
        mvp = self._mvps.get(mvp_id)
        if mvp and mvp.status in [MVPStatus.SUBMITTED, MVPStatus.FUNDED]:
            mvp.current_funding += amount
            mvp.backers_count += 1
            if mvp.current_funding >= sum(goal.amount for goal in mvp.funding_goals):
                mvp.status = MVPStatus.FUNDED
            return True
        return False
    
    def update_mvp_status(self, mvp_id: str, status: MVPStatus) -> bool:
        """Update MVP status"""
        mvp = self._mvps.get(mvp_id)
        if mvp:
            mvp.status = status
            return True
        return False
