import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Final Polish",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        
        if 'antutu' in df.columns:
            df['perf_score'] = (df['antutu'] / df['antutu'].max()) * 10
        else:
            df['perf_score'] = 8.0 
            
        if 'camera' in df.columns: df['cam_score'] = df['camera']
        if 'battery' in df.columns: df['batt_score'] = df['battery']
        if 'antutu' not in df.columns: df['antutu'] = df['price'] * 2000

        return df
    except Exception:
        return pd.DataFrame()

# --- 3. CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Inter:wght@400;600;900&display=swap');
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #222; }
    section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 { color: #FBBF24 !important; }
    div[data-baseweb="select"] > div { background-color: #222 !important; border: 1px solid #555 !important; }
    div[data-baseweb="select"] span { color: white !important; }
    div[data-baseweb="select"] svg { fill: #FBBF24 !important; }

    /* Winner Box */
    .winner-box {
        background: radial-gradient(circle at top right, #111, #000);
        border: 2px solid #3B82F6; border-radius: 20px; padding: 40px;
        box-shadow: 0 0 60px rgba(59, 130, 246, 0.25);
    }
    .award-badge {
        background: #F59E0B; color: black; font-weight: 900; padding: 10px 20px; 
        border-radius: 50px; text-transform: uppercase; display: inline-block; 
        margin-bottom: 20px; font-size: 0.9em; letter-spacing: 1px;
    }
    .hero-title { font-size: 3.5em; font-weight: 900; color: white; line-height: 1.1; margin-bottom: 15px; }
    .hero-price { color: #FBBF24; font-size: 3em; font-weight: 800; font-family: 'JetBrains Mono'; margin-bottom: 30px; }
    .expert-verdict { background: #111; border-left: 5px solid #3B82F6; padding: 25px; border-radius: 0 12px 12px 0; margin-bottom: 35px; color: #E0E0E0; line-height: 1.6; }
    
    .stat-container { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 35px; }
    .stat-box { background: #151515; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #333; }
    .stat-label { color: #888; font-size: 0.8em; font-weight: 700; margin-bottom: 5px; text-transform: uppercase; }
    .stat-val { font-size: 1.6em; font-weight: 900; color: white; }
    .bar-bg { background: #333; height: 6px; border-radius: 3px; margin-top: 10px; overflow: hidden; }
    
    .bench-row { display: flex; gap: 30px; padding-top: 25px; border-top: 1px solid #222; margin-top: 25px; }
    .bench-item span { font-weight: bold; font-size: 1.2em; margin-left: 8px; color:white; }
    .bench-item { color: #888; font-family: 'JetBrains Mono'; }

    .amazon-btn { background: #3B82F6; color: white !important; padding: 22px; display: block; text-align: center; border-radius: 12px; font-weight: 900; text-decoration: none; font-size: 1.4em; margin-top: 30px; transition: 0.3s; }
    .amazon-btn:hover { background: #2563EB; }

    /* Alternatives */
    .alt-link { text-decoration: none; display: block; }
    .alt-row { background: #0A0A0A; border: 1px solid #222; padding: 20px; border-radius: 12px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; transition: 0.2s; }
    .alt-row:hover { border-color: #FBBF24; background: #111; transform: scale(1.01); }
    .save-tag { color: #10B981; font-weight: bold; margin-left: 10px; }
    
    /* Clean Mini Bars */
    .mini-bar-container { display: flex; gap: 10px; margin-top: 10px; }
    .mini-stat { width: 50px; }
    .mini-track { width: 100%; height: 4px; background: #333; border-radius: 2px; }
    .mini-fill-blue { height: 100%; background: #3B82F6; border-radius: 2px;} 
    .mini-fill-purple { height: 100%; background: #A855F7; border-radius: 2px;} 
    .mini-fill-green { height: 100%; background: #10B981; border-radius: 2px;}
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🛒 TechChoose")
    st.caption("AI Smart Logic Engine")
    st.markdown("---")
    
    st.markdown("### ⚙️ Search Settings")
    os_choice = st.selectbox("📱 Operating System", ["Any", "iOS (Apple)", "Android"])
    st.write("")
    
    lifestyle = st.selectbox("👤 User Persona", [
        "💎 Ultimate High-End",
        "🏠 General Use / Daily Driver",
        "🎮 Hardcore Gamer", 
        "📸 Content Creator", 
        "💼 Business Pro", 
        "💰 Student / Budget", 
        "🛠️ Custom"
    ])
    st.write("")
    
    # --- 🔥 LOGIC: ซ่อน Budget เมื่อเลือก High-End ---
    if "High-End" in lifestyle:
        budget = 9999 # Unlimited Budget
        st.info("💎 Mode: Unlimited Budget Enabled")
    else:
        budget = st.slider("💰 Max Budget (USD)", 100, 2000, 2000, step=50)

    # --- WEIGHTS ---
    p, c, b, v = 5, 5, 5, 5
    price_penalty_threshold = 9999
    
    if "High-End" in lifestyle:
        p,c,b,v = 10, 10, 10, 0
    elif "Gamer" in lifestyle: 
        p,c,b,v = 20, 0, 8, 2
    elif "Creator" in lifestyle: 
        p,c,b,v = 6, 20, 6, 2
    elif "Business" in lifestyle: 
        p,c,b,v = 8, 4, 15, 5
    elif "General" in lifestyle:
        p,c,b,v = 8, 8, 8, 10
    elif "Student" in lifestyle: 
        p,c,b,v = 6, 6, 8, 20
        price_penalty_threshold = 800

    # --- 🔥 CUSTOM: ชื่อเต็มๆ ไม่งง ---
    if "Custom" in lifestyle:
        st.divider()
        st.markdown("### 🎛️ Adjust Preferences")
        p = st.slider("🚀 Performance (ความแรง)", 1, 10, 8)
        c = st.slider("📸 Camera Quality (กล้อง)", 1, 10, 8)
        b = st.slider("🔋 Battery Life (แบตเตอรี่)", 1, 10, 5)
        v = st.slider("💰 Value for Money (ความคุ้มค่า)", 1, 10, 5)

    st.divider()
    st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True)

# --- 5. FUNCTIONS ---
def get_dynamic_badge(mode, price):
    if "High-End" in mode: return "💎 ABSOLUTE BEST IN CLASS"
    elif "Gamer" in mode: return "🏆 GAMING BEAST"
    elif "Creator" in mode: return "🎥 CREATOR CHOICE"
    elif "Student" in mode: return "💰 SMART SAVER PICK"
    elif "Business" in mode: return "💼 RELIABLE WORKHORSE"
    elif "General" in mode: return "⭐ BEST BALANCED PICK"
    else: return "⭐ TOP FLAGSHIP"

def get_expert_verdict(row, mode):
    if "High-End" in mode: return f"<b>No Compromise:</b> This device represents the pinnacle of technology. Maximum performance, best-in-class camera, and premium build quality."
    elif "Gamer" in mode: return f"Built for speed. <b>AnTuTu {int(row['antutu']):,}</b> ensures lag-free gaming."
    elif "Creator" in mode: return f"Studio quality. Top-tier camera system for professional results."
    elif "Business" in mode: return f"<b>All-day Reliability:</b> Prioritizes battery life and multitasking stability for professionals."
    elif "General" in mode: return f"<b>The Perfect Balance:</b> Good camera, smooth performance, and decent battery. A jack of all trades."
    elif "Student" in mode: 
        if row['price'] > 800: return "<b>Luxury Pick:</b> Extremely powerful, but arguably overkill for a student budget."
        else: return "<b>Smart Choice:</b> High-end features at a fraction of the flagship price."
    return f"Excellent all-rounder recommendation."

def stat_bar_html(label, score, color):
    return f"<div class='stat-box'><div class='stat-label'>{label}</div><div class='stat-val'>{score:.1f}/10</div><div class='bar-bg'><div style='width:{score*10}%; height:100%; background:{color};'></div></div></div>"

# --- 6. MAIN APP ---
df = load_data()

if not df.empty:
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']
    df = df[df['price'] <= budget]

    # --- SCORE ENGINE ---
    base_score = (df['perf_score']*p) + (df['cam_score']*c) + (df['batt_score']*b) + (df['value']*v)
    price_penalty = df['price'].apply(lambda x: (x - price_penalty_threshold) * 0.5 if x > price_penalty_threshold else 0)
    df['final_score'] = base_score - price_penalty
    
    max_possible = (10*p) + (10*c) + (10*b) + (10*v)
    df['match'] = (df['final_score'] / max_possible) * 100
    
    df = df.sort_values(by='match', ascending=False).reset_index(drop=True)

    if len(df) > 0:
        winner = df.iloc[0]
        c1, c2 = st.columns([1.5, 1], gap="large")

        with c1:
            current_badge = get_dynamic_badge(lifestyle, winner['price'])
            verdict_html = get_expert_verdict(winner, lifestyle)
            stats_html = f"{stat_bar_html('🚀 PERFORMANCE', winner['perf_score'], '#3B82F6')}{stat_bar_html('📸 CAMERA', winner['cam_score'], '#A855F7')}{stat_bar_html('🔋 BATTERY', winner['batt_score'], '#10B981')}"
            
            winner_html = f"""<div class='winner-box'><div class='award-badge'>{current_badge}</div><div class='hero-title'>{winner['name']}</div><div class='hero-price'>${winner['price']:,}</div><div class='expert-verdict'>{verdict_html}</div><div class='stat-container'>{stats_html}</div><div class='bench-row'><div class='bench-item'>🚀 AnTuTu: <span>{int(winner['antutu']):,}</span></div><div class='bench-item'>📸 Camera: <span>{int(winner['cam_score'])}/10</span></div></div><a href='{winner['link']}' target='_blank' class='amazon-btn'>🛒 CHECK GLOBAL PRICE</a></div>"""
            st.markdown(winner_html, unsafe_allow_html=True)

        with c2:
            st.markdown("### 🥈 Top Alternatives")
            for i, row in df.iloc[1:6].iterrows():
                diff = winner['price'] - row['price']
                save_html = f"<span class='save-tag'>SAVE ${diff:,}</span>" if diff > 0 else ""
                
                bar1 = f"<div class='mini-stat'><div class='mini-track'><div class='mini-fill-blue' style='width:{row['perf_score']*10}%;'></div></div></div>"
                bar2 = f"<div class='mini-stat'><div class='mini-track'><div class='mini-fill-purple' style='width:{row['cam_score']*10}%;'></div></div></div>"
                bar3 = f"<div class='mini-stat'><div class='mini-track'><div class='mini-fill-green' style='width:{row['batt_score']*10}%;'></div></div></div>"
                mini_bars_html = f"<div class='mini-bar-container'>{bar1}{bar2}{bar3}</div>"
                
                alt_html = f"""
<a href='{row['link']}' target='_blank' class='alt-link'>
    <div class='alt-row'>
        <div>
            <div style='font-weight:bold; font-size:1.1em; color:white;'>{i}. {row['name']}</div>
            <div style='color:#FBBF24; font-weight:bold;'>${row['price']:,} {save_html}</div>
            {mini_bars_html}
            <div style='font-size:0.8em; color:#666; margin-top:6px;'>Match: {row['match']:.1f}%</div>
        </div>
        <div style='text-align:right'>
            <div style='font-size:1.3em; font-weight:900; color:#3B82F6;'>{row['match']:.0f}%</div>
            <div class='buy-hint' style='color:#FBBF24; font-size:0.8em; font-weight:bold; margin-top:5px;'>VIEW ></div>
        </div>
    </div>
</a>
"""
                st.markdown(alt_html, unsafe_allow_html=True)

    else:
        st.warning(f"No devices found under ${budget}. Please adjust your filters.")
else:
    st.error("Database Error.")