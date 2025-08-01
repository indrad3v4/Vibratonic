import streamlit as st
import folium
from streamlit_folium import st_folium
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styling import apply_custom_styling, load_css
from utils.state_management import initialize_session_state
from src._1_use_cases.hackathon_service import HackathonService

# Configure page
st.set_page_config(
    page_title="Map View - Vibratonic",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state and styling
initialize_session_state()
apply_custom_styling()
load_css("static/custom.css")

# Initialize services
hackathon_service = HackathonService()

st.markdown("# 🗺️ Hackathon Map")

# Get all hackathons
hackathons = hackathon_service.get_all_hackathons()

# Filter controls
col1, col2, col3 = st.columns(3)

with col1:
    status_filter = st.selectbox("Status", ["All", "Open", "In Progress", "Completed"])

with col2:
    theme_filter = st.selectbox("Theme", ["All"] + list(set([h.theme for h in hackathons if h.theme])))

with col3:
    city_filter = st.selectbox("City", ["All"] + list(set([h.venue.address.split(',')[-1].strip() for h in hackathons])))

# Apply filters
filtered_hackathons = hackathons

if status_filter != "All":
    filtered_hackathons = [h for h in filtered_hackathons if h.status.value == status_filter.lower().replace(" ", "_")]

if theme_filter != "All":
    filtered_hackathons = [h for h in filtered_hackathons if h.theme == theme_filter]

if city_filter != "All":
    filtered_hackathons = [h for h in filtered_hackathons if city_filter in h.venue.address]

# Create map
if filtered_hackathons:
    # Calculate center point
    center_lat = sum([h.venue.latitude for h in filtered_hackathons]) / len(filtered_hackathons)
    center_lng = sum([h.venue.longitude for h in filtered_hackathons]) / len(filtered_hackathons)
else:
    center_lat, center_lng = 52.2297, 21.0122  # Default to Warsaw

m = folium.Map(location=[center_lat, center_lng], zoom_start=6)

# Add markers for each hackathon
for hackathon in filtered_hackathons:
    # Color coding based on status
    if hackathon.status.value == "open":
        color = "#00FFE1"
        icon_color = "lightblue"
    elif hackathon.status.value == "in_progress":
        color = "#FFD700"
        icon_color = "orange"
    elif hackathon.status.value == "completed":
        color = "#FF00A8"
        icon_color = "pink"
    else:
        color = "#666666"
        icon_color = "gray"
    
    # Create popup content
    popup_html = f"""
    <div style="width: 300px; font-family: Arial, sans-serif;">
        <h4 style="color: {color}; margin: 0 0 10px 0;">{hackathon.title}</h4>
        <p style="margin: 5px 0;"><strong>Theme:</strong> {hackathon.theme}</p>
        <p style="margin: 5px 0;"><strong>Venue:</strong> {hackathon.venue.name}</p>
        <p style="margin: 5px 0;"><strong>Date:</strong> {hackathon.start_datetime.strftime('%B %d, %Y')}</p>
        <p style="margin: 5px 0;"><strong>Participants:</strong> {hackathon.current_participants}/{hackathon.max_participants}</p>
        <p style="margin: 5px 0;"><strong>Prize Pool:</strong> €{hackathon.prize_pool:,}</p>
        <p style="margin: 5px 0;"><strong>Status:</strong> <span style="color: {color}; text-transform: uppercase;">{hackathon.status.value}</span></p>
        <div style="margin-top: 10px;">
            <progress value="{hackathon.get_progress_percentage()}" max="100" style="width: 100%; height: 20px;"></progress>
            <small>{hackathon.get_progress_percentage():.1f}% full</small>
        </div>
    </div>
    """
    
    folium.Marker(
        [hackathon.venue.latitude, hackathon.venue.longitude],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{hackathon.title} ({hackathon.status.value})",
        icon=folium.Icon(color=icon_color, icon="calendar", prefix="fa")
    ).add_to(m)

# Display map
map_data = st_folium(m, width=700, height=500)

# Display hackathon list below map
st.markdown("---")
st.markdown("## 📋 Hackathon List")

# Show stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Hackathons", len(filtered_hackathons))

with col2:
    open_count = len([h for h in filtered_hackathons if h.status.value == "open"])
    st.metric("Open for Registration", open_count)

with col3:
    total_participants = sum([h.current_participants for h in filtered_hackathons])
    st.metric("Total Participants", total_participants)

with col4:
    total_prizes = sum([h.prize_pool for h in filtered_hackathons])
    st.metric("Total Prize Pool", f"€{total_prizes:,}")

# Hackathon cards
for hackathon in filtered_hackathons:
    with st.container():
        # Status color
        if hackathon.status.value == "open":
            status_color = "#00FFE1"
        elif hackathon.status.value == "in_progress":
            status_color = "#FFD700"
        elif hackathon.status.value == "completed":
            status_color = "#FF00A8"
        else:
            status_color = "#666666"
        
        progress = hackathon.get_progress_percentage()
        
        st.markdown(f"""
        <div class="hack-card" style="border-left: 4px solid {status_color};">
            <div class="hack-header">
                <h4 class="hack-title">{hackathon.title}</h4>
                <span class="hack-status" style="color: {status_color};">
                    {hackathon.status.value.upper()}
                </span>
            </div>
            <p class="hack-description">{hackathon.description[:150]}...</p>
            
            <div class="hack-details">
                <div class="detail-row">
                    <span>📍 <strong>Venue:</strong> {hackathon.venue.name}</span>
                </div>
                <div class="detail-row">
                    <span>📅 <strong>Date:</strong> {hackathon.start_datetime.strftime('%B %d, %Y at %I:%M %p')}</span>
                </div>
                <div class="detail-row">
                    <span>👥 <strong>Participants:</strong> {hackathon.current_participants}/{hackathon.max_participants}</span>
                </div>
                <div class="detail-row">
                    <span>💰 <strong>Prize Pool:</strong> €{hackathon.prize_pool:,}</span>
                </div>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%; background: {status_color};"></div>
            </div>
            
            <div class="hack-tags">
                {' '.join([f'<span class="tag">#{tag}</span>' for tag in hackathon.tags[:3]])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if hackathon.can_join():
                if st.button(f"Join {hackathon.title}", key=f"join_{hackathon.id}", use_container_width=True):
                    if hackathon_service.join_hackathon(hackathon.id, st.session_state.current_user):
                        st.success(f"Successfully joined {hackathon.title}!")
                        st.rerun()
                    else:
                        st.error("Failed to join hackathon")
            else:
                st.button("Full/Closed", disabled=True, use_container_width=True)
        
        with col2:
            if st.button(f"View Details", key=f"details_{hackathon.id}", use_container_width=True):
                st.session_state.selected_hackathon = hackathon.id
                st.info(f"Viewing details for {hackathon.title}")
        
        with col3:
            if st.button(f"View MVPs", key=f"mvps_{hackathon.id}", use_container_width=True):
                st.session_state.hackathon_filter = hackathon.id
                st.switch_page("pages/3_MVP_Showcase.py")

# Legend
st.markdown("---")
st.markdown("### 🗺️ Map Legend")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("🔵 **Open** - Registration available")

with col2:
    st.markdown("🟠 **In Progress** - Event ongoing")

with col3:
    st.markdown("🔴 **Completed** - Event finished")

with col4:
    st.markdown("⚫ **Draft/Cancelled** - Not active")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("🎯 Create Hackathon", use_container_width=True):
        st.switch_page("pages/1_Create_Hackathon.py")

with col3:
    if st.button("🚀 Browse MVPs", use_container_width=True):
        st.switch_page("pages/3_MVP_Showcase.py")
