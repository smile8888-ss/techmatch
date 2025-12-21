import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - World Class",
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
        return df
    except Exception:
        return pd.DataFrame()

# --- 3. WORLD-CLASS CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');
    
    /* CORE THEME */
    .stApp { background-color: #09090B; color: #E4E4E7; font-family: 'Inter', sans-serif; }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #27272A; }
    div[data-baseweb="select"] > div { background-color: #18181B !important; color: white !important; border: 1px solid #3F3F46 !important; }
    div[data-baseweb="select"] span { color: white !important; }

    /* --- WINNER CARD (PRO DESIGN) --- */
    .winner-box {
        background: linear-gradient(180deg, #18181B 0%, #09090B 100%);
        border: 1px solid #3B82F6;
        border-radius: 24px; 
        padding: 40px;
        box-shadow: 0 0 60px -20px rgba(59, 130, 246, 0.5); /* Neon Glow */
        position: relative;
        overflow: hidden;
    }
    
    .rank-tag {
        background: linear-gradient(90deg, #F59E0B, #FBBF24); color: black; font-weight: 900; 
        padding: 8px 16px; border-radius: 30px; 
        text-transform: uppercase; font-size: 0.8em; letter-spacing: 1.5px;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
    }
    
    .hero-title {
        font-size: 3.5em; font-weight: 900; margin: 25px 0 15px 0; line-height: 1.1;
        background: -webkit-linear-gradient(#ffffff, #A1A1AA);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    
    .hero-price { color: #FBBF24; font-size: 2.5em; font-weight: 800; margin-bottom: 30px; }

    /* --- DESCRIPTION (แก้ให้อ่านง่าย) --- */
    .hero-description {
        font-size: 1.2em; /* ตัวใหญ่ขึ้น */
        line-height: 1.7; /* บรรทัดห่างขึ้น */
        color: #E4E4E7; /* สีขาวนวล อ่านสบายตา */
        font-weight: 500;
        margin-bottom: 35px;
        padding: 20px;
        background: rgba(255,255,255,0.03); /* พื้นหลังจางๆ */
        border-radius: 12px;
        border-left: 4px solid #3B82F6;
    }

    /* --- STAT GRID --- */
    .stat-container {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;
        margin-bottom: 35px;
    }
    .stat-item { background: #18181B; padding: 15px; border-radius: 16px; border: 1px solid #27272A; text-align: center; }
    .stat-title { color: #A1A1AA; font-size: 0.85em; font-weight: 700; letter-spacing: 1px; margin-bottom: 8px; text-transform: uppercase;}
    .stat-num { font-size: 1.8em; font-weight: 900; color: white; }
    .bar-bg { background: #27272A; height: 8px; border-radius: 4px; margin-top: 10px; overflow: hidden; }
    
    /* --- BUTTON --- */
    .amazon-btn {
        background: linear-gradient(90deg, #F59E0B, #D97706);
        color: white !important; padding: 18px 40px; border-radius: 50px;
        text-decoration: none; font-weight: 800; font-size: 1.1em; display: block; text-align: center;
        box-shadow: 0 10px 30px -10px rgba(245, 158, 11, 0.5);
        transition: all 0.3s ease;
    }
    .amazon-btn:hover { transform: translateY(-3px); box-shadow: 0 15px 40px -10px rgba(245, 158, 11, 0.7); }

    /* --- ALTERNATIVES --- */
    .alt-item {
        background: #121217; border: 1px solid #27272A;
        padding: 22px; border-radius: 14px; margin-bottom: 14px;
        display: flex; justify-content: space-between; align-items: center;
        transition: all 0.2s ease;
    }
    .alt-item:hover { border-color: #3B82F6; background: #18181B; transform: translateX(5px); }

</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("💎 TechChoose")
    st.caption("Global AI Advisor")
    st.write("---")
    os_choice = st.selectbox("📱 Ecosystem", ["Any", "iOS (Apple)", "Android"])
    st.write("")
    lifestyle = st.selectbox("👤 User Persona", ["🎮 Hardcore Gamer", "📸 Content Creator", "💼 Business Pro", "💰 Student / Budget", "🛠️ Custom Manual"])
    st.write("")
    budget = st.slider("💰 Max Budget (USD)", 300, 2000, 2000, step=50)

    # Smart Logic
    p, c, b, v = 5, 5, 5, 5
    if "Gamer" in lifestyle: p,c,b,v = 10, 3, 8, 4
    elif "Creator" in lifestyle: p,c,b,v = 7, 10, 8, 5
    elif "Business" in lifestyle: p,c,b,v = 8, 6, 9, 6
    elif "Student" in lifestyle: p,c,b,v = 5, 5, 7, 10
    
    if budget >= 1000:
        v = 2; p += 2; c += 2
    elif budget <= 600:
        v = 12

    if "Custom" in lifestyle:
        st.divider()
        p = st.slider("Performance", 1,10,8)
        c = st.slider("Camera", 1,10,8)
        b = st.slider("Battery", 1,10,5)
        v = st.slider("Value", 1,10,5)

    st.divider()
    st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True)

# --- 5. HELPER FUNCTIONS (CRITICAL FIX: NO INDENTATION) ---
def get_verdict_html(row, mode):
    verdict_text = ""
    if "Gamer" in mode: verdict_text = f"The absolute gaming king. **{row['name']}** destroys benchmarks with elite sustained performance."
    elif "Creator" in mode: verdict_text = f"Cinematic quality in your hand. **{row['name']}** offers a studio-grade camera system for professionals."
    elif "Student" in mode: verdict_text = f"Unbeatable value. **{row['name']}** delivers flagship-level specs for a fraction of the price."
    else: verdict_text = f"The perfect daily driver. **{row['name']}** balances premium build quality, speed, and reliability."
    
    # คืนค่าเป็น HTML ที่จัด format แล้ว
    return f"""<b>🤖 AI Analysis:</b><br>{verdict_text}"""

def stat_html(label, score, color):
    # เขียนชิดซ้ายสุด ป้องกันบั๊ก 100%
    return f"""
<div class='stat-item'>
<div class='stat-title'>{label}</div>
<div class='stat-num'>{score}/10</div>
<div class='bar-bg'><div style='width:{score*10}%; height:100%; background:{color};'></div></div>
</div>
"""

# --- 6. MAIN LOGIC ---
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
        c1, c2 = st.columns([1.4, 1], gap="large")

        with c1:
            # --- THE CRITICAL FIX ---
            # เขียน HTML string แบบชิดซ้ายสุด ไม่มีการเว้นย่อหน้าใน code Python
            # วิธีนี้คือวิธีเดียวที่จะแก้ปัญหา HTML หลุดได้ 100% ในทุก environment
            html_content = f"""
<div class='winner-box'>
<span class='rank-tag'>🏆 #1 World-Class Pick</span>
<div class='hero-title'>{winner['name']}</div>
<div class='hero-price'>${winner['price']:,}</div>
<div class='hero-description'>
{get_verdict_html(winner, lifestyle)}
</div>
<div class='stat-container'>
{stat_html("🚀 Speed", winner['performance'], "#3B82F6")}
{stat_html("📸 Camera", winner['camera'], "#A855F7")}
{stat_html("🔋 Battery", winner['battery'], "#10B981")}
</div>
<a href="{winner['link']}" target="_blank" class="amazon-btn">
🛒 Check Price on Amazon
</a>
</div>
"""
            st.markdown(html_content, unsafe_allow_html=True)

        with c2:
            st.markdown("### 📊 Market Comparison")
            st.caption(f"Top alternatives under ${budget:,}")
            for i, row in df.iloc[1:5].iterrows():
                diff = winner['price'] - row['price']
                save_tag = f"<span style='color:#10B981; font-weight:900; font-size:0.9em;'>Save ${diff:,}</span>" if diff > 0 else ""
                
                # HTML ชิดซ้ายเช่นกัน
                alt_html = f"""
<div class='alt-item'>
<div>
<div style='font-weight:800; font-size:1.2em; color:white; margin-bottom:5px;'>{i}. {row['name']}</div>
<div style='color:#A1A1AA; font-weight:600;'>${row['price']:,} &nbsp; {save_tag}</div>
</div>
<div style='text-align:right;'>
<div style='color:#3B82F6; font-weight:900; font-size:1.4em;'>{row['match']:.0f}%</div>
<a href="{row['link']}" target="_blank" style='color:#F59E0B; text-decoration:none; font-size:0.9em; font-weight:700;'>View Deal ></a>
</div>
</div>
"""
                st.markdown(alt_html, unsafe_allow_html=True)

    else:
        st.warning(f"No smartphones found under ${budget:,}. Try increasing your budget.")
else:
    st.error("Database connection failed.")