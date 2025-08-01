import streamlit as st
from datetime import datetime
from src._0_domain.user import UserProfile, UserRole, UserStatus

def initialize_session_state():
    """Initialize all necessary session state variables"""
    
    # Current page tracking
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    
    # User authentication and profile
    if "current_user" not in st.session_state:
        st.session_state.current_user = create_demo_user()
    
    # Wizard state for hackathon creation
    if "wizard_step" not in st.session_state:
        st.session_state.wizard_step = 1
    
    if "hackathon_data" not in st.session_state:
        st.session_state.hackathon_data = {}
    
    # Modal states
    if "funding_modal_mvp" not in st.session_state:
        st.session_state.funding_modal_mvp = None
    
    if "mvp_details" not in st.session_state:
        st.session_state.mvp_details = None
    
    # Filter states
    if "hackathon_filter" not in st.session_state:
        st.session_state.hackathon_filter = "All"
    
    if "mvp_filter" not in st.session_state:
        st.session_state.mvp_filter = "All"
    
    # Activity feed state
    if "activity_feed" not in st.session_state:
        st.session_state.activity_feed = []
    
    if "last_activity_update" not in st.session_state:
        st.session_state.last_activity_update = datetime.now()
    
    # Chat state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # Notification state
    if "notifications" not in st.session_state:
        st.session_state.notifications = []
    
    # Theme preferences
    if "theme_preference" not in st.session_state:
        st.session_state.theme_preference = "neon"
    
    # Language preference
    if "language" not in st.session_state:
        st.session_state.language = "en"
    
    # Draft storage for offline capabilities
    if "drafts" not in st.session_state:
        st.session_state.drafts = {}

def create_demo_user():
    """Create a demo user for the session"""
    return UserProfile(
        id="user001",
        username="demo_creator",
        email="creator@vibratonic.app",
        full_name="Demo Creator",
        role=UserRole.PARTICIPANT,
        status=UserStatus.ACTIVE,
        bio="Passionate hackathon creator and tech innovator building the future of collaborative development.",
        skills=["Python", "React", "AI/ML", "Blockchain", "IoT", "Mobile Development"],
        github_username="demo_creator",
        linkedin_url="https://linkedin.com/in/democreator",
        total_investments=2500.0,
        total_funded_projects=3,
        created_hackathons=2,
        joined_hackathons=5,
        created_mvps=4,
        registration_date=datetime(2025, 1, 15)
    )

def save_draft(key, data):
    """Save draft data for offline capabilities"""
    st.session_state.drafts[key] = {
        "data": data,
        "timestamp": datetime.now(),
        "user_id": st.session_state.current_user.id
    }

def load_draft(key):
    """Load draft data"""
    return st.session_state.drafts.get(key, {}).get("data")

def clear_draft(key):
    """Clear a specific draft"""
    if key in st.session_state.drafts:
        del st.session_state.drafts[key]

def get_user_preference(key, default=None):
    """Get user preference"""
    return st.session_state.get(f"pref_{key}", default)

def set_user_preference(key, value):
    """Set user preference"""
    st.session_state[f"pref_{key}"] = value

def add_notification(message, type="info", duration=5):
    """Add a notification to the queue"""
    notification = {
        "id": f"notif_{datetime.now().timestamp()}",
        "message": message,
        "type": type,
        "timestamp": datetime.now(),
        "duration": duration,
        "read": False
    }
    st.session_state.notifications.append(notification)

def mark_notification_read(notification_id):
    """Mark a notification as read"""
    for notif in st.session_state.notifications:
        if notif["id"] == notification_id:
            notif["read"] = True
            break

def clear_notifications():
    """Clear all notifications"""
    st.session_state.notifications = []

def get_unread_notifications():
    """Get unread notifications"""
    return [n for n in st.session_state.notifications if not n["read"]]

def switch_user_role(new_role):
    """Switch user role (for demo purposes)"""
    if isinstance(new_role, str):
        new_role = UserRole(new_role)
    
    st.session_state.current_user.role = new_role
    add_notification(f"Role switched to {new_role.value.title()}", "success")

def reset_session():
    """Reset session to initial state"""
    keys_to_keep = ["current_user"]  # Keep user logged in
    
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]
    
    # Reinitialize
    initialize_session_state()

def cache_data(key, data, expiry_minutes=30):
    """Cache data with expiry"""
    cache_key = f"cache_{key}"
    st.session_state[cache_key] = {
        "data": data,
        "timestamp": datetime.now(),
        "expiry_minutes": expiry_minutes
    }

def get_cached_data(key):
    """Get cached data if not expired"""
    cache_key = f"cache_{key}"
    cached = st.session_state.get(cache_key)
    
    if not cached:
        return None
    
    # Check if expired
    time_diff = datetime.now() - cached["timestamp"]
    if time_diff.total_seconds() > (cached["expiry_minutes"] * 60):
        del st.session_state[cache_key]
        return None
    
    return cached["data"]

def update_user_activity(activity_type, details=None):
    """Update user activity log"""
    activity_key = "user_activity"
    
    if activity_key not in st.session_state:
        st.session_state[activity_key] = []
    
    activity = {
        "type": activity_type,
        "details": details,
        "timestamp": datetime.now(),
        "user_id": st.session_state.current_user.id
    }
    
    st.session_state[activity_key].append(activity)
    
    # Keep only last 50 activities
    st.session_state[activity_key] = st.session_state[activity_key][-50:]

def get_user_activity():
    """Get user activity log"""
    return st.session_state.get("user_activity", [])

def is_mobile():
    """Check if user is on mobile device (simplified check)"""
    # This is a simplified check - in production, you'd use JavaScript
    return st.session_state.get("is_mobile", False)

def set_mobile_mode(is_mobile_device):
    """Set mobile mode"""
    st.session_state.is_mobile = is_mobile_device

def get_wizard_progress():
    """Get wizard completion progress"""
    step = st.session_state.get("wizard_step", 1)
    total_steps = 5
    return (step / total_steps) * 100

def validate_session():
    """Validate session integrity"""
    # Check if required session variables exist
    required_keys = ["current_user", "current_page"]
    
    for key in required_keys:
        if key not in st.session_state:
            initialize_session_state()
            return False
    
    # Check if user object is valid
    user = st.session_state.current_user
    if not hasattr(user, 'id') or not hasattr(user, 'role'):
        st.session_state.current_user = create_demo_user()
        return False
    
    return True

def sync_user_preferences():
    """Sync user preferences (placeholder for backend sync)"""
    # In production, this would sync with backend
    preferences = {
        "theme": st.session_state.get("theme_preference", "neon"),
        "language": st.session_state.get("language", "en"),
        "notifications": st.session_state.get("notification_preferences", {}),
        "layout": st.session_state.get("layout_preference", "default")
    }
    
    # Cache preferences
    cache_data("user_preferences", preferences, expiry_minutes=1440)  # 24 hours
    
    return preferences

def restore_user_preferences():
    """Restore user preferences from cache"""
    preferences = get_cached_data("user_preferences")
    
    if preferences:
        st.session_state.theme_preference = preferences.get("theme", "neon")
        st.session_state.language = preferences.get("language", "en")
        st.session_state.notification_preferences = preferences.get("notifications", {})
        st.session_state.layout_preference = preferences.get("layout", "default")
        
        return True
    
    return False
