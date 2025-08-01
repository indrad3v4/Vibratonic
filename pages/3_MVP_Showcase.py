import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styling import apply_custom_styling, load_css
from utils.state_management import initialize_session_state
from src._1_use_cases.mvp_service import MVPService
from src._1_use_cases.hackathon_service import HackathonService
from src._1_use_cases.payment_service import PaymentService

# Configure page
st.set_page_config(
    page_title="MVP Showcase - Vibratonic",
    page_icon="🚀",
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
payment_service = PaymentService()

st.markdown("# 🚀 MVP Showcase")

# Filter controls
col1, col2, col3, col4 = st.columns(4)

with col1:
    status_filter = st.selectbox("Status", ["All", "Draft", "Submitted", "Funded", "Completed"])

with col2:
    hackathons = hackathon_service.get_all_hackathons()
    hackathon_options = ["All"] + [h.title for h in hackathons]
    hackathon_filter = st.selectbox("Hackathon", hackathon_options)

with col3:
    sort_options = ["Recent", "Funding Amount", "Backers Count", "Title"]
    sort_by = st.selectbox("Sort by", sort_options)

with col4:
    tech_stack_options = ["All", "Python", "JavaScript", "React", "Node.js", "AI/ML", "Blockchain", "IoT"]
    tech_filter = st.selectbox("Tech Stack", tech_stack_options)

# Get MVPs
mvps = mvp_service.get_all_mvps()

# Apply filters
if status_filter != "All":
    mvps = [mvp for mvp in mvps if mvp.status.value == status_filter.lower()]

if hackathon_filter != "All":
    selected_hackathon = next((h for h in hackathons if h.title == hackathon_filter), None)
    if selected_hackathon:
        mvps = [mvp for mvp in mvps if mvp.hackathon_id == selected_hackathon.id]

if tech_filter != "All":
    mvps = [mvp for mvp in mvps if tech_filter in mvp.tech_stack]

# Sort MVPs
if sort_by == "Funding Amount":
    mvps.sort(key=lambda x: x.current_funding, reverse=True)
elif sort_by == "Backers Count":
    mvps.sort(key=lambda x: x.backers_count, reverse=True)
elif sort_by == "Title":
    mvps.sort(key=lambda x: x.title)
elif sort_by == "Recent":
    mvps.sort(key=lambda x: x.submission_datetime or x.id, reverse=True)

# Stats
st.markdown("### 📊 Showcase Stats")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total MVPs", len(mvps))

with col2:
    funded_mvps = [mvp for mvp in mvps if mvp.status.value == "funded"]
    st.metric("Funded Projects", len(funded_mvps))

with col3:
    total_funding = sum([mvp.current_funding for mvp in mvps])
    st.metric("Total Funding", f"€{total_funding:,.0f}")

with col4:
    total_backers = sum([mvp.backers_count for mvp in mvps])
    st.metric("Total Backers", total_backers)

st.markdown("---")

# Display MVPs
if not mvps:
    st.info("No MVPs found matching your filters.")
else:
    for mvp in mvps:
        with st.container():
            # Get hackathon info
            hackathon = hackathon_service.get_hackathon(mvp.hackathon_id)
            hackathon_title = hackathon.title if hackathon else "Unknown Hackathon"
            
            funding_percentage = mvp.get_funding_percentage()
            total_goal = sum(goal.amount for goal in mvp.funding_goals)
            
            # Status color
            if mvp.status.value == "funded":
                status_color = "#00FFE1"
            elif mvp.status.value == "submitted":
                status_color = "#FFD700"
            else:
                status_color = "#FF00A8"
            
            st.markdown(f"""
            <div class="mvp-card">
                <div class="mvp-header">
                    <h3 class="mvp-title">{mvp.title}</h3>
                    <span class="mvp-status" style="color: {status_color};">
                        {mvp.status.value.upper()}
                    </span>
                </div>
                
                <div class="mvp-meta">
                    <span class="mvp-hackathon">🏆 {hackathon_title}</span>
                    <span class="mvp-creator">👤 {mvp.creator_id}</span>
                </div>
                
                <p class="mvp-description">{mvp.description}</p>
                
                <div class="mvp-tech-stack">
                    <strong>Tech Stack:</strong>
                    {' '.join([f'<span class="tech-tag">{tech}</span>' for tech in mvp.tech_stack[:6]])}
                </div>
                
                <div class="mvp-links">
                    {f'<a href="{mvp.github_url}" target="_blank" class="mvp-link">🔗 GitHub</a>' if mvp.github_url else ''}
                    {f'<a href="{mvp.demo_url}" target="_blank" class="mvp-link">🌐 Demo</a>' if mvp.demo_url else ''}
                </div>
                
                <div class="mvp-funding">
                    <div class="funding-header">
                        <h4>💰 Funding Progress</h4>
                        <span class="funding-percentage">{funding_percentage:.1f}%</span>
                    </div>
                    
                    <div class="funding-bar">
                        <div class="funding-fill" style="width: {funding_percentage}%; background: linear-gradient(90deg, {status_color}, #FFD700);"></div>
                    </div>
                    
                    <div class="funding-details">
                        <span class="funding-amount">€{mvp.current_funding:,.0f} raised</span>
                        <span class="funding-goal">Goal: €{total_goal:,.0f}</span>
                        <span class="funding-backers">{mvp.backers_count} backers</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Funding goals
            if mvp.funding_goals:
                st.markdown("**Funding Tiers:**")
                cols = st.columns(len(mvp.funding_goals))
                
                for i, goal in enumerate(mvp.funding_goals):
                    with cols[i % len(cols)]:
                        tier_color = "#00FFE1" if goal.tier.value == "basic" else "#FF00A8" if goal.tier.value == "premium" else "#FFD700"
                        
                        st.markdown(f"""
                        <div class="funding-tier" style="border-color: {tier_color};">
                            <h5 style="color: {tier_color}; margin: 0;">{goal.tier.value.title()}</h5>
                            <div class="tier-amount">€{goal.amount:,.0f}</div>
                            <p class="tier-description">{goal.description}</p>
                            <div class="tier-rewards">
                                {'<br>'.join([f'✓ {reward}' for reward in goal.rewards[:3]])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button(f"💰 Fund Project", key=f"fund_{mvp.id}", use_container_width=True):
                    st.session_state.funding_modal_mvp = mvp.id
                    st.rerun()
            
            with col2:
                if st.button(f"📊 View Details", key=f"details_{mvp.id}", use_container_width=True):
                    st.session_state.mvp_details = mvp.id
            
            with col3:
                if mvp.demo_url:
                    st.link_button("🌐 Live Demo", mvp.demo_url, use_container_width=True)
                else:
                    st.button("🌐 No Demo", disabled=True, use_container_width=True)
            
            with col4:
                if mvp.github_url:
                    st.link_button("🔗 GitHub", mvp.github_url, use_container_width=True)
                else:
                    st.button("🔗 No Repo", disabled=True, use_container_width=True)
            
            st.markdown("---")

# Funding Modal
if "funding_modal_mvp" in st.session_state:
    mvp_id = st.session_state.funding_modal_mvp
    mvp = mvp_service.get_mvp(mvp_id)
    
    if mvp:
        st.markdown("---")
        st.markdown(f"## 💰 Fund {mvp.title}")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Project Details")
            st.markdown(f"**Title:** {mvp.title}")
            st.markdown(f"**Creator:** {mvp.creator_id}")
            st.markdown(f"**Current Funding:** €{mvp.current_funding:,.0f}")
            st.markdown(f"**Backers:** {mvp.backers_count}")
            
            if mvp.funding_goals:
                st.markdown("**Available Tiers:**")
                for goal in mvp.funding_goals:
                    st.markdown(f"- **{goal.tier.value.title()}**: €{goal.amount:,.0f} - {goal.description}")
        
        with col2:
            st.markdown("### 💳 Make Payment")
            
            # Funding amount
            funding_amount = st.number_input("Funding Amount (€)", min_value=10, max_value=50000, value=100)
            
            # Payment method
            payment_methods = ["Credit Card", "iDEAL", "PayPal", "Bank Transfer"]
            payment_method = st.selectbox("Payment Method", payment_methods)
            
            # Calculate fees
            fees = payment_service.calculate_fees(funding_amount)
            
            st.markdown("**Payment Breakdown:**")
            st.markdown(f"- **Amount:** €{fees['amount']:.2f}")
            st.markdown(f"- **Platform Fee ({fees['fee_percentage']:.0f}%):** €{fees['platform_fee']:.2f}")
            st.markdown(f"- **To Creator:** €{fees['creator_amount']:.2f}")
            
            # Terms
            agree_terms = st.checkbox("I agree to the terms and conditions")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("❌ Cancel", use_container_width=True):
                    del st.session_state.funding_modal_mvp
                    st.rerun()
            
            with col2:
                if st.button("💳 Process Payment", disabled=not agree_terms, use_container_width=True):
                    # Create payment
                    try:
                        payment = payment_service.create_payment(
                            amount=funding_amount,
                            description=f"Funding for {mvp.title}",
                            mvp_id=mvp.id,
                            backer_id=st.session_state.current_user.id
                        )
                        
                        st.success("🎉 Payment created successfully!")
                        st.markdown(f"**Payment ID:** `{payment['payment_id']}`")
                        st.markdown(f"**Status:** {payment['status']}")
                        
                        # Simulate successful payment for demo
                        if mvp_service.add_funding(mvp.id, funding_amount, st.session_state.current_user.id):
                            st.success(f"✅ Successfully funded {mvp.title} with €{funding_amount}!")
                            st.balloons()
                        
                        # In production, redirect to Mollie checkout
                        st.markdown(f"🔗 [Complete Payment]({payment['checkout_url']})")
                        
                        del st.session_state.funding_modal_mvp
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Payment failed: {str(e)}")

# MVP Details Modal
if "mvp_details" in st.session_state:
    mvp_id = st.session_state.mvp_details
    mvp = mvp_service.get_mvp(mvp_id)
    
    if mvp:
        st.markdown("---")
        st.markdown(f"## 📊 {mvp.title} - Detailed View")
        
        # Close button
        if st.button("❌ Close Details"):
            del st.session_state.mvp_details
            st.rerun()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📝 Description")
            st.markdown(mvp.description)
            
            st.markdown("### 🛠️ Technology Stack")
            st.markdown(' '.join([f'`{tech}`' for tech in mvp.tech_stack]))
            
            if mvp.media_files:
                st.markdown("### 🎬 Media")
                for media in mvp.media_files:
                    if media.type == "image":
                        st.image(media.url, caption=media.title, width=400)
                    elif media.type == "video":
                        st.video(media.url)
            
        with col2:
            st.markdown("### 💰 Funding Information")
            
            funding_percentage = mvp.get_funding_percentage()
            total_goal = sum(goal.amount for goal in mvp.funding_goals)
            
            st.metric("Current Funding", f"€{mvp.current_funding:,.0f}")
            st.metric("Funding Goal", f"€{total_goal:,.0f}")
            st.metric("Progress", f"{funding_percentage:.1f}%")
            st.metric("Backers", mvp.backers_count)
            
            # Progress bar
            st.progress(funding_percentage / 100)
            
            st.markdown("### 📈 Funding Goals")
            for goal in mvp.funding_goals:
                with st.expander(f"{goal.tier.value.title()} - €{goal.amount:,.0f}"):
                    st.markdown(goal.description)
                    st.markdown("**Rewards:**")
                    for reward in goal.rewards:
                        st.markdown(f"- {reward}")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("🗺️ Map View", use_container_width=True):
        st.switch_page("pages/2_Map_View.py")

with col3:
    if st.button("💰 Investor Feed", use_container_width=True):
        st.switch_page("pages/4_Investor_Feed.py")
