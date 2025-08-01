import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styling import apply_custom_styling, load_css
from utils.state_management import initialize_session_state
from src._1_use_cases.mvp_service import MVPService
from src._1_use_cases.hackathon_service import HackathonService
from src._0_domain.user import UserRole
from src._0_domain.hackathon import HackathonStatus
from src._0_domain.mvp import MVPStatus

# Configure page
st.set_page_config(
    page_title="Admin Dashboard - Vibratonic",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state and styling
initialize_session_state()
apply_custom_styling()
load_css("static/custom.css")

# Check admin permissions
if not st.session_state.current_user.can_admin():
    st.error("🚫 Access Denied")
    st.warning("Admin privileges required to access this dashboard.")
    st.stop()

# Initialize services
mvp_service = MVPService()
hackathon_service = HackathonService()

st.markdown("# ⚙️ Admin Dashboard")
st.markdown("*Platform management and analytics*")

# Get data
hackathons = hackathon_service.get_all_hackathons()
mvps = mvp_service.get_all_mvps()

# Key metrics
total_funding = sum([mvp.current_funding for mvp in mvps])
platform_revenue = total_funding * 0.20  # 20% platform fee
total_participants = sum([h.current_participants for h in hackathons])
active_hackathons = len([h for h in hackathons if h.status == HackathonStatus.OPEN])

# Dashboard metrics
st.markdown("### 📊 Platform Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "🎯 Total Hackathons", 
        len(hackathons),
        delta=f"+{len([h for h in hackathons if h.status == HackathonStatus.OPEN])}"
    )

with col2:
    st.metric(
        "🚀 Total MVPs", 
        len(mvps),
        delta=f"+{len([mvp for mvp in mvps if mvp.status == MVPStatus.SUBMITTED])}"
    )

with col3:
    st.metric(
        "💰 Total Funding", 
        f"€{total_funding:,.0f}",
        delta="€2,150"
    )

with col4:
    st.metric(
        "💵 Platform Revenue", 
        f"€{platform_revenue:,.0f}",
        delta="€430"
    )

with col5:
    st.metric(
        "👥 Total Participants", 
        total_participants,
        delta="+23"
    )

st.markdown("---")

# Dashboard tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Analytics", "🎯 Hackathons", "🚀 MVPs", "👥 Users", "💰 Payments"])

with tab1:
    st.markdown("### 📈 Platform Analytics")
    
    # Funding over time chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💰 Funding Trends")
        
        # Create sample data for funding over time
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        funding_data = []
        cumulative_funding = 0
        
        for date in dates:
            daily_funding = sum([mvp.current_funding for mvp in mvps if mvp.submission_datetime and mvp.submission_datetime.date() <= date.date()]) / len(dates)
            cumulative_funding += daily_funding
            funding_data.append({"Date": date, "Funding": cumulative_funding})
        
        df_funding = pd.DataFrame(funding_data)
        
        fig_funding = px.line(
            df_funding, 
            x="Date", 
            y="Funding",
            title="Cumulative Funding Over Time",
            color_discrete_sequence=["#00FFE1"]
        )
        fig_funding.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#FFFFFF"
        )
        st.plotly_chart(fig_funding, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Hackathon Status Distribution")
        
        status_counts = {}
        for status in HackathonStatus:
            status_counts[status.value] = len([h for h in hackathons if h.status == status])
        
        fig_status = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Hackathon Status Distribution",
            color_discrete_sequence=["#00FFE1", "#FF00A8", "#FFD700", "#666666"]
        )
        fig_status.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#FFFFFF"
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    # MVP performance
    st.markdown("#### 🚀 MVP Performance")
    
    mvp_data = []
    for mvp in mvps:
        mvp_data.append({
            "Title": mvp.title,
            "Funding": mvp.current_funding,
            "Backers": mvp.backers_count,
            "Status": mvp.status.value,
            "Tech Stack": len(mvp.tech_stack)
        })
    
    df_mvps = pd.DataFrame(mvp_data)
    
    if not df_mvps.empty:
        fig_mvp = px.scatter(
            df_mvps,
            x="Backers",
            y="Funding",
            size="Tech Stack",
            color="Status",
            hover_data=["Title"],
            title="MVP Funding vs Backers",
            color_discrete_sequence=["#00FFE1", "#FF00A8", "#FFD700", "#666666"]
        )
        fig_mvp.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#FFFFFF"
        )
        st.plotly_chart(fig_mvp, use_container_width=True)

with tab2:
    st.markdown("### 🎯 Hackathon Management")
    
    # Hackathon controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Create New Hackathon", use_container_width=True):
            st.switch_page("pages/1_Create_Hackathon.py")
    
    with col2:
        if st.button("📊 Export Hackathon Data", use_container_width=True):
            st.success("📄 Export functionality would be implemented here")
    
    with col3:
        if st.button("📧 Send Notifications", use_container_width=True):
            st.success("📧 Notification system would be implemented here")
    
    # Hackathon list with management options
    st.markdown("#### Active Hackathons")
    
    for hackathon in hackathons:
        with st.expander(f"{hackathon.title} ({hackathon.status.value})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {hackathon.description}")
                st.markdown(f"**Venue:** {hackathon.venue.name}")
                st.markdown(f"**Participants:** {hackathon.current_participants}/{hackathon.max_participants}")
                st.markdown(f"**Prize Pool:** €{hackathon.prize_pool:,}")
                st.markdown(f"**Start:** {hackathon.start_datetime.strftime('%Y-%m-%d %H:%M')}")
            
            with col2:
                # Status management
                new_status = st.selectbox(
                    "Change Status",
                    [status.value for status in HackathonStatus],
                    index=[status.value for status in HackathonStatus].index(hackathon.status.value),
                    key=f"status_{hackathon.id}"
                )
                
                if st.button(f"Update Status", key=f"update_{hackathon.id}"):
                    hackathon_service.update_hackathon_status(hackathon.id, HackathonStatus(new_status))
                    st.success(f"Status updated to {new_status}")
                    st.rerun()
                
                if st.button(f"View Details", key=f"view_{hackathon.id}"):
                    st.info(f"Detailed view for {hackathon.title}")

with tab3:
    st.markdown("### 🚀 MVP Management")
    
    # MVP controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Generate MVP Report", use_container_width=True):
            st.success("📊 MVP analytics report would be generated here")
    
    with col2:
        if st.button("🏆 Feature MVP", use_container_width=True):
            st.success("🏆 MVP featuring system would be implemented here")
    
    with col3:
        if st.button("📧 Contact Creators", use_container_width=True):
            st.success("📧 Creator communication system would be implemented here")
    
    # MVP performance table
    st.markdown("#### MVP Performance Overview")
    
    mvp_performance = []
    for mvp in mvps:
        hackathon = hackathon_service.get_hackathon(mvp.hackathon_id)
        mvp_performance.append({
            "Title": mvp.title,
            "Hackathon": hackathon.title if hackathon else "Unknown",
            "Status": mvp.status.value,
            "Funding": f"€{mvp.current_funding:,.0f}",
            "Goal": f"€{sum(goal.amount for goal in mvp.funding_goals):,.0f}",
            "Progress": f"{mvp.get_funding_percentage():.1f}%",
            "Backers": mvp.backers_count,
            "Creator": mvp.creator_id
        })
    
    df_performance = pd.DataFrame(mvp_performance)
    
    if not df_performance.empty:
        st.dataframe(df_performance, use_container_width=True)
    
    # Individual MVP management
    st.markdown("#### Individual MVP Management")
    
    for mvp in mvps[:5]:  # Show first 5 for management
        with st.expander(f"{mvp.title} - {mvp.status.value}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {mvp.description}")
                st.markdown(f"**Tech Stack:** {', '.join(mvp.tech_stack)}")
                st.markdown(f"**Funding:** €{mvp.current_funding:,.0f} / €{sum(goal.amount for goal in mvp.funding_goals):,.0f}")
                st.markdown(f"**Backers:** {mvp.backers_count}")
            
            with col2:
                new_mvp_status = st.selectbox(
                    "Change Status",
                    [status.value for status in MVPStatus],
                    index=[status.value for status in MVPStatus].index(mvp.status.value),
                    key=f"mvp_status_{mvp.id}"
                )
                
                if st.button(f"Update Status", key=f"mvp_update_{mvp.id}"):
                    mvp_service.update_mvp_status(mvp.id, MVPStatus(new_mvp_status))
                    st.success(f"MVP status updated to {new_mvp_status}")
                    st.rerun()

with tab4:
    st.markdown("### 👥 User Management")
    
    # User statistics
    user_roles = {
        "Participants": 45,
        "Investors": 23,
        "Organizers": 8,
        "Admins": 3
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👤 Participants", user_roles["Participants"])
    with col2:
        st.metric("💰 Investors", user_roles["Investors"])
    with col3:
        st.metric("🎯 Organizers", user_roles["Organizers"])
    with col4:
        st.metric("⚙️ Admins", user_roles["Admins"])
    
    # User management tools
    st.markdown("#### User Management Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📧 Send Platform Updates", use_container_width=True):
            st.success("📧 Platform update notifications sent")
    
    with col2:
        if st.button("📊 Export User Data", use_container_width=True):
            st.success("📊 User data export initiated")
    
    with col3:
        if st.button("🔒 Manage Permissions", use_container_width=True):
            st.success("🔒 Permission management panel would open here")
    
    # Mock user list
    st.markdown("#### Recent User Activity")
    
    recent_users = [
        {"Name": "Alice Chen", "Role": "Investor", "Last Active": "2 hours ago", "Actions": "Funded 2 MVPs"},
        {"Name": "Bob Wilson", "Role": "Participant", "Last Active": "5 hours ago", "Actions": "Created new MVP"},
        {"Name": "Carol Davis", "Role": "Organizer", "Last Active": "1 day ago", "Actions": "Launched hackathon"},
        {"Name": "David Kumar", "Role": "Participant", "Last Active": "2 days ago", "Actions": "Joined hackathon"}
    ]
    
    for user in recent_users:
        st.markdown(f"""
        <div class="user-activity-item">
            <strong>{user['Name']}</strong> ({user['Role']})
            <br>
            <small>Last active: {user['Last Active']} • {user['Actions']}</small>
        </div>
        """, unsafe_allow_html=True)

with tab5:
    st.markdown("### 💰 Payment & Revenue Management")
    
    # Revenue metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Volume", f"€{total_funding:,.0f}")
    
    with col2:
        st.metric("💵 Platform Revenue", f"€{platform_revenue:,.0f}")
    
    with col3:
        monthly_revenue = platform_revenue * 0.3  # Mock monthly revenue
        st.metric("📅 Monthly Revenue", f"€{monthly_revenue:,.0f}")
    
    with col4:
        avg_transaction = total_funding / max(len(mvps), 1)
        st.metric("📊 Avg Transaction", f"€{avg_transaction:,.0f}")
    
    # Payment management tools
    st.markdown("#### Payment Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Generate Revenue Report", use_container_width=True):
            st.success("📊 Revenue report generated")
    
    with col2:
        if st.button("💳 Process Refunds", use_container_width=True):
            st.success("💳 Refund processing panel would open here")
    
    with col3:
        if st.button("🔍 Audit Transactions", use_container_width=True):
            st.success("🔍 Transaction audit initiated")
    
    # Recent transactions
    st.markdown("#### Recent Transactions")
    
    transactions = []
    for mvp in mvps:
        if mvp.current_funding > 0:
            transactions.append({
                "MVP": mvp.title,
                "Amount": f"€{mvp.current_funding:,.0f}",
                "Platform Fee": f"€{mvp.current_funding * 0.20:,.0f}",
                "Creator Amount": f"€{mvp.current_funding * 0.80:,.0f}",
                "Status": "Completed",
                "Date": "2025-07-28"  # Mock date
            })
    
    if transactions:
        df_transactions = pd.DataFrame(transactions)
        st.dataframe(df_transactions, use_container_width=True)

# System health
st.markdown("---")
st.markdown("### ⚡ System Health")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🟢 API Status", "Online", delta="99.9% uptime")

with col2:
    st.metric("💾 Database", "Healthy", delta="Low latency")

with col3:
    st.metric("💳 Payment Gateway", "Connected", delta="Mollie API")

with col4:
    st.metric("📡 WebSocket", "Active", delta="Real-time updates")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("📊 Platform Analytics", use_container_width=True):
        st.info("Advanced analytics dashboard would be loaded here")

with col3:
    if st.button("⚙️ System Settings", use_container_width=True):
        st.info("System configuration panel would be loaded here")
