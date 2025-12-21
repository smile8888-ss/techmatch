import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Masterpiece",
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
        
        # Auto-fill missing data
        if 'antutu' not in df.columns: df['antutu'] = df['price'].apply(lambda x: x * 2500 if x > 0 else 500000)
        if 'dxomark' not in df.columns: df['dxomark'] = df['camera'].apply(lambda x: x * 15 + 20)
        if 'award' not in df.columns: df['award'] = "Top Choice"
            
        return df
    except Exception:
        return pd.DataFrame()

# --- 3. CSS (PREMIUM BRANDING THEME) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Inter:wght@400;600;900&display=swap');
    
    /* Background */
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] { background-color: #080808; border-right: 1px solid #222; }
    .stMarkdown label p { font-size: 1.1em; font-weight: 800; color: #FBBF24 !important; letter-spacing: 0.5px; }
    
    /* High Contrast Controls */
    div[data-baseweb="select"] > div { background-color: #1A1A1A !important; color: white !important; border: 1px solid #444 !important; }
    div[data-baseweb="select"] span { color: white !important; font-weight:600; }
    ul[data-baseweb="menu"] { background-color: #1A1A1A !important; }
    li[data-baseweb="option"] { color: #FFF !important; }
    
    /* --- WINNER CARD (GLOW EFFECT) --- */
    .winner-box {
        background: linear-gradient(145deg, #111 0%, #000 100%);
        border: 1px solid #333;
        border-top: 4px solid #3B82F6;
        border-radius: 24px; padding: 40px;
        box-shadow: 0 0 80px rgba(59, 130, 246, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    /* Dynamic Brand Badges */
    .brand-badge {
        font-size: 0.75em; font-weight: 900; text-transform: uppercase; letter-spacing: 1.5px;
        padding: 6px 14px; border-radius: 6px; display: inline-block; margin-bottom: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .hero-title { font-size: 3.8em; font-weight: 900; color: white; line-height: 1.05; margin-bottom: 15px; letter-spacing: -1px; }
    .hero-price { color: #FBBF24; font-size: 3.2em; font-weight: 800; font-family: 'JetBrains Mono'; margin-bottom: 30px; }

    /* Stats & Benchmarks */
    .stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 30px; }
    .stat-pill { background: #151515; padding: 12px; border-radius: 12px; text-align: center; border: 1px solid #252525; }
    .stat-val { font-size: 1.4em; font-weight: 900; color: white; }
    .stat-lbl { font-size: 0.7em; color: #777; font-weight: 700; text-transform: uppercase; margin-top: 5px; }
    
    .bench-box { 
        display: flex; justify-content: space-around; background: #0F0F0F; 
        padding: 20px; border-radius: 12px; border: 1px dashed #333; margin-top: 25px;
    }
    .bench-val { font-family: 'JetBrains Mono'; font-size: 1.1em; color: #AAA; }
    .bench-val span { color: #FFF; font-weight: bold; font-size: 1.2em; }

    /* Verdict */
    .verdict-text { 
        font-size: 1.1em; line-height: 1.6; color: #D4D4D8; 
        background: rgba(59, 130, 246, 0.05); padding: 20px; border-radius: 12px; border-left: 3px solid #3B82F6;
    }

    /* Button */
    .amazon-btn {
        background: linear-gradient(90deg, #3B82F6, #2563EB); color: white !important; 
        padding: 22px; width: 100%; display: block; text-align: center; 
        border-radius: 16px; font-weight: 800; text-decoration: none; font-size: 1.3em;
        margin-top: 35px; transition: 0.3s; box-shadow: 0 10px 30px -10px rgba(37, 99, 235, 0.5);
    }
    .amazon-btn:hover { transform: translateY(-2px); box-shadow: 0 15px 40px -10px rgba(37, 99, 235, 0.7); }

    /* Alternatives */
    .alt-link { text-decoration: none; display: block; }
    .alt-card {
        background: #0A0A0A; border: 1px solid #222;
        padding: 20px; border-radius: 14px; margin-bottom: 12px;
        display: flex; justify-content: space-between; align-items: center;
        transition: all 0.2s ease;
    }
    .alt-card:hover { border-color: #F59E0B; background: #111; transform: scale(1.01); }
    .save-badge { background: #064E3B; color: #34D399; font-size: 0.7em; font-weight: 800; padding: 3px 8px; border-radius: 4px; margin-left: 8px; }

</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🛒 TechChoose")
    st.caption("AI Market Analytics")
    st.markdown("---")
    
    st.markdown("### ⚙️ Search Filters")
    os_choice = st.selectbox("📱 Ecosystem", ["Any", "iOS (Apple)", "Android"])
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
def get_brand_style(name):
    # ฟังก์ชันสร้างป้ายแบรนด์ (The Secret Sauce 🌶️)
    name_lower = name.lower()
    if "samsung" in name_lower: return "background:#0045B5; color:white;", "SAMSUNG"
    elif "iphone" in name_lower: return "background:#333333; color:white;", "APPLE"
    elif "xiaomi" in name_lower or "redmi" in name_lower or "poco" in name_lower: return "background:#FF6900; color:white;", "XIAOMI"
    elif "pixel" in name_lower: return "background:linear-gradient(90deg, #4285F4, #EA4335, #FBBC04, #34A853); color:white;", "GOOGLE"
    elif "oneplus" in name_lower: return "background:#F50514; color:white;", "ONEPLUS"
    elif "rog" in name_lower or "redmagic" in name_lower: return "background:#D50000; color:white;", "GAMING"
    else: return "background:#555; color:white;", "SMARTPHONE"

def get_verdict(row, mode):
    verdict = ""
    if "Gamer" in mode: verdict = f"Engineered for dominance. The **{row['name']}** crushes AAA titles with an AnTuTu score of {int(row['antutu']):,}."
    elif "Creator" in mode: verdict = f"Cinematic mastery. **{row['name']}** achieves a DXOMARK rating of {int(row['dxomark'])}, perfect for pro-level content."
    elif "Student" in mode or row['price'] < 400: verdict = f"Value champion. **{row['name']}** delivers premium features and reliability at an unbeatable price point."
    else: verdict = f"The ultimate daily driver. **{row['name']}** offers a perfect balance of performance, build quality, and battery life."
    return verdict

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

        # Get Brand Badge Style
        b_style, b_name = get_brand_style(winner['name'])

        with c1:
            # HTML (One-Line for Safety)
            winner_html = f"<div class='winner-box'><div class='brand-badge' style='{b_style}'>{b_name}</div><div style='float:right; color:#F59E0B; font-weight:900;'>🏆 {winner['award']}</div><div style='clear:both'></div><div class='hero-title'>{winner['name']}</div><div class='hero-price'>${winner['price']:,}</div><div class='verdict-text'><b>💡 AI Analysis:</b> {get_verdict(winner, lifestyle)}</div><div style='margin-top:25px'></div><div class='stat-grid'><div class='stat-pill'><div class='stat-val'>{winner['performance']}/10</div><div class='stat-lbl'>Speed</div></div><div class='stat-pill'><div class='stat-val'>{winner['camera']}/10</div><div class='stat-lbl'>Camera</div></div><div class='stat-pill'><div class='stat-val'>{winner['battery']}/10</div><div class='stat-lbl'>Battery</div></div></div><div class='bench-box'><div class='bench-val'>AnTuTu: <span>{int(winner['antutu']):,}</span></div><div class='bench-val'>DXOMARK: <span>{int(winner['dxomark'])}</span></div></div><a href='{winner['link']}' target='_blank' class='amazon-btn'>🛒 CHECK LIVE PRICE</a></div>"
            st.markdown(winner_html, unsafe_allow_html=True)

        with c2:
            st.markdown("### 🥈 Best Alternatives")
            st.caption("Click any card to view details on Amazon")
            for i, row in df.iloc[1:6].iterrows():
                diff = winner['price'] - row['price']
                save_tag = f"<span class='save-badge'>SAVE ${diff:,}</span>" if diff > 0 else ""
                
                # Alternatives with Link
                alt_html = f"<a href='{row['link']}' target='_blank' class='alt-link'><div class='alt-card'><div><div style='font-weight:700; font-size:1.1em; color:white;'>{i}. {row['name']} {save_tag}</div><div style='color:#666; font-size:0.9em; margin-top:4px;'>AnTuTu: {int(row['antutu']):,}</div></div><div style='text-align:right'><div style='color:#FBBF24; font-weight:800; font-size:1.1em;'>${row['price']:,}</div><div style='color:#3B82F6; font-weight:900; font-size:0.8em;'>{row['match']:.0f}% Match</div></div></div></a>"
                st.markdown(alt_html, unsafe_allow_html=True)

    else:
        st.warning(f"No devices found under ${budget}.")
else:
    st.error("Connection Error.")