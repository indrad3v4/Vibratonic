import streamlit as st
from typing import Dict, Any
from src._0_domain.user import UserProfile, UserRole, UserStatus
from src._1_use_cases.hackathon_service import HackathonService
from src._1_use_cases.mvp_service import MVPService
from src._1_use_cases.payment_service import PaymentService

class VibratonicApp:
    def __init__(self):
        self.hackathon_service = HackathonService()
        self.mvp_service = MVPService()
        self.payment_service = PaymentService()
        self._initialize_user()
    
    def _initialize_user(self):
        """Initialize current user session"""
        if "current_user" not in st.session_state:
            # Create a demo user for the session
            st.session_state.current_user = UserProfile(
                id="user001",
                username="demo_creator",
                email="creator@vibratonic.app",
                full_name="Demo Creator",
                role=UserRole.PARTICIPANT,
                status=UserStatus.ACTIVE,
                bio="Passionate hackathon creator and tech innovator",
                skills=["Python", "React", "AI/ML", "Blockchain"],
                github_username="demo_creator",
                linkedin_url="https://linkedin.com/in/democreator"
            )
    
    def run(self):
        """Main application entry point"""
        self._render_header()
        self._render_navigation()
        self._render_main_content()
        self._render_footer()
    
    def _render_header(self):
        """Render the main header"""
        st.markdown("""
        <div class="header-container">
            <div class="logo-section">
                <h1 class="app-title">⚡ VIBRATONIC</h1>
                <p class="app-tagline">Hack → Demo → Fund</p>
            </div>
            <div class="user-section">
                <span class="user-greeting">Welcome, {}</span>
                <div class="user-role">{}</div>
            </div>
        </div>
        """.format(
            st.session_state.current_user.full_name,
            st.session_state.current_user.role.value.title()
        ), unsafe_allow_html=True)
    
    def _render_navigation(self):
        """Render navigation menu"""
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.current_page = "home"
        
        with col2:
            if st.button("🗺️ Map", use_container_width=True):
                st.session_state.current_page = "map"
        
        with col3:
            if st.button("🚀 MVPs", use_container_width=True):
                st.session_state.current_page = "mvps"
        
        with col4:
            if st.button("💰 Invest", use_container_width=True):
                st.session_state.current_page = "invest"
        
        with col5:
            if st.button("👤 Profile", use_container_width=True):
                st.session_state.current_page = "profile"
        
        with col6:
            if st.session_state.current_user.can_admin():
                if st.button("⚙️ Admin", use_container_width=True):
                    st.session_state.current_page = "admin"
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_main_content(self):
        """Render main content based on current page"""
        current_page = st.session_state.get("current_page", "home")
        
        if current_page == "home":
            self._render_home_page()
        elif current_page == "map":
            self._render_map_page()
        elif current_page == "mvps":
            self._render_mvp_page()
        elif current_page == "invest":
            self._render_investor_page()
        elif current_page == "profile":
            self._render_profile_page()
        elif current_page == "admin":
            self._render_admin_page()
        else:
            self._render_home_page()
    
    def _render_home_page(self):
        """Render the home page"""
        st.markdown('<div class="page-container">', unsafe_allow_html=True)
        
        # Hero section
        st.markdown("""
        <div class="hero-section">
            <h2 class="hero-title">Turn Your Ideas Into Funded Reality</h2>
            <p class="hero-description">
                Create hackathons, showcase MVPs, and secure funding all in one platform.
                Join the vibrant ecosystem of creators and investors.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick actions
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="action-card">', unsafe_allow_html=True)
            st.markdown("### 🎯 Create Hackathon")
            st.markdown("Launch your own hackathon event and bring creators together")
            if st.button("Start Creating", key="create_hack", use_container_width=True):
                st.session_state.current_page = "create_hackathon"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="action-card">', unsafe_allow_html=True)
            st.markdown("### 💡 Browse MVPs")
            st.markdown("Discover innovative projects and fund the next big idea")
            if st.button("Explore MVPs", key="browse_mvps", use_container_width=True):
                st.session_state.current_page = "mvps"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Featured hackathons
        st.markdown("## 🔥 Featured Hackathons")
        hackathons = self.hackathon_service.get_open_hackathons()[:3]
        
        for hackathon in hackathons:
            self._render_hackathon_card(hackathon)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_hackathon_card(self, hackathon):
        """Render a hackathon card"""
        progress = hackathon.get_progress_percentage()
        status_color = "#00FFE1" if hackathon.status.value == "open" else "#FF00A8"
        
        st.markdown(f"""
        <div class="hack-card">
            <div class="hack-header">
                <h4 class="hack-title">{hackathon.title}</h4>
                <span class="hack-status" style="color: {status_color}">
                    {hackathon.status.value.upper()}
                </span>
            </div>
            <p class="hack-description">{hackathon.description[:120]}...</p>
            <div class="hack-details">
                <div class="hack-venue">📍 {hackathon.venue.name}</div>
                <div class="hack-date">📅 {hackathon.start_datetime.strftime('%B %d, %Y')}</div>
                <div class="hack-participants">👥 {hackathon.current_participants}/{hackathon.max_participants}</div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%"></div>
            </div>
            <div class="hack-tags">
                {' '.join([f'<span class="tag">#{tag}</span>' for tag in hackathon.tags[:3]])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_map_page(self):
        """Render map view (placeholder for now)"""
        st.markdown("## 🗺️ Hackathon Map View")
        st.info("Interactive map with hackathon locations will be implemented here using Folium.")
        
        # Show list of venues for now
        hackathons = self.hackathon_service.get_all_hackathons()
        for hackathon in hackathons:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{hackathon.venue.name}** - {hackathon.title}")
            with col2:
                st.write(f"{hackathon.current_participants}/{hackathon.max_participants}")
            with col3:
                status_emoji = "🟢" if hackathon.status.value == "open" else "🔴"
                st.write(f"{status_emoji} {hackathon.status.value}")
    
    def _render_mvp_page(self):
        """Render MVP showcase page"""
        st.markdown("## 🚀 MVP Showcase")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Status", ["All", "Submitted", "Funded", "Completed"])
        with col2:
            hackathon_filter = st.selectbox("Hackathon", ["All"] + [h.title for h in self.hackathon_service.get_all_hackathons()])
        with col3:
            sort_by = st.selectbox("Sort by", ["Funding", "Recent", "Backers"])
        
        # Get MVPs
        mvps = self.mvp_service.get_all_mvps()
        
        # Apply filters
        if status_filter != "All":
            mvps = [mvp for mvp in mvps if mvp.status.value == status_filter.lower()]
        
        # Display MVPs
        for mvp in mvps:
            self._render_mvp_card(mvp)
    
    def _render_mvp_card(self, mvp):
        """Render an MVP card"""
        funding_percentage = mvp.get_funding_percentage()
        total_goal = sum(goal.amount for goal in mvp.funding_goals)
        
        st.markdown(f"""
        <div class="mvp-card">
            <div class="mvp-header">
                <h4 class="mvp-title">{mvp.title}</h4>
                <span class="mvp-status">{mvp.status.value.upper()}</span>
            </div>
            <p class="mvp-description">{mvp.description}</p>
            <div class="mvp-tech-stack">
                {' '.join([f'<span class="tech-tag">{tech}</span>' for tech in mvp.tech_stack[:5]])}
            </div>
            <div class="mvp-funding">
                <div class="funding-progress">
                    <div class="funding-bar">
                        <div class="funding-fill" style="width: {funding_percentage}%"></div>
                    </div>
                    <div class="funding-text">
                        €{mvp.current_funding:,.0f} / €{total_goal:,.0f} ({funding_percentage:.1f}%)
                    </div>
                </div>
                <div class="funding-backers">{mvp.backers_count} backers</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Fund button
        if st.button(f"💰 Fund {mvp.title}", key=f"fund_{mvp.id}"):
            self._show_funding_modal(mvp)
    
    def _show_funding_modal(self, mvp):
        """Show funding modal for an MVP"""
        st.markdown("### 💰 Fund This MVP")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Project:** {mvp.title}")
            st.markdown(f"**Creator:** {mvp.creator_id}")
            
            # Funding tiers
            st.markdown("**Available Tiers:**")
            for tier in mvp.funding_goals:
                st.markdown(f"- **{tier.tier.value.title()}**: €{tier.amount:,.0f} - {tier.description}")
        
        with col2:
            # Funding form
            funding_amount = st.number_input("Funding Amount (€)", min_value=10, max_value=10000, value=100)
            
            # Calculate fees
            fees = self.payment_service.calculate_fees(funding_amount)
            
            st.markdown("**Payment Breakdown:**")
            st.markdown(f"- Amount: €{fees['amount']:.2f}")
            st.markdown(f"- Platform Fee ({fees['fee_percentage']:.0f}%): €{fees['platform_fee']:.2f}")
            st.markdown(f"- To Creator: €{fees['creator_amount']:.2f}")
            
            if st.button("💳 Proceed to Payment", use_container_width=True):
                # Create payment
                payment = self.payment_service.create_payment(
                    amount=funding_amount,
                    description=f"Funding for {mvp.title}",
                    mvp_id=mvp.id,
                    backer_id=st.session_state.current_user.id
                )
                
                st.success("Payment created successfully!")
                st.markdown(f"**Payment ID:** {payment['payment_id']}")
                st.markdown(f"**Checkout URL:** [Pay Now]({payment['checkout_url']})")
    
    def _render_investor_page(self):
        """Render investor feed page"""
        st.markdown("## 💰 Investor Feed")
        
        # Live activity feed
        st.markdown("### 📈 Live Activity")
        
        # Mock real-time activity
        activities = [
            {"type": "funding", "text": "🎉 EcoTrack AI received €500 from GreenTech Ventures", "time": "2 min ago"},
            {"type": "milestone", "text": "🎯 CryptoLend reached 75% funding goal", "time": "5 min ago"},
            {"type": "new_mvp", "text": "🚀 New MVP submitted: HealthSync IoT Platform", "time": "8 min ago"},
            {"type": "investor", "text": "👥 Alice Chen joined AI for Climate Change hackathon", "time": "12 min ago"}
        ]
        
        for activity in activities:
            icon = "💰" if activity["type"] == "funding" else "📊"
            st.markdown(f"""
            <div class="activity-item">
                <span class="activity-icon">{icon}</span>
                <span class="activity-text">{activity['text']}</span>
                <span class="activity-time">{activity['time']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Top MVPs
        st.markdown("### 🏆 Top Funded MVPs")
        funded_mvps = self.mvp_service.get_funded_mvps()
        
        for mvp in funded_mvps[:3]:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{mvp.title}**")
            with col2:
                st.write(f"€{mvp.current_funding:,.0f}")
            with col3:
                st.write(f"{mvp.backers_count} backers")
    
    def _render_profile_page(self):
        """Render user profile page"""
        user = st.session_state.current_user
        
        st.markdown("## 👤 Profile")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div class="profile-avatar">
                <div class="avatar-circle">
                    {user.full_name[0].upper()}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"### {user.full_name}")
            st.markdown(f"**@{user.username}** • {user.role.value.title()}")
            st.markdown(f"**Email:** {user.email}")
            if user.bio:
                st.markdown(f"**Bio:** {user.bio}")
        
        # Stats
        st.markdown("### 📊 Stats")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Hackathons Created", user.created_hackathons)
        with col2:
            st.metric("Hackathons Joined", user.joined_hackathons)
        with col3:
            st.metric("MVPs Created", user.created_mvps)
        with col4:
            st.metric("Total Investments", f"€{user.total_investments:,.0f}")
        
        # Skills
        if user.skills:
            st.markdown("### 🛠️ Skills")
            st.markdown(' '.join([f'<span class="skill-tag">{skill}</span>' for skill in user.skills]), unsafe_allow_html=True)
    
    def _render_admin_page(self):
        """Render admin dashboard"""
        if not st.session_state.current_user.can_admin():
            st.error("Access denied. Admin privileges required.")
            return
        
        st.markdown("## ⚙️ Admin Dashboard")
        
        # Key metrics
        st.markdown("### 📊 Platform Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        hackathons = self.hackathon_service.get_all_hackathons()
        mvps = self.mvp_service.get_all_mvps()
        total_funding = sum(mvp.current_funding for mvp in mvps)
        total_fees = total_funding * 0.20
        
        with col1:
            st.metric("Total Hackathons", len(hackathons))
        with col2:
            st.metric("Total MVPs", len(mvps))
        with col3:
            st.metric("Total Funding", f"€{total_funding:,.0f}")
        with col4:
            st.metric("Platform Revenue", f"€{total_fees:,.0f}")
        
        # Recent activity
        st.markdown("### 📈 Recent Activity")
        
        st.markdown("**Recent Hackathons:**")
        for hackathon in hackathons[-3:]:
            st.markdown(f"- {hackathon.title} ({hackathon.status.value}) - {hackathon.current_participants} participants")
        
        st.markdown("**Recent MVPs:**")
        for mvp in mvps[-3:]:
            st.markdown(f"- {mvp.title} - €{mvp.current_funding:,.0f} funded ({mvp.backers_count} backers)")
    
    def _render_footer(self):
        """Render footer"""
        st.markdown("""
        <div class="footer">
            <p>⚡ VIBRATONIC - Powering the future of hackathons • Made with ❤️ for creators and investors</p>
        </div>
        """, unsafe_allow_html=True)
