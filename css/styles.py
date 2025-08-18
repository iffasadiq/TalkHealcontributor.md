import streamlit as st
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def apply_custom_css():
    from core.theme import get_current_theme
    theme_config = get_current_theme()
    theme_overrides = {
        'primary': '#6366f1',
        'primary_light': '#818cf8',
        'primary_dark': '#4f46e5',
        'secondary': '#ec4899',
        'success': '#10b981',
        'warning': '#f59e0b',
        'danger': '#ef4444',
        'surface': 'rgba(255,255,255,0.14)',
        'surface_alt': 'rgba(25,25,46,0.23)',
        'text_primary': '#fff',
        'text_secondary': 'white',
        'text_muted': '#a0aec0',
        'border': 'rgba(255,255,255,0.18)',
        'border_light': 'rgba(255,255,255,0.09)',
        'shadow': '0 4px 32px rgba(33,40,98,0.13)',
        'shadow_lg': '0 16px 48px rgba(99,102,241,0.12)',
        'background_overlay': 'linear-gradient(120deg, rgba(34,37,74,0.53) 0%, rgba(34,41,79,0.68) 100%)'
    }
    theme_config.update(theme_overrides)

    background_image_path = theme_config.get('background_image', 'static_files/Background.jpg')
    base64_image = get_base64_of_bin_file(background_image_path) if background_image_path else None
    st.markdown(f"""
    <style>
        /* Font imports */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap');

        /* CSS variables and root styling */
        :root {{
            --primary-color: {theme_config['primary']};
            --primary-light: {theme_config['primary_light']};
            --primary-dark: {theme_config['primary_dark']};
            --secondary-color: {theme_config['secondary']};
            --success-color: {theme_config['success']};
            --warning-color: {theme_config['warning']};
            --danger-color: {theme_config['danger']};
            --surface: {theme_config['surface']};
            --surface-alt: {theme_config['surface_alt']};
            --text-primary: {theme_config['text_primary']};
            --text-secondary: {theme_config['text_secondary']};
            --text-muted: {theme_config['text_muted']};
            --border: {theme_config['border']};
            --border-light: {theme_config['border_light']};
            --shadow: {theme_config['shadow']};
            --shadow-lg: {theme_config['shadow_lg']};
            --radius: 12px;
            --radius-lg: 22px;
            --radius-xl: 36px;
            --glass-effect: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.05));
            --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .stApp > header {{
            background-color: transparent !important;
        }}
        
        /* Main app background and styling */
        .stApp {{
            background-image: url("data:image/jpeg;base64,{base64_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center center;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            min-height: 100vh;
            color: var(--text-primary);
            letter-spacing: 0.01em;
        }}

        /* Background overlay */
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: var(--background-overlay);
            z-index: -1;
        }}

        /* Smooth scrolling */
        html {{ scroll-behavior: smooth; }}

        /* Main container styling */
        .main .block-container {{
            padding-top: 1rem;
            padding-bottom: 2.5rem;
            max-width: 1200px;
            margin: 0 auto;
        }}

        /* Hero Section */
        .hero-section {{
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(236,72,153,0.15));
            border-radius: 24px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}

        .hero-section h1 {{
            font-family: 'Poppins', sans-serif;
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(135deg, #6366f1, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
        }}

        .hero-section p {{
            font-size: 1.2em;
            color: rgba(255,255,255,0.9);
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.6;
        }}

        /* Feature Cards */
        .feature-card {{
            background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.08));
            border-radius: 20px;
            padding: 25px 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: all 0.3s cubic-bezier(0.25,0.8,0.25,1);
            position: relative;
            overflow: hidden;
            height: 200px;
            display: flex;
            flex-direction: column;
        }}

        .feature-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            border-radius: 20px 20px 0 0;
        }}

        .feature-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 16px 48px rgba(0,0,0,0.2);
            border-color: rgba(255,255,255,0.3);
        }}

        .card-icon {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-align: center;
        }}

        .feature-card h3 {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.3em;
            font-weight: 600;
            color: white;
            margin-bottom: 12px;
            text-align: center;
        }}

        .feature-card p {{
            color: rgba(255,255,255,0.85);
            font-size: 0.95em;
            line-height: 1.5;
            text-align: center;
            margin-bottom: 15px;
            flex-grow: 1;
        }}

        .card-features {{
            font-size: 0.85em;
            color: rgba(255,255,255,0.7);
            text-align: left;
            margin-top: auto;
        }}

        .card-features span {{
            display: block;
            margin-bottom: 3px;
        }}

        /* Specific card colors */
        .mindfulness-card::before {{ background: linear-gradient(90deg, #10b981, #059669); }}
        .breathing-card::before {{ background: linear-gradient(90deg, #06b6d4, #0891b2); }}
        .focus-card::before {{ background: linear-gradient(90deg, #8b5cf6, #7c3aed); }}
        .journaling-card::before {{ background: linear-gradient(90deg, #f59e0b, #d97706); }}
        .mood-card::before {{ background: linear-gradient(90deg, #ec4899, #be185d); }}
        .selfhelp-card::before {{ background: linear-gradient(90deg, #6366f1, #4f46e5); }}
        .doctor-card::before {{ background: linear-gradient(90deg, #ef4444, #dc2626); }}
        .emergency-card::before {{ background: linear-gradient(90deg, #dc2626, #b91c1c); }}
        .about-card::before {{ background: linear-gradient(90deg, #6b7280, #4b5563); }}

        /* Typography styling */
        h1, h2, h3, h4 {{
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            margin-bottom: .45em;
        }}

        p {{
            font-weight: 400;
            color: var(--text-secondary);
            line-height: 1.68;
            margin-bottom: 1.1em;
        }}

        /* Message bubble styling */
        .user-message,.bot-message {{
            font-size: 1.08em;
            padding: 16px 22px;
            border-radius: 20px 20px 8px 18px;
            margin: 22px 0 16px auto;
            max-width: 75%;
            word-break: break-word;
            box-shadow: var(--shadow);
            font-weight: 470;
            line-height: 1.5;
            position: relative;
            backdrop-filter: blur(11px);
            display: block;
            opacity: 0;
            animation: floatUp 0.5s cubic-bezier(0.25,0.8,0.25,1) forwards;
        }}
        
        /* User message styling */
        .user-message {{
            color: #fff;
            background: linear-gradient(130deg, #6366f1 70%, #818cf8 100%);
            border: 1.5px solid rgba(129,140,248,0.21);
            margin-left: auto;
            margin-right: 0;
        }}
        
        /* Bot message styling */
        .bot-message {{
            background: var(--glass-effect);
            background-color: var(--surface-alt);
            color: #efeef9;
            border: 1.25px solid var(--border);
            margin-left: 0;
            margin-right: auto;
        }}
        
        /* Message animation */
        @keyframes floatUp {{
            from {{ transform: translateY(20px); opacity: 0; }}
            to   {{ transform: none; opacity: 1; }}
        }}

        /* Message timestamp styling */
        .message-time {{
            font-size: .78em;
            opacity: .76;
            text-align: right;
            margin-top: 8px;
            color: #c8defe;
        }}
        .bot-message .message-time {{
            color: #c4d0e0;
        }}

        /* Welcome message styling */
        .welcome-message {{
            background: linear-gradient(120deg, rgba(99,102,241,0.75) 0%, rgba(236,72,153,0.75) 100%);
            color: #f7fafb;
            padding: 33px 24px 27px 24px;
            margin: 38px auto 32px auto;
            border-radius: var(--radius-xl);
            max-width: 680px;
            box-shadow: 0 6px 38px 0 rgba(96,100,255,0.11);
            font-size: 1.14em;
            text-align: center;
            backdrop-filter: blur(12px);
            position: relative;
            overflow: hidden;
            transform: scale(0.97);
            opacity: 0;
            animation: scaleIn 0.7s cubic-bezier(0.22,0.68,0.32,1.18) .1s forwards;
        }}
        
        /* Welcome message animation */
        @keyframes scaleIn {{
            from {{ transform: scale(0.97); opacity: 0;  }}
            to   {{ transform: scale(1); opacity: 1; }}
        }}

        /* Main header styling */
        .main-header {{
            --gradient: linear-gradient(100deg, var(--primary-color), var(--secondary-color));
            text-align: center;
            padding: 38px 20px 28px 20px;
            background: var(--surface);
            color: white;
            border-radius: var(--radius-xl);
            margin-bottom: 32px;
            box-shadow: var(--shadow-lg);
            border: 1px solid var(--border-light);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }}
        
        /* Header gradient animation */
        .main-header::before {{
            content: '';
            position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: var(--gradient);
            animation: gradientFlow 7s linear infinite;
            background-size: 200% 200%;
        }}
        @keyframes gradientFlow {{
          0% {{ background-position: 0% 50%; }}
          50% {{ background-position: 100% 50%;}}
          100% {{ background-position: 0% 50%;}}
        }}
        
        /* Header title styling */
        .main-header h1 {{
            margin: 0 0 11px 0;
            font-size: 2.35em;
            font-weight: 700;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            display: inline-block;
            letter-spacing: 1px;
        }}
        
        /* Header description styling */
        .main-header p {{
            font-size: 1.19em;
            font-weight: 450;
            color: rgba(255,255,255,0.93);
            margin: 0 auto;
            max-width: 640px;
        }}

        /* Emergency button styling */
        .emergency_button {{
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.9) 20%, rgba(220, 38, 38, 0.9) 80%) !important;
            color: white !important;
            padding: 18px 24px;
            display: block;
            border-radius: var(--radius-xl) !important;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
            cursor: pointer;
            transition: var(--transition) !important;
            font-weight: 600;
            font-size: 1.1em;
            border: 1px solid rgba(239, 68, 68, 0.8) !important;
            backdrop-filter: blur(5px);
            text-decoration: none !important;
            position: relative;
            overflow: hidden;
            z-index: 1;
        }}
        
        /* Emergency button hover effect */
        .emergency_button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(220, 38, 38, 1) 0%, rgba(185, 28, 28, 1) 100%);
            z-index: -1;
            opacity: 0;
            transition: var(--transition);
        }}
        .emergency_button:hover {{
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
        }}
        .emergency_button:hover::before {{
            opacity: 1;
        }}
        
        /* Emergency button pulse animation */
        .emergency_button.pulse {{
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
            70% {{ box-shadow: 0 0 0 15px rgba(239, 68, 68, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
        }}

        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: linear-gradient(120deg, rgba(236,72,153,0.45), rgba(219,39,119,0.25), rgba(236,72,153,0.15)) !important;
            backdrop-filter: blur(15px) !important;
            border-right: 2px solid rgba(236,72,153,0.35) !important;
            box-shadow: 8px 0 48px rgba(236,72,153,0.25) !important;
            color: #e2e8f0 !important;
            transition: background .32s cubic-bezier(.5,.13,.36,1.19);
        }}
        [data-testid="stSidebar"] * {{
            color: #f5f7fb !important;
        }}

        /* Sidebar toggle button styling */
        .stApp [data-testid="stSidebarToggleButton"] button,
        button[data-testid="stSidebarToggleButton"],
        [data-testid="stSidebarToggleButton"] > button,
        div[data-testid="stSidebarToggleButton"] button,
        .stApp > div > div > div > button[title*="Toggle"],
        .stApp header button {{
            background: rgba(30, 41, 59, 0.9) !important;
            color: #ffffff !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 50% !important;
            width: 40px !important;
            height: 40px !important;
            font-size: 20px !important;
            font-weight: 900 !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(10px) !important;
        }}
        
        /* Sidebar toggle button hover effects */
        .stApp [data-testid="stSidebarToggleButton"] button:hover,
        button[data-testid="stSidebarToggleButton"]:hover,
        [data-testid="stSidebarToggleButton"] > button:hover,
        div[data-testid="stSidebarToggleButton"] button:hover,
        .stApp > div > div > div > button[title*="Toggle"]:hover,
        .stApp header button:hover {{
            background: rgba(30, 41, 59, 1) !important;
            border-color: var(--primary-color) !important;
            transform: scale(1.05) !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
        }}

        /* Send button styling */
        .stChatInputContainer button,
        button[kind="primary"],
        button[data-testid*="send"],
        button[title*="Send"],
        .stChatInput button,
        div[data-testid="stChatInput"] button,
        form button[type="submit"],
        .stApp button[aria-label*="Send"],
        .stApp button[class*="send"] {{
            background: var(--primary-color) !important;
            color: black !important;
            border: 2px solid var(--primary-light) !important;
            border-radius: var(--radius) !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        }}
        
        /* Send button hover effects */
        .stChatInputContainer button:hover,
        button[kind="primary"]:hover,
        button[data-testid*="send"]:hover,
        button[title*="Send"]:hover,
        .stChatInput button:hover,
        div[data-testid="stChatInput"] button:hover,
        form button[type="submit"]:hover,
        .stApp button[aria-label*="Send"]:hover,
        .stApp button[class*="send"]:hover {{
            background: var(--primary-dark) !important;
            transform: scale(1.02) !important;
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4) !important;
        }}

        /* General button styling */
        button, .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {{
            background: var(--glass-effect) !important;
            background-color: var(--light-transparent-bg, rgba(255,255,255,0.13)) !important;
            color: #000000 !important;
            border: 1px solid var(--light-transparent-border, rgba(255,255,255,0.16)) !important;
            border-radius: var(--radius) !important;
            padding: 14px 22px !important;
            font-weight: 600 !important;
            font-family: 'Poppins',sans-serif !important;
            box-shadow: 0 3px 12px rgba(0,0,0,0.08) !important;
            transition: var(--transition,.21s cubic-bezier(.5,.08,.37,1.11)) !important;
        }}
        
        /* General button hover effects */
        button:hover, .stButton > button:hover,
        .stDownloadButton > button:hover,
        .stFormSubmitButton > button:hover {{
            border-color: var(--primary-color) !important;
            border-width: 2px !important;
            transform: translateY(-2px) scale(1.04) !important;
            box-shadow: 0 4px 16px rgba(99,102,241,0.2) !important;
        }}
        
        /* Primary buttons */
        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"] {{
            background: var(--light-transparent-bg, rgba(255,255,255,0.20)) !important;
            color: white !important;
            font-weight: 700 !important;
        }}
        
        .stButton > button[kind="primary"]:hover,
        .stFormSubmitButton > button[kind="primary"]:hover {{
            background: rgba(99, 102, 241, 0.9) !important;
            color: white !important;
        }}
        
        /* Secondary buttons (Emergency) */
        .stButton > button[kind="secondary"] {{
            background: linear-gradient(135deg, #ef4444, #b91c1c) !important;
            color: white !important;
            border: 1px solid #ef4444 !important;
            font-weight: 600 !important;
            transform: none !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        }}

        .stButton > button[kind="secondary"]:hover {{
            background: linear-gradient(135deg, #dc2626, #991b1b) !important;
            border-color: #dc2626 !important;
            color: white !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
        }}
        
        /* Form input styling */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{
            background: var(--glass-effect) !important;
            background-color: #FFDDEE !important;
            border: 2px solid var(--border) !important;
            border-radius: var(--radius) !important;
            font-size: 1em !important;
            color: black;
            font-family: 'Inter',sans-serif !important;
            transition: all .18s cubic-bezier(.35,.72,.44,1.18) !important;
            backdrop-filter: blur(10px) !important;
        }}
        
        /* Input field focus effects */
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: var(--primary-color) !important;
        }}
        
        /* Input placeholder styling */
        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {{
            color: black !important;
            opacity: .77 !important;
        }}

        /* Floating action button styling */
        .floating-action-button {{
            position: fixed;
            bottom: 28px; right: 28px;
            width: 58px; height: 58px;
            border-radius: 50%;
            background: linear-gradient(130deg, var(--primary-color), var(--secondary-color));
            color: #fff;
            display: flex; 
            align-items: center; 
            justify-content: center;
            font-size: 23px;
            box-shadow: 0 6px 24px rgba(0,0,0,0.14);
            cursor: pointer; 
            z-index: 120;
            border: none;
            transition: .16s cubic-bezier(.47,.43,.41,1.35);
        }}
        
        /* Floating action button hover effects */
        .floating-action-button:hover {{
            transform: translateY(-4px) scale(1.10);
            box-shadow: 0 10px 32px rgba(0,0,0,0.27);
        }}

        /* Expander styling */
        .stExpander,
        .stExpander > div,
        .stExpanderHeader,
        .stExpanderContent {{
            background: rgba(255, 255, 255, 0.30) !important;
            color: #f7fafc !important;
            border-radius: var(--radius-lg, 18px) !important;
            border: 1.5px solid var(--border, rgba(255,255,255,0.11)) !important;
            box-shadow: 0 2px 12px rgba(33,40,98,0.10) !important;
            backdrop-filter: blur(8px) !important;
        }}
        
        /* Expander header styling */
        .stExpanderHeader {{
            font-family: 'Poppins',sans-serif !important;
            font-weight: 600 !important;
            color: #dbeafe !important;
            font-size: 1.07em !important;
            padding: 12px 16px !important;
        }}

        /* Expander content styling */
        .stExpanderContent {{
            padding: 16px !important;
        }}

        /* Sidebar section styling */
        .sidebar-section {{
            background: var(--glass-effect) !important;
            background-color: rgba(15, 23, 42, 0.30) !important;
            border-radius: var(--radius-xl) !important;
            padding: 20px 14px !important;
            margin-bottom: 18px !important;
            border: 1px solid var(--light-transparent-border, rgba(255,255,255,.23)) !important;
            backdrop-filter: blur(10px) !important;
            box-shadow: 0 3px 14px rgba(0,0,0,0.07) !important;
        }}

        /* Quick action buttons in main page */
        .quick-action-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .quick-action-btn {{
            background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.1)) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            border-radius: 16px !important;
            padding: 16px !important;
            text-align: center !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(10px) !important;
            font-weight: 600 !important;
            color: white !important;
        }}

        .quick-action-btn:hover {{
            transform: translateY(-4px) scale(1.05) !important;
            box-shadow: 0 12px 32px rgba(0,0,0,0.2) !important;
            border-color: var(--primary-color) !important;
        }}

        /* Section dividers */
        .section-divider {{
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            margin: 30px 0;
        }}

        /* Loading animations */
        .loading-spinner {{
            border: 3px solid rgba(255,255,255,0.2);
            border-top: 3px solid var(--primary-color);
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }}

        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        /* Success/error messages */
        .success-message {{
            background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(5,150,105,0.1));
            border: 1px solid rgba(16,185,129,0.4);
            border-radius: 12px;
            padding: 16px;
            color: #10b981;
            margin: 16px 0;
        }}

        .error-message {{
            background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(220,38,38,0.1));
            border: 1px solid rgba(239,68,68,0.4);
            border-radius: 12px;
            padding: 16px;
            color: #ef4444;
            margin: 16px 0;
        }}

        /* Responsive design for mobile */
        @media (max-width: 768px) {{
            .main .block-container {{ 
                padding: 1rem; 
                max-width: 100%;
            }}
            
            .user-message, .bot-message {{ 
                max-width: 98%; 
                font-size: 1em; 
                padding: 12px 13px; 
            }}
            
            .main-header h1 {{ 
                font-size: 1.8em; 
            }}
            
            .hero-section h1 {{
                font-size: 2em;
            }}
            
            .hero-section p {{
                font-size: 1em;
            }}
            
            .main-header, .welcome-message {{ 
                padding: 16px 4vw; 
            }}
            
            .floating-action-button {{ 
                bottom: 18px; 
                right: 18px; 
                width: 46px; 
                height: 46px; 
                font-size: 15px; 
            }}
            
            [data-testid="stSidebar"] {{ 
                width: 280px !important; 
            }}
            
            .feature-card {{
                height: auto;
                min-height: 180px;
                padding: 20px 15px;
            }}
            
            .card-icon {{
                font-size: 2em;
            }}
            
            .feature-card h3 {{
                font-size: 1.1em;
            }}
            
            .quick-action-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
            }}
        }}

        /* Ultra-wide screen optimizations */
        @media (min-width: 1400px) {{
            .main .block-container {{
                max-width: 1400px;
            }}
            
            .hero-section {{
                padding: 60px 20px;
            }}
            
            .feature-card {{
                height: 220px;
                padding: 30px 25px;
            }}
        }}

        /* Dark mode specific adjustments */
        @media (prefers-color-scheme: dark) {{
            .feature-card {{
                background: linear-gradient(135deg, rgba(30,41,59,0.8), rgba(15,23,42,0.6));
                border: 1px solid rgba(255,255,255,0.1);
            }}
            
            .hero-section {{
                background: linear-gradient(135deg, rgba(30,41,59,0.6), rgba(15,23,42,0.4));
            }}
        }}

        /* Print styles */
        @media print {{
            .floating-action-button,
            [data-testid="stSidebar"],
            .stApp > div:first-child {{
                display: none !important;
            }}
            
            .main .block-container {{
                max-width: 100% !important;
                padding: 0 !important;
            }}
        }}

        /* High contrast mode support */
        @media (prefers-contrast: high) {{
            .feature-card {{
                border: 2px solid white;
                background: rgba(0,0,0,0.8);
            }}
            
            .feature-card h3,
            .feature-card p {{
                color: white;
            }}
        }}

        /* Reduced motion support */
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
            
            .feature-card:hover {{
                transform: none !important;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)