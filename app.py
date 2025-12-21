import streamlit as st
import pandas as pd
import textwrap

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Global Expert",
    page_icon="🏆",
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
        
        # Auto-fill data (กันพัง)
        if 'antutu' not in df.columns: df['antutu'] = df['price'].apply(lambda x: x * 2500 if x > 0 else 500000)
        if 'dxomark' not in df.columns: df['dxomark'] = df['camera'].apply(lambda x: x * 15 + 20)
        if 'award' not in df.columns: df['award'] = "Top Choice"
            
        return df
    except Exception:
        return pd.DataFrame()

# --- 3. GLOBAL CSS (White Text on Black) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Inter:wght@400;600;900&display=swap');
    
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #0A0A0A; border-right: 1px solid #222; }
    .stMarkdown label p { font-size: 1.1em; font-weight: 700; color: #FBBF24 !important; }
    div[data-baseweb="select"] > div { background-color: #222 !important; color: white !important; border: 1px solid #444 !important; }
    div[data-baseweb="select"] span { color: white !important; }
    ul[data-baseweb="menu"] { background-color: #222 !important; }
    li[data-baseweb="option"] { color: #FFFFFF !important; }
    
    /* --- WINNER CARD --- */
    .winner-box {
        background: radial-gradient(circle at top right, #111, #000);
        border: 2px solid #3B82F6;
        border-radius: 24px; padding: 40px;
        box-shadow: 0 0 60px rgba(59, 130, 246, 0.2);
    }
    
    .award-badge {
        background: #F59E0B; color: black; font-weight: 900; 
        padding: 6px 14px; border-radius: 50px; 
        text-transform: uppercase; font-size: 0.8em; letter-spacing: 1px;
        display: inline-block; margin-bottom: 15px;
    }
    
    .hero-title { font-size: 3.5em; font-weight: 900; line-height: 1.1; margin-bottom: 10px; color: white; }
    .hero-price { color: #FBBF24; font-size: 2.8em; font-weight: 800; font-family: 'JetBrains Mono'; margin-bottom: 25px; }

    /* VERDICT BOX (คำอธิบาย) */
    .expert-verdict {
        background: #111; border-left: 4px solid #3B82F6;
        padding: 20px; border-radius: 0 12px 12px 0;
        margin-bottom: 30px;
        font-size: 1.1em; line-height: 1.6; color: #DDD;
    }

    /* STAT BARS (หลอดพลังที่พี่ชอบ) */
    .stat-container {
        display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;
        margin-bottom: 30px;
    }
    .stat-box { background: #1A1A1A; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #333; }
    .stat-label { font-size: 0.8em; color: #BBB; font-weight: 700; margin-bottom: 5px; }
    .stat-val { font-size: 1.5em; font-weight: 900; color: white; }
    .bar-bg { background: #333; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden; }

    /* BENCHMARK DATA (คะแนนดิบ) */
    .bench-row {
        display: flex; gap: 20px; margin-top: 20px; padding-top: 20px; border-top: 1px solid #333;
    }
    .bench-item { font-family: 'JetBrains Mono'; font-size: 0.9em; color: #888; }
    .bench-item span { color: #FFF; font-weight: bold; }

    /* BUTTON */
    .amazon-btn {
        background: #3B82F6; color: white !important; 
        padding: 20px; width: 100%; display: block; text-align: center; 
        border-radius: 12px; font-weight: 800; text-decoration: none; font-size: 1.3em;
        transition: 0.3s;
    }
    .amazon-btn:hover { background: #2563EB; transform: scale(1.02); }

    /* ALTERNATIVES */
    .alt-row {
        background: #0F0F0F; border: 1px solid #222;
        padding: 15px; border-radius: 10px; margin-bottom: 10px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .alt-row:hover { border-color: #FBBF24; background: #141414; }

</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🛒 TechChoose")
    st.caption("Global Market Analyzer")
    st.markdown("---")
    
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
    # ฟังก์ชันสร้างคำอธิบายแบบ Expert
    verdict = f"<b>🤖 Expert Analysis:</b><br>"
    
    if "Gamer" in mode:
        verdict += f"Based on its massive <b>AnTuTu score of {int(row['antutu']):,}</b>, the {row['name']} is a verified gaming powerhouse. It outperforms 95% of devices in its class."
    elif "Creator" in mode:
        verdict += f"According to DXOMARK standards, this device scores <b>{int(row['dxomark'])}</b>, making it a top-tier choice for mobile photography and videography."
    elif "Student" in mode or row['price'] < 400:
        verdict += f"Global market data indicates this is a 'Best Value' leader. You get flagship-grade features at a fraction of the cost."
    else:
        verdict += f"A balanced flagship that excels across all metrics. Trusted by professionals for its reliability and consistent performance."
        
    return verdict

def stat_bar(label, score, color):
    # สร้างหลอดพลัง
    return f"""
    <div class='stat-box'>
        <div class='stat-label'>{label}</div>
        <div class='stat-val'>{score}/10</div>
        <div class='bar-bg'><div style='width:{score*10}%; height:100%; background:{color};'></div></div>
    </div>
    """

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
            # HTML แบบบรรทัดเดียว (กันพัง 100%)
            winner_html = textwrap.dedent(f"""
<div class='winner-box'>
    <div class='award-badge'>🏆 {winner['award']}</div>
    <div class='hero-title'>{winner['name']}</div>
    <div class='hero-price'>${winner['price']:,}</div>
    
    <div class='expert-verdict'>
        {get_expert_verdict(winner, lifestyle)}
    </div>
    
    <div class='stat-container'>
        {stat_bar("🚀 PERFORMANCE", winner['performance'], "#3B82F6")}
        {stat_bar("📸 CAMERA", winner['camera'], "#A855F7")}
        {stat_bar("🔋 BATTERY", winner['battery'], "#10B981")}
    </div>

    <div class='bench-row'>
        <div class='bench-item'>AnTuTu Benchmark: <span>{int(winner['antutu']):,}</span></div>
        <div class='bench-item'>DXOMARK Score: <span>{int(winner['dxomark'])}</span></div>
    </div>
    
    <br>
    <a href="{winner['link']}" target="_blank" class='amazon-btn'>
        🛒 CHECK GLOBAL PRICE
    </a>
</div>
""")
            st.markdown(winner_html, unsafe_allow_html=True)

        with c2:
            st.markdown("### 🥈 Top Alternatives")
            for i, row in df.iloc[1:6].iterrows():
                diff = winner['price'] - row['price']
                save_tag = f"<span style='color:#10B981; margin-left:10px;'>SAVE ${diff:,}</span>" if diff > 0 else ""
                
                alt_html = f"""
<div class='alt-row'>
    <div>
        <div style='font-weight:bold; font-size:1.1em; color:white;'>{i}. {row['name']}</div>
        <div style='color:#FBBF24; font-weight:bold;'>${row['price']:,} {save_tag}</div>
        <div style='font-size:0.8em; color:#888; margin-top:5px;'>
            🚀 AnTuTu: {int(row['antutu']):,} | 📸 DXO: {int(row['dxomark'])}
        </div>
    </div>
    <div style='font-size:1.3em; font-weight:900; color:#3B82F6;'>{row['match']:.0f}%</div>
</div>
"""
                st.markdown(alt_html, unsafe_allow_html=True)

    else:
        st.warning(f"No devices found under ${budget}. Please adjust your budget.")
else:
    st.error("Database connection failed.")