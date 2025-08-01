import streamlit as st
import random
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styling import apply_custom_styling, load_css
from utils.state_management import initialize_session_state
from src._1_use_cases.mvp_service import MVPService
from src._1_use_cases.hackathon_service import HackathonService

# Configure page
st.set_page_config(
    page_title="Investor Feed - Vibratonic",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state and styling
initialize_session_state()
apply_custom_styling()
load_css("static/custom.css")

# Initialize services
mvp_service = MVPService()
hackathon_service = HackathonService()

st.markdown("# 💰 Investor Feed")

# Real-time activity simulation
if "last_activity_update" not in st.session_state:
    st.session_state.last_activity_update = datetime.now()

if "activity_feed" not in st.session_state:
    # Initialize with some activities
    st.session_state.activity_feed = [
        {
            "type": "funding",
            "message": "💰 **EcoTrack AI** received €500 from **GreenTech Ventures**",
            "timestamp": datetime.now() - timedelta(minutes=2),
            "amount": 500,
            "mvp": "EcoTrack AI",
            "investor": "GreenTech Ventures"
        },
        {
            "type": "milestone",
            "message": "🎯 **CryptoLend** reached 75% funding goal!",
            "timestamp": datetime.now() - timedelta(minutes=5),
            "mvp": "CryptoLend",
            "milestone": "75% funding goal"
        },
        {
            "type": "new_mvp",
            "message": "🚀 New MVP submitted: **HealthSync IoT Platform**",
            "timestamp": datetime.now() - timedelta(minutes=8),
            "mvp": "HealthSync IoT Platform"
        },
        {
            "type": "investor_joined",
            "message": "👥 **Alice Chen** joined **AI for Climate Change** hackathon",
            "timestamp": datetime.now() - timedelta(minutes=12),
            "investor": "Alice Chen",
            "hackathon": "AI for Climate Change"
        }
    ]

# Auto-refresh every 10 seconds (simulate real-time)
if datetime.now() - st.session_state.last_activity_update > timedelta(seconds=10):
    # Add new activity
    activities = [
        {
            "type": "funding",
            "message": f"💰 **{random.choice(['EcoTrack AI', 'CryptoLend', 'HealthSync'])}** received €{random.randint(100, 1000)} from **{random.choice(['TechFund', 'Innovation Capital', 'Startup Boost', 'Digital Ventures'])}**",
            "timestamp": datetime.now(),
            "amount": random.randint(100, 1000)
        },
        {
            "type": "milestone",
            "message": f"🎯 **{random.choice(['EcoTrack AI', 'CryptoLend', 'HealthSync'])}** reached {random.choice(['25%', '50%', '75%', '100%'])} funding goal!",
            "timestamp": datetime.now()
        },
        {
            "type": "investor_joined",
            "message": f"👥 **{random.choice(['Bob Smith', 'Carol Davis', 'David Kumar', 'Eva Wilson'])}** joined **{random.choice(['AI for Climate Change', 'FinTech Revolution', 'Health Tech Innovation'])}** hackathon",
            "timestamp": datetime.now()
        },
        {
            "type": "chat",
            "message": f"💬 **{random.choice(['Mike Johnson', 'Sarah Lee', 'Tom Brown'])}**: \"{random.choice(['Great project!', 'Very promising idea!', 'Love the tech stack!', 'When is the demo?'])}\"",
            "timestamp": datetime.now()
        }
    ]
    
    new_activity = random.choice(activities)
    st.session_state.activity_feed.insert(0, new_activity)
    st.session_state.last_activity_update = datetime.now()
    
    # Keep only last 20 activities
    st.session_state.activity_feed = st.session_state.activity_feed[:20]

# Live stats
col1, col2, col3, col4 = st.columns(4)

mvps = mvp_service.get_all_mvps()
hackathons = hackathon_service.get_all_hackathons()
total_funding = sum([mvp.current_funding for mvp in mvps])
active_investors = 47  # Mock number

with col1:
    st.metric("💰 Total Funding", f"€{total_funding:,.0f}", delta="€1,250")

with col2:
    funded_mvps = len([mvp for mvp in mvps if mvp.status.value == "funded"])
    st.metric("🚀 Funded MVPs", funded_mvps, delta="+2")

with col3:
    total_backers = sum([mvp.backers_count for mvp in mvps])
    st.metric("👥 Active Backers", total_backers, delta="+5")

with col4:
    st.metric("🔥 Live Investors", active_investors, delta="+3")

# Auto-refresh button
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### 📈 Live Activity Feed")
with col2:
    if st.button("🔄 Refresh", help="Auto-refreshes every 10 seconds"):
        st.rerun()

# Activity feed
with st.container():
    for i, activity in enumerate(st.session_state.activity_feed):
        time_ago = datetime.now() - activity["timestamp"]
        
        if time_ago.total_seconds() < 60:
            time_str = f"{int(time_ago.total_seconds())}s ago"
        elif time_ago.total_seconds() < 3600:
            time_str = f"{int(time_ago.total_seconds() / 60)}m ago"
        else:
            time_str = f"{int(time_ago.total_seconds() / 3600)}h ago"
        
        # Activity type styling
        if activity["type"] == "funding":
            border_color = "#00FFE1"
            bg_opacity = "0.1"
        elif activity["type"] == "milestone":
            border_color = "#FFD700"
            bg_opacity = "0.1"
        elif activity["type"] == "new_mvp":
            border_color = "#FF00A8"
            bg_opacity = "0.1"
        else:
            border_color = "#666666"
            bg_opacity = "0.05"
        
        st.markdown(f"""
        <div class="activity-card" style="border-left: 3px solid {border_color}; background: rgba(255,255,255,{bg_opacity}); margin-bottom: 10px; padding: 15px; border-radius: 8px;">
            <div style="display: flex; justify-content: between; align-items: center;">
                <div style="flex: 1;">
                    {activity["message"]}
                </div>
                <div style="color: #888; font-size: 0.9em; margin-left: 10px;">
                    {time_str}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Top Performers
st.markdown("### 🏆 Top Performing MVPs")

# Sort MVPs by funding
top_mvps = sorted(mvps, key=lambda x: x.current_funding, reverse=True)[:5]

for i, mvp in enumerate(top_mvps, 1):
    col1, col2, col3, col4, col5 = st.columns([0.5, 3, 1.5, 1, 1])
    
    with col1:
        # Medal icons
        if i == 1:
            st.markdown("🥇")
        elif i == 2:
            st.markdown("🥈")
        elif i == 3:
            st.markdown("🥉")
        else:
            st.markdown(f"#{i}")
    
    with col2:
        st.markdown(f"**{mvp.title}**")
        st.markdown(f"_{mvp.description[:60]}..._")
    
    with col3:
        funding_percentage = mvp.get_funding_percentage()
        st.progress(funding_percentage / 100)
        st.markdown(f"{funding_percentage:.1f}% funded")
    
    with col4:
        st.metric("Funding", f"€{mvp.current_funding:,.0f}")
    
    with col5:
        st.metric("Backers", mvp.backers_count)

st.markdown("---")

# Investment Opportunities
st.markdown("### 💡 Investment Opportunities")

# Filter MVPs that are accepting funding
funding_mvps = [mvp for mvp in mvps if mvp.status.value in ["submitted", "funded"] and mvp.get_funding_percentage() < 100]

if funding_mvps:
    for mvp in funding_mvps[:3]:
        with st.expander(f"🚀 {mvp.title} - Looking for €{sum(goal.amount for goal in mvp.funding_goals) - mvp.current_funding:,.0f}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(mvp.description)
                st.markdown(f"**Tech Stack:** {' • '.join(mvp.tech_stack[:4])}")
                
                # Funding tiers
                st.markdown("**Investment Tiers:**")
                for goal in mvp.funding_goals:
                    st.markdown(f"- **{goal.tier.value.title()}**: €{goal.amount:,.0f} - {goal.description}")
            
            with col2:
                funding_percentage = mvp.get_funding_percentage()
                st.metric("Progress", f"{funding_percentage:.1f}%")
                st.metric("Raised", f"€{mvp.current_funding:,.0f}")
                st.metric("Backers", mvp.backers_count)
                
                if st.button(f"💰 Invest in {mvp.title}", key=f"invest_{mvp.id}"):
                    st.session_state.investment_mvp = mvp.id
                    st.switch_page("pages/3_MVP_Showcase.py")

# Investor Leaderboard
st.markdown("---")
st.markdown("### 👑 Top Investors This Month")

# Mock investor data
top_investors = [
    {"name": "GreenTech Ventures", "invested": 5000, "projects": 8, "avatar": "🌱"},
    {"name": "Innovation Capital", "invested": 4200, "projects": 6, "avatar": "💡"},
    {"name": "TechFund", "invested": 3800, "projects": 5, "avatar": "🚀"},
    {"name": "Digital Boost", "invested": 3200, "projects": 4, "avatar": "💻"},
    {"name": "Startup Angels", "invested": 2900, "projects": 7, "avatar": "😇"}
]

for i, investor in enumerate(top_investors, 1):
    col1, col2, col3, col4, col5 = st.columns([0.5, 0.5, 2.5, 1.5, 1])
    
    with col1:
        if i <= 3:
            st.markdown(["🥇", "🥈", "🥉"][i-1])
        else:
            st.markdown(f"#{i}")
    
    with col2:
        st.markdown(investor["avatar"])
    
    with col3:
        st.markdown(f"**{investor['name']}**")
    
    with col4:
        st.markdown(f"€{investor['invested']:,} invested")
    
    with col5:
        st.markdown(f"{investor['projects']} projects")

# Chat/Comments Section
st.markdown("---")
st.markdown("### 💬 Community Chat")

# Mock chat messages
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"user": "Alice Chen", "message": "Great to see so many innovative projects!", "time": "2m ago", "avatar": "👩‍💼"},
        {"user": "Bob Wilson", "message": "EcoTrack AI looks very promising. When is the demo?", "time": "5m ago", "avatar": "👨‍💻"},
        {"user": "Carol Davis", "message": "Just funded CryptoLend! Excited to see where it goes.", "time": "8m ago", "avatar": "👩‍🚀"},
        {"user": "David Kumar", "message": "Love the diversity of projects this month.", "time": "12m ago", "avatar": "👨‍🔬"}
    ]

# Display chat messages
for msg in st.session_state.chat_messages:
    st.markdown(f"""
    <div class="chat-message">
        <span class="chat-avatar">{msg['avatar']}</span>
        <strong>{msg['user']}</strong>
        <span class="chat-time">({msg['time']})</span>
        <br>
        <span class="chat-text">{msg['message']}</span>
    </div>
    """, unsafe_allow_html=True)

# Chat input
with st.form("chat_form"):
    col1, col2 = st.columns([4, 1])
    with col1:
        new_message = st.text_input("Share your thoughts...", placeholder="What do you think about these projects?")
    with col2:
        send_button = st.form_submit_button("💬 Send", use_container_width=True)
    
    if send_button and new_message:
        st.session_state.chat_messages.insert(0, {
            "user": st.session_state.current_user.full_name,
            "message": new_message,
            "time": "now",
            "avatar": "👤"
        })
        st.rerun()

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("🚀 Browse MVPs", use_container_width=True):
        st.switch_page("pages/3_MVP_Showcase.py")

with col3:
    if st.button("👤 Profile", use_container_width=True):
        st.switch_page("pages/5_Profile.py")

# Auto-refresh the page every 30 seconds for live updates
st.markdown("""
<script>
setTimeout(function(){
    window.location.reload();
}, 30000);
</script>
""", unsafe_allow_html=True)
