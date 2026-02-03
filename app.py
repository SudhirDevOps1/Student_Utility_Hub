import streamlit as st
import os
from pathlib import Path

# Import all modules
import image_tools
import pdf_tools
import ocr_text_tools
import student_utils
import file_manager
import extension
import learning_tools
import productivity_tools
import analytics_tools
import creative_tools
import utility_tools
import study_resources

# Page config
st.set_page_config(
    page_title="Student Utility Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Advanced Dark Theme CSS with Glassmorphism
def apply_custom_css():
    theme = st.session_state.theme
    
    if theme == 'dark':
        bg_color = "#0f1419"
        card_bg = "rgba(30, 35, 45, 0.7)"
        glass_bg = "rgba(255, 255, 255, 0.05)"
        text_color = "#e8eaed"
        border_color = "rgba(255, 255, 255, 0.1)"
        gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        shadow = "0 8px 32px 0 rgba(31, 38, 135, 0.37)"
    else:
        bg_color = "#ffffff"
        card_bg = "rgba(255, 255, 255, 0.7)"
        glass_bg = "rgba(0, 0, 0, 0.05)"
        text_color = "#1f2937"
        border_color = "rgba(0, 0, 0, 0.1)"
        gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.1)"
    
    css = f"""
    <style>
        /* Global Styles */
        .stApp {{
            background: {bg_color};
            color: {text_color};
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }}
        
        /* Header Styling */
        .app-header {{
            background: {gradient};
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: {shadow};
            text-align: center;
            backdrop-filter: blur(10px);
        }}
        
        .app-header h1 {{
            color: white;
            font-size: 3rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .app-header p {{
            color: rgba(255,255,255,0.9);
            font-size: 1.2rem;
            margin: 0.5rem 0 0 0;
        }}
        
        /* Glassmorphism Cards */
        .glass-card {{
            background: {glass_bg};
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem 0;
            border: 1px solid {border_color};
            box-shadow: {shadow};
            transition: all 0.3s ease;
        }}
        
        .glass-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
        }}
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background: {card_bg};
            backdrop-filter: blur(10px);
            border-right: 1px solid {border_color};
        }}
        
        section[data-testid="stSidebar"] > div {{
            background: transparent;
        }}
        
        /* Buttons */
        .stButton > button {{
            background: {gradient};
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: {shadow};
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 40px 0 rgba(102, 126, 234, 0.6);
        }}
        
        /* File Uploader */
        .stFileUploader {{
            background: {glass_bg};
            border-radius: 15px;
            padding: 1.5rem;
            border: 2px dashed {border_color};
            transition: all 0.3s ease;
        }}
        
        .stFileUploader:hover {{
            border-color: #667eea;
        }}
        
        /* Progress Bar */
        .stProgress > div > div {{
            background: {gradient};
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
            background: transparent;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: {glass_bg};
            border-radius: 50px;
            padding: 10px 25px;
            border: 1px solid {border_color};
            transition: all 0.3s ease;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            background: {gradient};
            color: white;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: {gradient};
            color: white !important;
        }}
        
        /* Success/Error Messages */
        .stSuccess {{
            background: rgba(76, 175, 80, 0.1);
            border-left: 4px solid #4caf50;
            border-radius: 10px;
        }}
        
        .stError {{
            background: rgba(244, 67, 54, 0.1);
            border-left: 4px solid #f44336;
            border-radius: 10px;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            border-top: 1px solid {border_color};
            color: {text_color};
            font-size: 1rem;
        }}
        
        .footer strong {{
            background: {gradient};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        /* Metrics */
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            font-weight: 700;
            background: {gradient};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        /* Text Input */
        .stTextInput > div > div > input {{
            background: {glass_bg};
            border: 1px solid {border_color};
            border-radius: 12px;
            color: {text_color};
            padding: 10px 15px;
        }}
        
        /* Selectbox */
        .stSelectbox > div > div {{
            background: {glass_bg};
            border: 1px solid {border_color};
            border-radius: 12px;
        }}
        
        /* Dataframe */
        .stDataFrame {{
            border-radius: 15px;
            overflow: hidden;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background: {glass_bg};
            border-radius: 12px;
            border: 1px solid {border_color};
        }}
        
        /* Animation */
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .glass-card {{
            animation: slideIn 0.5s ease-out;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Header
def render_header():
    st.markdown(f"""
    <div class="app-header">
        <h1>🎓 Student Utility Hub</h1>
        <p>Your All-in-One Student Productivity Platform</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
def render_footer():
    st.markdown(f"""
    <div class="footer">
        Built by <strong>Sudhir Kumar</strong> | <strong>@SudhirDevOps1</strong>
    </div>
    """, unsafe_allow_html=True)

# Main App
def main():
    apply_custom_css()
    render_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Theme Toggle
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌙 Dark", use_container_width=True, 
                        type="primary" if st.session_state.theme == 'dark' else "secondary"):
                st.session_state.theme = 'dark'
                st.rerun()
        with col2:
            if st.button("☀️ Light", use_container_width=True,
                        type="primary" if st.session_state.theme == 'light' else "secondary"):
                st.session_state.theme = 'light'
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📋 Navigation")
        
        # Navigation
        menu_options = {
            "🖼 Image Tools": "image_tools",
            "📄 PDF Tools": "pdf_tools",
            "🔍 OCR & Text": "ocr_text",
            "🎓 Student Utilities": "student_utils",
            "📂 File Manager": "file_manager",
            "🧩 File Converter": "file_converter",
            "📚 Learning Tools": "learning_tools",
            "🎯 Productivity+": "productivity_tools",
            "📊 Analytics": "analytics_tools",
            "🎨 Creative Tools": "creative_tools",
            "🌐 Utilities": "utility_tools",
            "📚 Study Resources": "study_resources",
            "⚡ Extra Tools": "extra_tools"
        }
        
        for label, value in menu_options.items():
            if st.button(label, use_container_width=True, key=f"nav_{value}"):
                st.session_state.current_page = value
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "image_tools"
    
    # Main Content
    current_page = st.session_state.current_page
    
    if current_page == "image_tools":
        image_tools.show()
    elif current_page == "pdf_tools":
        pdf_tools.show()
    elif current_page == "ocr_text":
        ocr_text_tools.show()
    elif current_page == "student_utils":
        student_utils.show()
    elif current_page == "file_manager":
        file_manager.show()
    elif current_page == "file_converter":
        extension.show()
    elif current_page == "learning_tools":
        learning_tools.show()
    elif current_page == "productivity_tools":
        productivity_tools.show()
    elif current_page == "analytics_tools":
        analytics_tools.show()
    elif current_page == "creative_tools":
        creative_tools.show()
    elif current_page == "utility_tools":
        utility_tools.show()
    elif current_page == "study_resources":
        study_resources.show()
    elif current_page == "extra_tools":
        show_extra_tools()
    
    render_footer()

# Extra Tools Section
def show_extra_tools():
    import qrcode
    from io import BytesIO
    import random
    import string
    
    st.markdown("## ⚡ Extra Tools")
    
    tabs = st.tabs(["QR Code Generator", "Password Generator", "URL Notes"])
    
    # QR Code Generator
    with tabs[0]:
        st.markdown("### 📱 QR Code Generator")
        qr_text = st.text_area("Enter text or URL:", placeholder="https://example.com")
        
        col1, col2 = st.columns(2)
        with col1:
            qr_size = st.slider("Size", 5, 20, 10)
        with col2:
            qr_border = st.slider("Border", 1, 10, 2)
        
        if st.button("Generate QR Code"):
            if qr_text:
                qr = qrcode.QRCode(version=1, box_size=qr_size, border=qr_border)
                qr.add_data(qr_text)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                
                buf = BytesIO()
                img.save(buf, format='PNG')
                buf.seek(0)
                
                st.image(buf, caption="Generated QR Code")
                st.download_button("Download QR Code", buf, "qrcode.png", "image/png")
    
    # Password Generator
    with tabs[1]:
        st.markdown("### 🔐 Password Generator")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            pwd_length = st.slider("Length", 8, 32, 16)
        with col2:
            use_special = st.checkbox("Special Characters", True)
        with col3:
            use_numbers = st.checkbox("Numbers", True)
        
        if st.button("Generate Password"):
            chars = string.ascii_letters
            if use_numbers:
                chars += string.digits
            if use_special:
                chars += string.punctuation
            
            password = ''.join(random.choice(chars) for _ in range(pwd_length))
            st.code(password, language=None)
            st.success("Password generated! Copy it now.")
    
    # URL Notes
    with tabs[2]:
        st.markdown("### 📝 URL Short Notes Saver")
        
        if 'url_notes' not in st.session_state:
            st.session_state.url_notes = []
        
        col1, col2 = st.columns([3, 1])
        with col1:
            note_url = st.text_input("URL:", key="url_input")
            note_text = st.text_area("Note:", key="note_input")
        with col2:
            if st.button("Save Note"):
                if note_url and note_text:
                    st.session_state.url_notes.append({"url": note_url, "note": note_text})
                    st.success("Note saved!")
        
        st.markdown("### 📋 Saved Notes")
        for i, note in enumerate(st.session_state.url_notes):
            with st.expander(f"📌 {note['url'][:50]}..."):
                st.write(note['note'])
                if st.button(f"Delete", key=f"del_{i}"):
                    st.session_state.url_notes.pop(i)
                    st.rerun()

if __name__ == "__main__":
    main()
