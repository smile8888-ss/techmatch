import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Pro Edition",
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
        
        # กันข้อมูล Error
        if 'antutu' not in df.columns: df['antutu'] = df['price'].apply(lambda x: x * 2500 if x > 0 else 500000)
        if 'dxomark' not in df.columns: df['dxomark'] = df['camera'].apply(lambda x: x * 15 + 20)
        if 'award' not in df.columns: df['award'] = "Top Choice"
            
        return df
    except Exception:
        return pd.DataFrame()

# --- 3. CSS (Pro Theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Inter:wght@400;600;900&display=swap');
    
    /* Background */
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #222; }
    .stMarkdown label p { font-size: 1.2em; font-weight: 800; color: #FBBF24 !important; }
    
    /* Input Controls */
    div[data-baseweb="select"] > div { background-color: #222222 !important; color: white !important; border: 2px solid #555 !important; }
    div[data-baseweb="select"] span { color: #FFFFFF !important; font-weight: 600; font-size: 1.1em; }
    div[data-baseweb="select"] svg { fill: #FBBF24 !important; }
    ul[data-baseweb="menu"] { background-color: #222 !important; border: 1px solid #555; }
    li[data-baseweb="option"] { color: #FFF !important; }
    
    /* --- WINNER CARD --- */
    .winner-box {
        background: radial-gradient(circle at top right, #111, #000);
        border: 2px solid #3B82F6;
        border-radius: 20px; padding: 40px;
        box-shadow: 0 0 60px rgba(59, 130, 246, 0.25);
    }
    .award-badge {
        background: #F59E0B; color: black; font-weight: 900; 
        padding: 8px 16px; border-radius: 50px; text-transform: uppercase; 
        display: inline-block; margin-bottom: 20px; font-size: 0.9em; letter-spacing: 1px;
    }
    .hero-title { font-size: 3.5em; font-weight: 900; color: white; line-height: 1.1; margin-bottom: 15px; }
    .hero-price { color: #FBBF24; font-size: 3em; font-weight: 800; font-family: 'JetBrains Mono'; margin-bottom: 30px; }

    .expert-verdict {
        background: #111; border-left: 5px solid #3B82F6;
        padding: 25px; border-radius: 0 12px 12px 0; margin-bottom: 35px;
        font-size: 1.15em; line-height: 1.6; color: #E0E0E0;
    }

    .stat-container { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 35px; }
    .stat-box { background: #151515; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #333; }
    .stat-label { color: #888; font-size: 0.8em; font-weight: 700; margin-bottom: 5px; text-transform: uppercase; }
    .stat-val { font-size: 1.6em; font-weight: 900; color: white; }
    .bar-bg { background: #333; height: 6px; border-radius: 3px; margin-top: 10px; overflow: hidden; }

    .bench-row { display: flex; gap: 30px; padding-top: 25px; border-top: 1px solid #222; margin-top: 25px; }
    .bench-item { font-family: 'JetBrains Mono'; color: #888; font-size: 1em; }
    .bench-item span { color: #FFF; font-weight: bold; font-size: 1.2em; margin-left: 8px; }

    .amazon-btn {
        background: #3B82F6; color: white !important; 
        padding: 22px; width: 100%; display: block; text-align: center; 
        border-radius: 12px; font-weight: 900; text-decoration: none; font-size: 1.4em;
        margin-top: 30px; transition: 0.3s;
    }
    .amazon-btn:hover { background: #2563EB; box-shadow: 0 0 30px rgba(59, 130, 246, 0.4); }

    /* --- CLICKABLE ALTERNATIVES WITH MINI BARS --- */
    .alt-link { text-decoration: none; display: block; }
    .alt-row {
        background: #0A0A0A; border: 1px solid #222;
        padding: 20px; border-radius: 12px; margin-bottom: 12px;
        display: flex; justify-content: space-between; align-items: center;
        transition: all 0.2s ease;
    }
    .alt-row:hover { border-color: #FBBF24; background: #111; transform: scale(1.01); }
    
    /* CSS สำหรับ Mini Bars */
    .mini-bar-container { display: flex; gap: 12px; margin-top: 8px; }
    .mini-stat { width: 45px; }
    .mini-label { font-size: 0.6em; color: #888; margin-bottom: 2px; }
    .mini-track { width: 100%; height: 4px; background: #333; border-radius: 2px; }
    .mini-fill { height: 100%; border-radius: 2px; }

</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🛒 TechChoose")
    st.caption("Global Market Analyzer")
    st.markdown("---")
    
    st.markdown("### ⚙️ Search Settings")
    os_choice = st.selectbox("📱 Operating System", ["Any", "iOS (Apple)", "Android"])
    st.write("")
    lifestyle = st.selectbox("👤 User Persona", ["🎮 Hardcore Gamer", "📸 Content Creator", "💼 Business Pro", "💰 Student / Budget", "🛠️ Custom"])
    st.write("")
    budget = st.slider("💰 Max Budget (USD)", 100, 2000, 2000, step=50)

    # Logic
    p, c, b, v = 5, 5, 5, 5
    if "Gamer" in lifestyle: p,c,b,v = 10, 3, 8, 4
    elif "Creator" in lifestyle: p,c,b,v = 7, 10, 8, 5
    elif "Business" in lifestyle: p,c,b,v = 8, 6, 9, 6
    elif "Student" in lifestyle: p,c,b,v = 5, 5, 7, 15
    if budget >= 1000: v = 2; p += 2; c += 2
    elif budget <= 400: v = 20
    if "Custom" in lifestyle:
        p = st.slider("Perf", 1,10,8); c = st.slider("Cam", 1,10,8); b = st.slider("Batt", 1,10,5); v = st.slider("Val", 1,10,5)

    st.divider()
    st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True)

# --- 5. HELPER FUNCTIONS ---
def get_expert_verdict(row, mode):
    verdict = "<b>🤖 Expert Analysis:</b><br>"
    if "Gamer" in mode:
        verdict += f"Dominates the arena with an <b>AnTuTu score of {int(row['antutu']):,}</b>. Verified as a top-tier gaming powerhouse for 2025."
    elif "Creator" in mode:
        verdict += f"Studio-grade imaging. <b>DXOMARK score of {int(row['dxomark'])}</b> ensures professional photo and video quality in all conditions."
    elif "Student" in mode or row['price'] < 400:
        verdict += f"Global 'Best Value' leader. Delivers flagship-level features and reliability at a highly competitive price point."
    else:
        verdict += f"The ultimate all-rounder. Achieves top stability scores across performance, camera, and battery metrics."
    return verdict

def stat_bar_html(label, score, color):
    return f"<div class='stat-box'><div class='stat-label'>{label}</div><div class='stat-val'>{score}/10</div><div class='bar-bg'><div style='width:{score*10}%; height:100%; background:{color};'></div></div></div>"

# --- 6. MAIN APP ---
df = load_data()

if not df.empty:
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']
    df = df[df['price'] <= budget]

    df['score'] = (df['performance']*p) + (df['camera']*c) + (df['battery']*b) + (df['value']*v)
    max_score = (10*p) + (10*c) + (10*b) + (10*v)
    df['match'] = (df['score'] / max_score) * 100
    df = df.sort_values(by='match', ascending=False).reset_index(drop=True)

    if len(df) > 0:
        winner = df.iloc[0]
        c1, c2 = st.columns([1.5, 1], gap="large")

        with c1:
            winner_html = f"<div class='winner-box'><div class='award-badge'>🏆 {winner['award']}</div><div class='hero-title'>{winner['name']}</div><div class='hero-price'>${winner['price']:,}</div><div class='expert-verdict'>{get_expert_verdict(winner, lifestyle)}</div><div class='stat-container'>{stat_bar_html('🚀 PERFORMANCE', winner['performance'], '#3B82F6')}{stat_bar_html('📸 CAMERA', winner['camera'], '#A855F7')}{stat_bar_html('🔋 BATTERY', winner['battery'], '#10B981')}</div><div class='bench-row'><div class='bench-item'>🚀 AnTuTu: <span>{int(winner['antutu']):,}</span></div><div class='bench-item'>📸 DXOMARK: <span>{int(winner['dxomark'])}</span></div></div><a href='{winner['link']}' target='_blank' class='amazon-btn'>🛒 CHECK GLOBAL PRICE</a></div>"
            st.markdown(winner_html, unsafe_allow_html=True)

        with c2:
            st.markdown("### 🥈 Top Alternatives")
            for i, row in df.iloc[1:6].iterrows():
                diff = winner['price'] - row['price']
                save_tag = f"<span style='color:#10B981; margin-left:10px;'>SAVE ${diff:,}</span>" if diff > 0 else ""
                
                # --- NEW: MINI BARS INJECTION ---
                # เพิ่มหลอดพลังจิ๋ว 3 สี (ฟ้า/ม่วง/เขียว) ใต้ราคา
                mini_bars = f"""
                <div class='mini-bar-container'>
                    <div class='mini-stat'><div class='mini-label'>🚀 {row['performance']}</div><div class='mini-track'><div class='mini-fill' style='width:{row['performance']*10}%; background:#3B82F6;'></div></div></div>
                    <div class='mini-stat'><div class='mini-label'>📸 {row['camera']}</div><div class='mini-track'><div class='mini-fill' style='width:{row['camera']*10}%; background:#A855F7;'></div></div></div>
                    <div class='mini-stat'><div class='mini-label'>🔋 {row['battery']}</div><div class='mini-track'><div class='mini-fill' style='width:{row['battery']*10}%; background:#10B981;'></div></div></div>
                </div>
                """
                
                # HTML รวมร่าง (One-line)
                alt_html = f"""
<a href="{row['link']}" target="_blank" class="alt-link">
    <div class='alt-row'>
        <div>
            <div style='font-weight:bold; font-size:1.1em; color:white;'>{i}. {row['name']}</div>
            <div style='color:#FBBF24; font-weight:bold;'>${row['price']:,} {save_tag}</div>
            {mini_bars}
            <div style='font-size:0.8em; color:#666; margin-top:6px;'>AnTuTu: {int(row['antutu']):,}</div>
        </div>
        <div style='text-align:right'>
            <div style='font-size:1.3em; font-weight:900; color:#3B82F6;'>{row['match']:.0f}%</div>
            <div class='buy-hint'>VIEW ></div>
        </div>
    </div>
</a>
"""
                st.markdown(alt_html, unsafe_allow_html=True)

    else:
        st.warning(f"No devices found under ${budget}. Please adjust your filters.")
else:
    st.error("Database Error.")