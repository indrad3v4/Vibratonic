import streamlit as st

def apply_custom_styling():
    """Apply custom styling to the Streamlit app"""
    st.markdown("""
    <style>
    /* Custom CSS for Vibratonic neon theme */
    .stApp {
        background-color: #0A0A0A;
        color: #FFFFFF;
    }
    
    /* Header styling */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 2px solid #00FFE1;
        margin-bottom: 2rem;
    }
    
    .app-title {
        color: #00FFE1;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 0 0 10px #00FFE1;
    }
    
    .app-tagline {
        color: #FF00A8;
        font-size: 1rem;
        margin: 0;
        text-shadow: 0 0 5px #FF00A8;
    }
    
    .user-section {
        text-align: right;
    }
    
    .user-greeting {
        color: #FFFFFF;
        font-size: 1.1rem;
    }
    
    .user-role {
        color: #FFD700;
        font-size: 0.9rem;
        text-transform: uppercase;
        font-weight: bold;
    }
    
    /* Navigation styling */
    .nav-container {
        margin-bottom: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #00FFE1, #FF00A8);
        border: none;
        border-radius: 8px;
        color: #000000;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 255, 225, 0.4);
    }
    
    /* Card styling */
    .hack-card, .mvp-card {
        background: #1A1A1A;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .hack-card:hover, .mvp-card:hover {
        border-color: #00FFE1;
        box-shadow: 0 4px 15px rgba(0, 255, 225, 0.2);
    }
    
    .hack-title, .mvp-title {
        color: #00FFE1;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .hack-description, .mvp-description {
        color: #CCCCCC;
        margin-bottom: 1rem;
    }
    
    /* Progress bar styling */
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #333333;
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00FFE1, #FF00A8);
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    /* Tag styling */
    .tag, .tech-tag, .skill-tag {
        background: rgba(0, 255, 225, 0.2);
        color: #00FFE1;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
        border: 1px solid #00FFE1;
    }
    
    .tech-tag {
        background: rgba(255, 0, 168, 0.2);
        color: #FF00A8;
        border-color: #FF00A8;
    }
    
    .skill-tag {
        background: rgba(255, 215, 0, 0.2);
        color: #FFD700;
        border-color: #FFD700;
    }
    
    /* Status styling */
    .hack-status, .mvp-status {
        font-weight: bold;
        padding: 0.25rem 0.5rem;
        border-radius: 8px;
        font-size: 0.8rem;
        text-transform: uppercase;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, rgba(0, 255, 225, 0.1), rgba(255, 0, 168, 0.1));
        border-radius: 16px;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        color: #FFFFFF;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(0, 255, 225, 0.5);
    }
    
    .hero-description {
        color: #CCCCCC;
        font-size: 1.2rem;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Action cards */
    .action-card {
        background: #1A1A1A;
        border: 2px solid #333333;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .action-card:hover {
        border-color: #00FFE1;
        background: rgba(0, 255, 225, 0.05);
        transform: translateY(-5px);
    }
    
    /* Profile styling */
    .profile-avatar, .profile-avatar-large {
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .avatar-circle, .avatar-circle-large {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(45deg, #00FFE1, #FF00A8);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        font-size: 2rem;
        font-weight: bold;
        color: #000000;
    }
    
    .avatar-circle-large {
        width: 120px;
        height: 120px;
        font-size: 3rem;
    }
    
    /* Activity feed */
    .activity-item, .activity-card {
        background: #1A1A1A;
        border-left: 3px solid #00FFE1;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    
    .activity-icon {
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
    
    .activity-text {
        color: #FFFFFF;
    }
    
    .activity-time {
        color: #888888;
        font-size: 0.9rem;
        float: right;
    }
    
    /* Funding styling */
    .funding-tier {
        background: #1A1A1A;
        border: 2px solid;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
    }
    
    .tier-amount {
        font-size: 1.5rem;
        font-weight: bold;
        color: #FFFFFF;
        margin: 0.5rem 0;
    }
    
    .tier-description {
        color: #CCCCCC;
        margin-bottom: 0.5rem;
    }
    
    .tier-rewards {
        color: #AAAAAA;
        font-size: 0.9rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        border-top: 1px solid #333333;
        margin-top: 3rem;
        color: #888888;
    }
    
    /* Custom metric styling */
    [data-testid="metric-container"] {
        background: #1A1A1A;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    [data-testid="metric-container"]:hover {
        border-color: #00FFE1;
        box-shadow: 0 2px 10px rgba(0, 255, 225, 0.2);
    }
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: #1A1A1A;
        border: 1px solid #333333;
        border-radius: 8px;
        color: #FFFFFF;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #00FFE1;
        box-shadow: 0 0 5px rgba(0, 255, 225, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1A1A1A;
    }
    
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom animations */
    @keyframes glow {
        0% { text-shadow: 0 0 5px currentColor; }
        50% { text-shadow: 0 0 20px currentColor; }
        100% { text-shadow: 0 0 5px currentColor; }
    }
    
    .glow-text {
        animation: glow 2s ease-in-out infinite alternate;
    }
    </style>
    """, unsafe_allow_html=True)

def load_css(file_path):
    """Load CSS from a file"""
    try:
        with open(file_path, "r") as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # CSS file doesn't exist, skip loading
        pass

def apply_neon_theme():
    """Apply neon color theme to components"""
    st.markdown("""
    <style>
    /* Neon theme colors */
    :root {
        --primary-color: #00FFE1;
        --secondary-color: #FF00A8;
        --accent-color: #FFD700;
        --background-color: #0A0A0A;
        --surface-color: #1A1A1A;
        --text-color: #FFFFFF;
        --text-secondary: #CCCCCC;
    }
    
    /* Apply theme to components */
    .element-container {
        color: var(--text-color);
    }
    
    .stMarkdown {
        color: var(--text-color);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-color);
    }
    
    .stAlert > div {
        background-color: var(--surface-color);
        border-color: var(--primary-color);
        color: var(--text-color);
    }
    
    .stSuccess > div {
        background-color: rgba(0, 255, 225, 0.1);
        border-color: var(--primary-color);
    }
    
    .stError > div {
        background-color: rgba(255, 0, 168, 0.1);
        border-color: var(--secondary-color);
    }
    
    .stWarning > div {
        background-color: rgba(255, 215, 0, 0.1);
        border-color: var(--accent-color);
    }
    
    .stInfo > div {
        background-color: rgba(0, 255, 225, 0.1);
        border-color: var(--primary-color);
    }
    </style>
    """, unsafe_allow_html=True)

def create_glowing_button(text, color="#00FFE1"):
    """Create a glowing button with custom color"""
    return f"""
    <style>
    .glow-button {{
        background: linear-gradient(45deg, {color}, #FF00A8);
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        color: #000000;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
        box-shadow: 0 0 10px {color}40;
    }}
    
    .glow-button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 15px {color}80;
    }}
    </style>
    <button class="glow-button">{text}</button>
    """

def apply_mobile_optimizations():
    """Apply mobile-first responsive design optimizations"""
    st.markdown("""
    <style>
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2rem;
        }
        
        .hero-title {
            font-size: 2rem;
        }
        
        .hero-description {
            font-size: 1rem;
        }
        
        .hack-card, .mvp-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .action-card {
            padding: 1.5rem;
            margin: 0.5rem;
        }
        
        .stButton > button {
            width: 100%;
            margin: 0.25rem 0;
        }
        
        .header-container {
            flex-direction: column;
            text-align: center;
        }
        
        .nav-container {
            overflow-x: auto;
        }
    }
    
    @media (max-width: 480px) {
        .app-title {
            font-size: 1.5rem;
        }
        
        .hero-title {
            font-size: 1.5rem;
        }
        
        .hero-section {
            padding: 2rem 0;
        }
        
        .hack-card, .mvp-card {
            padding: 0.75rem;
        }
        
        .action-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
