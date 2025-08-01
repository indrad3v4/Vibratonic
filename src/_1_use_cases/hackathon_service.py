from typing import List, Optional
from datetime import datetime
from src._0_domain.hackathon import Hackathon, Venue, HackathonStatus
from src._0_domain.user import UserProfile

class HackathonService:
    def __init__(self):
        self._hackathons = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample hackathons for demonstration"""
        sample_venues = [
            Venue("TechHub Warsaw", "Rondo ONZ 1, Warsaw", 52.2297, 21.0122, 100),
            Venue("Innovation Center Krakow", "Rynek Główny 1, Krakow", 50.0647, 19.9450, 80),
            Venue("Digital Campus Gdansk", "Długi Targ 1, Gdansk", 54.3520, 18.6466, 60),
            Venue("StartupLab Berlin", "Potsdamer Platz 1, Berlin", 52.5096, 13.3765, 120),
            Venue("Innovation Hub Amsterdam", "Dam Square 1, Amsterdam", 52.3702, 4.8952, 90)
        ]
        
        sample_hackathons = [
            Hackathon(
                id="hack001",
                title="AI for Climate Change",
                description="Build AI solutions to combat climate change and create sustainable technologies.",
                venue=sample_venues[0],
                start_datetime=datetime(2025, 8, 15, 10, 0),
                end_datetime=datetime(2025, 8, 17, 18, 0),
                max_participants=100,
                current_participants=67,
                status=HackathonStatus.OPEN,
                theme="Sustainability & AI",
                prize_pool=10000.0,
                organizer_id="org001",
                tags=["AI", "Climate", "Sustainability", "Machine Learning"],
                requirements=["Python experience", "Basic ML knowledge"]
            ),
            Hackathon(
                id="hack002",
                title="FinTech Revolution",
                description="Create the next generation of financial technology solutions.",
                venue=sample_venues[1],
                start_datetime=datetime(2025, 8, 22, 9, 0),
                end_datetime=datetime(2025, 8, 24, 17, 0),
                max_participants=80,
                current_participants=45,
                status=HackathonStatus.OPEN,
                theme="Financial Technology",
                prize_pool=15000.0,
                organizer_id="org002",
                tags=["FinTech", "Blockchain", "Payment", "DeFi"],
                requirements=["JavaScript/Python", "API development"]
            ),
            Hackathon(
                id="hack003",
                title="Health Tech Innovation",
                description="Develop healthcare solutions using cutting-edge technology.",
                venue=sample_venues[2],
                start_datetime=datetime(2025, 9, 5, 10, 0),
                end_datetime=datetime(2025, 9, 7, 16, 0),
                max_participants=60,
                current_participants=60,
                status=HackathonStatus.IN_PROGRESS,
                theme="Healthcare Technology",
                prize_pool=8000.0,
                organizer_id="org003",
                tags=["HealthTech", "IoT", "Mobile", "Data Analytics"],
                requirements=["Mobile development", "Data analysis"]
            )
        ]
        
        for hackathon in sample_hackathons:
            self._hackathons[hackathon.id] = hackathon
    
    def create_hackathon(self, hackathon_data: dict, organizer: UserProfile) -> Hackathon:
        """Create a new hackathon"""
        hackathon_id = f"hack{len(self._hackathons) + 1:03d}"
        
        venue = Venue(
            name=hackathon_data.get("venue_name", ""),
            address=hackathon_data.get("venue_address", ""),
            latitude=hackathon_data.get("latitude", 0.0),
            longitude=hackathon_data.get("longitude", 0.0),
            capacity=hackathon_data.get("max_participants", 50)
        )
        
        hackathon = Hackathon(
            id=hackathon_id,
            title=hackathon_data.get("title", ""),
            description=hackathon_data.get("description", ""),
            venue=venue,
            start_datetime=hackathon_data.get("start_datetime"),
            end_datetime=hackathon_data.get("end_datetime"),
            max_participants=hackathon_data.get("max_participants", 50),
            theme=hackathon_data.get("theme", ""),
            prize_pool=hackathon_data.get("prize_pool", 0.0),
            organizer_id=organizer.id,
            tags=hackathon_data.get("tags", []),
            requirements=hackathon_data.get("requirements", [])
        )
        
        self._hackathons[hackathon_id] = hackathon
        return hackathon
    
    def get_all_hackathons(self) -> List[Hackathon]:
        """Get all hackathons"""
        return list(self._hackathons.values())
    
    def get_hackathon(self, hackathon_id: str) -> Optional[Hackathon]:
        """Get hackathon by ID"""
        return self._hackathons.get(hackathon_id)
    
    def get_open_hackathons(self) -> List[Hackathon]:
        """Get all open hackathons"""
        return [h for h in self._hackathons.values() if h.status == HackathonStatus.OPEN]
    
    def join_hackathon(self, hackathon_id: str, user: UserProfile) -> bool:
        """Join a hackathon"""
        hackathon = self._hackathons.get(hackathon_id)
        if hackathon and hackathon.can_join():
            hackathon.current_participants += 1
            return True
        return False
    
    def update_hackathon_status(self, hackathon_id: str, status: HackathonStatus) -> bool:
        """Update hackathon status"""
        hackathon = self._hackathons.get(hackathon_id)
        if hackathon:
            hackathon.status = status
            return True
        return False
