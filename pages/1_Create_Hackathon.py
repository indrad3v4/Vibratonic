import streamlit as st
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styling import apply_custom_styling, load_css
from utils.state_management import initialize_session_state
from src._1_use_cases.hackathon_service import HackathonService
from src._0_domain.hackathon import Venue

# Configure page
st.set_page_config(
    page_title="Create Hackathon - Vibratonic",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state and styling
initialize_session_state()
apply_custom_styling()
load_css("static/custom.css")

# Initialize services
hackathon_service = HackathonService()

st.markdown("# 🎯 Create Hackathon")

# Wizard steps
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1

# Progress indicator
progress = st.session_state.wizard_step / 5
st.progress(progress)

col1, col2, col3, col4, col5 = st.columns(5)
steps = ["Basic Info", "Venue", "Schedule", "Requirements", "Review"]

for i, (col, step) in enumerate(zip([col1, col2, col3, col4, col5], steps), 1):
    with col:
        if i == st.session_state.wizard_step:
            st.markdown(f"**{i}. {step}** ✨")
        elif i < st.session_state.wizard_step:
            st.markdown(f"~~{i}. {step}~~ ✅")
        else:
            st.markdown(f"{i}. {step}")

st.markdown("---")

# Step 1: Basic Information
if st.session_state.wizard_step == 1:
    st.markdown("## 📝 Basic Information")
    
    with st.form("basic_info_form"):
        title = st.text_input("Hackathon Title", placeholder="AI for Climate Change")
        description = st.text_area("Description", placeholder="Build AI solutions to combat climate change and create sustainable technologies.", height=120)
        theme = st.text_input("Theme", placeholder="Sustainability & AI")
        
        col1, col2 = st.columns(2)
        with col1:
            max_participants = st.number_input("Max Participants", min_value=10, max_value=500, value=100)
        with col2:
            prize_pool = st.number_input("Prize Pool (€)", min_value=0, max_value=100000, value=5000)
        
        # Tags
        st.markdown("**Tags** (comma-separated)")
        tags_input = st.text_input("Tags", placeholder="AI, Climate, Sustainability, Machine Learning")
        
        submitted = st.form_submit_button("Next Step ➡️", use_container_width=True)
        
        if submitted and title and description:
            st.session_state.hackathon_data = {
                "title": title,
                "description": description,
                "theme": theme,
                "max_participants": max_participants,
                "prize_pool": prize_pool,
                "tags": [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            }
            st.session_state.wizard_step = 2
            st.rerun()

# Step 2: Venue Selection
elif st.session_state.wizard_step == 2:
    st.markdown("## 📍 Venue Selection")
    
    # Predefined venues for demo
    venues = [
        {"name": "TechHub Warsaw", "address": "Rondo ONZ 1, Warsaw", "lat": 52.2297, "lng": 21.0122, "capacity": 100},
        {"name": "Innovation Center Krakow", "address": "Rynek Główny 1, Krakow", "lat": 50.0647, "lng": 19.9450, "capacity": 80},
        {"name": "Digital Campus Gdansk", "address": "Długi Targ 1, Gdansk", "lat": 54.3520, "lng": 18.6466, "capacity": 60},
        {"name": "StartupLab Berlin", "address": "Potsdamer Platz 1, Berlin", "lat": 52.5096, "lng": 13.3765, "capacity": 120},
        {"name": "Innovation Hub Amsterdam", "address": "Dam Square 1, Amsterdam", "lat": 52.3702, "lng": 4.8952, "capacity": 90}
    ]
    
    with st.form("venue_form"):
        st.markdown("**Select a venue or add custom location:**")
        
        venue_option = st.selectbox("Choose Venue", 
                                   ["Select from list"] + [f"{v['name']} - {v['address']}" for v in venues] + ["Custom venue"])
        
        if venue_option != "Select from list" and venue_option != "Custom venue":
            # Pre-selected venue
            selected_venue = venues[[f"{v['name']} - {v['address']}" for v in venues].index(venue_option)]
            st.info(f"Selected: {selected_venue['name']} (Capacity: {selected_venue['capacity']})")
            
        elif venue_option == "Custom venue":
            st.markdown("**Custom Venue Details:**")
            custom_name = st.text_input("Venue Name")
            custom_address = st.text_input("Address")
            col1, col2, col3 = st.columns(3)
            with col1:
                custom_lat = st.number_input("Latitude", value=52.2297)
            with col2:
                custom_lng = st.number_input("Longitude", value=21.0122)
            with col3:
                custom_capacity = st.number_input("Capacity", min_value=10, value=50)
        
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("⬅️ Back", use_container_width=True)
        with col2:
            next_step = st.form_submit_button("Next Step ➡️", use_container_width=True)
        
        if back:
            st.session_state.wizard_step = 1
            st.rerun()
        
        if next_step and venue_option != "Select from list":
            if venue_option == "Custom venue":
                venue_data = {
                    "venue_name": custom_name,
                    "venue_address": custom_address,
                    "latitude": custom_lat,
                    "longitude": custom_lng,
                    "capacity": custom_capacity
                }
            else:
                selected_venue = venues[[f"{v['name']} - {v['address']}" for v in venues].index(venue_option)]
                venue_data = {
                    "venue_name": selected_venue["name"],
                    "venue_address": selected_venue["address"],
                    "latitude": selected_venue["lat"],
                    "longitude": selected_venue["lng"],
                    "capacity": selected_venue["capacity"]
                }
            
            st.session_state.hackathon_data.update(venue_data)
            st.session_state.wizard_step = 3
            st.rerun()

# Step 3: Schedule
elif st.session_state.wizard_step == 3:
    st.markdown("## 📅 Schedule")
    
    with st.form("schedule_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now().date() + timedelta(days=7))
            start_time = st.time_input("Start Time", value=datetime.now().time().replace(hour=10, minute=0))
        
        with col2:
            end_date = st.date_input("End Date", value=datetime.now().date() + timedelta(days=9))
            end_time = st.time_input("End Time", value=datetime.now().time().replace(hour=18, minute=0))
        
        # Combine date and time
        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)
        
        # Validation
        if start_datetime >= end_datetime:
            st.error("End date/time must be after start date/time")
        
        duration = end_datetime - start_datetime
        st.info(f"Hackathon duration: {duration.days} days, {duration.seconds // 3600} hours")
        
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("⬅️ Back", use_container_width=True)
        with col2:
            next_step = st.form_submit_button("Next Step ➡️", use_container_width=True)
        
        if back:
            st.session_state.wizard_step = 2
            st.rerun()
        
        if next_step and start_datetime < end_datetime:
            st.session_state.hackathon_data.update({
                "start_datetime": start_datetime,
                "end_datetime": end_datetime
            })
            st.session_state.wizard_step = 4
            st.rerun()

# Step 4: Requirements
elif st.session_state.wizard_step == 4:
    st.markdown("## 📋 Requirements & Rules")
    
    with st.form("requirements_form"):
        st.markdown("**Participant Requirements:**")
        requirements = st.text_area("Requirements (one per line)", 
                                   placeholder="Python experience\nBasic ML knowledge\nLaptop required", 
                                   height=120)
        
        st.markdown("**Rules & Guidelines:**")
        rules = st.text_area("Rules", 
                            placeholder="Teams of 2-4 people\nOriginal code only\nPresentation required", 
                            height=120)
        
        st.markdown("**Judging Criteria:**")
        criteria = st.text_area("Criteria", 
                               placeholder="Innovation (30%)\nTechnical execution (30%)\nImpact potential (25%)\nPresentation (15%)", 
                               height=120)
        
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("⬅️ Back", use_container_width=True)
        with col2:
            next_step = st.form_submit_button("Next Step ➡️", use_container_width=True)
        
        if back:
            st.session_state.wizard_step = 3
            st.rerun()
        
        if next_step:
            st.session_state.hackathon_data.update({
                "requirements": [req.strip() for req in requirements.split("\n") if req.strip()],
                "rules": rules,
                "criteria": criteria
            })
            st.session_state.wizard_step = 5
            st.rerun()

# Step 5: Review & Create
elif st.session_state.wizard_step == 5:
    st.markdown("## 📋 Review & Create")
    
    data = st.session_state.hackathon_data
    
    # Display summary
    st.markdown(f"### {data['title']}")
    st.markdown(f"**Theme:** {data['theme']}")
    st.markdown(f"**Description:** {data['description']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Venue:** {data['venue_name']}")
        st.markdown(f"**Address:** {data['venue_address']}")
        st.markdown(f"**Capacity:** {data['capacity']} participants")
    
    with col2:
        st.markdown(f"**Start:** {data['start_datetime'].strftime('%B %d, %Y at %I:%M %p')}")
        st.markdown(f"**End:** {data['end_datetime'].strftime('%B %d, %Y at %I:%M %p')}")
        st.markdown(f"**Prize Pool:** €{data['prize_pool']:,}")
    
    if data.get('tags'):
        st.markdown(f"**Tags:** {', '.join(data['tags'])}")
    
    if data.get('requirements'):
        st.markdown("**Requirements:**")
        for req in data['requirements']:
            st.markdown(f"- {req}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Edit", use_container_width=True):
            st.session_state.wizard_step = 4
            st.rerun()
    
    with col2:
        if st.button("🚀 Create Hackathon", use_container_width=True):
            # Create hackathon
            try:
                hackathon = hackathon_service.create_hackathon(data, st.session_state.current_user)
                st.success(f"🎉 Hackathon '{hackathon.title}' created successfully!")
                st.balloons()
                
                # Reset wizard
                if "hackathon_data" in st.session_state:
                    del st.session_state.hackathon_data
                st.session_state.wizard_step = 1
                
                # Option to view or create another
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📍 View on Map", use_container_width=True):
                        st.switch_page("pages/2_Map_View.py")
                with col2:
                    if st.button("🎯 Create Another", use_container_width=True):
                        st.rerun()
                        
            except Exception as e:
                st.error(f"Error creating hackathon: {str(e)}")

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
    if st.button("🚀 Browse MVPs", use_container_width=True):
        st.switch_page("pages/3_MVP_Showcase.py")
