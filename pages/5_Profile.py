import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styling import apply_custom_styling, load_css
from utils.state_management import initialize_session_state
from src._1_use_cases.mvp_service import MVPService
from src._1_use_cases.hackathon_service import HackathonService
from src._0_domain.user import UserRole

# Configure page
st.set_page_config(
    page_title="Profile - Vibratonic",
    page_icon="👤",
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

st.markdown("# 👤 Profile")

user = st.session_state.current_user

# Profile Header
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown(f"""
    <div class="profile-avatar-large">
        <div class="avatar-circle-large">
            {user.full_name[0].upper()}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"## {user.full_name}")
    st.markdown(f"**@{user.username}** • {user.role.value.title()}")
    st.markdown(f"📧 {user.email}")
    
    if user.bio:
        st.markdown(f"*{user.bio}*")
    
    # Social links
    links = []
    if user.github_username:
        links.append(f"[🔗 GitHub](https://github.com/{user.github_username})")
    if user.linkedin_url:
        links.append(f"[💼 LinkedIn]({user.linkedin_url})")
    
    if links:
        st.markdown(" • ".join(links))

st.markdown("---")

# Profile Stats
st.markdown("### 📊 Your Stats")

col1, col2, col3, col4 = st.columns(4)

# Get user's activities
user_hackathons = [h for h in hackathon_service.get_all_hackathons() if h.organizer_id == user.id]
user_mvps = [mvp for mvp in mvp_service.get_all_mvps() if mvp.creator_id == user.id]
total_funding_received = sum([mvp.current_funding for mvp in user_mvps])

with col1:
    st.metric("🎯 Hackathons Created", len(user_hackathons))

with col2:
    st.metric("🚀 MVPs Created", len(user_mvps))

with col3:
    st.metric("💰 Total Funding Received", f"€{total_funding_received:,.0f}")

with col4:
    st.metric("👥 Total Investments", f"€{user.total_investments:,.0f}")

# Skills section
if user.skills:
    st.markdown("### 🛠️ Skills")
    st.markdown(' '.join([f'<span class="skill-tag">{skill}</span>' for skill in user.skills]), unsafe_allow_html=True)

st.markdown("---")

# Tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["🎯 My Hackathons", "🚀 My MVPs", "💰 Investments", "⚙️ Settings"])

with tab1:
    st.markdown("### 🎯 My Hackathons")
    
    if user_hackathons:
        for hackathon in user_hackathons:
            progress = hackathon.get_progress_percentage()
            status_color = "#00FFE1" if hackathon.status.value == "open" else "#FF00A8" if hackathon.status.value == "completed" else "#FFD700"
            
            st.markdown(f"""
            <div class="hack-card-profile">
                <div class="hack-header">
                    <h4>{hackathon.title}</h4>
                    <span style="color: {status_color};">{hackathon.status.value.upper()}</span>
                </div>
                <p>{hackathon.description[:120]}...</p>
                <div class="hack-stats">
                    <span>📍 {hackathon.venue.name}</span>
                    <span>👥 {hackathon.current_participants}/{hackathon.max_participants}</span>
                    <span>💰 €{hackathon.prize_pool:,}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%; background: {status_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"📊 View Analytics", key=f"analytics_{hackathon.id}"):
                    st.info(f"Analytics for {hackathon.title} would be displayed here")
            with col2:
                if st.button(f"✏️ Edit", key=f"edit_{hackathon.id}"):
                    st.info(f"Edit form for {hackathon.title} would be displayed here")
            with col3:
                if st.button(f"🗺️ View on Map", key=f"map_{hackathon.id}"):
                    st.switch_page("pages/2_Map_View.py")
            
            st.markdown("---")
    else:
        st.info("🎯 You haven't created any hackathons yet. Ready to start your first one?")
        if st.button("🚀 Create Your First Hackathon", use_container_width=True):
            st.switch_page("pages/1_Create_Hackathon.py")

with tab2:
    st.markdown("### 🚀 My MVPs")
    
    if user_mvps:
        for mvp in user_mvps:
            funding_percentage = mvp.get_funding_percentage()
            total_goal = sum(goal.amount for goal in mvp.funding_goals)
            status_color = "#00FFE1" if mvp.status.value == "funded" else "#FFD700" if mvp.status.value == "submitted" else "#FF00A8"
            
            st.markdown(f"""
            <div class="mvp-card-profile">
                <div class="mvp-header">
                    <h4>{mvp.title}</h4>
                    <span style="color: {status_color};">{mvp.status.value.upper()}</span>
                </div>
                <p>{mvp.description}</p>
                <div class="mvp-tech">
                    {' '.join([f'<span class="tech-tag-small">{tech}</span>' for tech in mvp.tech_stack[:4]])}
                </div>
                <div class="mvp-funding-info">
                    <div class="funding-progress">
                        <div class="funding-bar">
                            <div class="funding-fill" style="width: {funding_percentage}%; background: {status_color};"></div>
                        </div>
                        <span>€{mvp.current_funding:,.0f} / €{total_goal:,.0f} ({funding_percentage:.1f}%)</span>
                    </div>
                    <span>{mvp.backers_count} backers</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button(f"📊 Analytics", key=f"mvp_analytics_{mvp.id}"):
                    st.info(f"Analytics for {mvp.title} would be displayed here")
            with col2:
                if st.button(f"✏️ Edit", key=f"mvp_edit_{mvp.id}"):
                    st.info(f"Edit form for {mvp.title} would be displayed here")
            with col3:
                if mvp.demo_url:
                    st.link_button(f"🌐 Demo", mvp.demo_url)
                else:
                    st.button("🌐 No Demo", disabled=True)
            with col4:
                if mvp.github_url:
                    st.link_button(f"🔗 GitHub", mvp.github_url)
                else:
                    st.button("🔗 No Repo", disabled=True)
            
            st.markdown("---")
    else:
        st.info("🚀 You haven't created any MVPs yet. Participate in a hackathon to get started!")
        if st.button("🗺️ Find Hackathons", use_container_width=True):
            st.switch_page("pages/2_Map_View.py")

with tab3:
    st.markdown("### 💰 Investment History")
    
    # Mock investment data for demonstration
    investments = [
        {"mvp": "EcoTrack AI", "amount": 500, "date": "2025-07-28", "status": "Active"},
        {"mvp": "CryptoLend", "amount": 1000, "date": "2025-07-25", "status": "Active"},
        {"mvp": "HealthSync", "amount": 250, "date": "2025-07-20", "status": "Completed"}
    ]
    
    if user.role in [UserRole.INVESTOR, UserRole.ORGANIZER, UserRole.ADMIN]:
        total_invested = sum([inv["amount"] for inv in investments])
        active_investments = len([inv for inv in investments if inv["status"] == "Active"])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 Total Invested", f"€{total_invested:,}")
        with col2:
            st.metric("📈 Active Investments", active_investments)
        with col3:
            st.metric("🎯 Projects Funded", len(investments))
        
        st.markdown("#### Investment Details")
        for inv in investments:
            status_color = "#00FFE1" if inv["status"] == "Active" else "#FFD700"
            st.markdown(f"""
            <div class="investment-item">
                <div class="investment-header">
                    <strong>{inv['mvp']}</strong>
                    <span style="color: {status_color};">{inv['status']}</span>
                </div>
                <div class="investment-details">
                    <span>💰 €{inv['amount']}</span>
                    <span>📅 {inv['date']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💰 Investment features are available for Investors, Organizers, and Admins.")
        st.markdown("Upgrade your account to start investing in innovative projects!")

with tab4:
    st.markdown("### ⚙️ Profile Settings")
    
    with st.form("profile_settings"):
        st.markdown("#### Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            new_full_name = st.text_input("Full Name", value=user.full_name)
            new_email = st.text_input("Email", value=user.email)
        with col2:
            new_username = st.text_input("Username", value=user.username)
            new_bio = st.text_area("Bio", value=user.bio, height=100)
        
        st.markdown("#### Social Links")
        col1, col2 = st.columns(2)
        with col1:
            new_github = st.text_input("GitHub Username", value=user.github_username)
        with col2:
            new_linkedin = st.text_input("LinkedIn URL", value=user.linkedin_url)
        
        st.markdown("#### Skills")
        skills_text = ", ".join(user.skills)
        new_skills = st.text_input("Skills (comma-separated)", value=skills_text)
        
        st.markdown("#### Account Settings")
        role_options = [role.value for role in UserRole if role != UserRole.GUEST]
        current_role_index = role_options.index(user.role.value)
        new_role = st.selectbox("Account Type", role_options, index=current_role_index)
        
        # Notification preferences
        st.markdown("#### Notification Preferences")
        col1, col2 = st.columns(2)
        with col1:
            email_notifications = st.checkbox("Email Notifications", value=True)
            funding_alerts = st.checkbox("Funding Alerts", value=True)
        with col2:
            hackathon_updates = st.checkbox("Hackathon Updates", value=True)
            investment_reports = st.checkbox("Investment Reports", value=True)
        
        submitted = st.form_submit_button("💾 Save Changes", use_container_width=True)
        
        if submitted:
            # Update user profile (in a real app, this would update the database)
            st.session_state.current_user.full_name = new_full_name
            st.session_state.current_user.email = new_email
            st.session_state.current_user.username = new_username
            st.session_state.current_user.bio = new_bio
            st.session_state.current_user.github_username = new_github
            st.session_state.current_user.linkedin_url = new_linkedin
            st.session_state.current_user.skills = [skill.strip() for skill in new_skills.split(",") if skill.strip()]
            st.session_state.current_user.role = UserRole(new_role)
            
            st.success("✅ Profile updated successfully!")
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
    if st.button("💰 Investor Feed", use_container_width=True):
        st.switch_page("pages/4_Investor_Feed.py")
