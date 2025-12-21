import streamlit as st
import pandas as pd
import textwrap # พระเอกขี่ม้าขาว มาแก้ HTML หลุด

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

# --- 3. WORLD-CLASS CSS (ปรับสีให้อ่านง่ายสุดๆ) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');
    
    /* CORE THEME */
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #222; }
    div[data-baseweb="select"] > div { background-color: #111 !important; color: white !important; border: 1px solid #444 !important; }
    div[data-baseweb="select"] span { color: white !important; }
    
    /* WINNER CARD */
    .winner-box {
        background: radial-gradient(circle at top right, #1a1a2e, #000000);
        border: 1px solid #3B82F6;
        border-radius: 24px; 
        padding: 40px;
        box-shadow: 0 0 80px -20px rgba(59, 130, 246, 0.4);
        position: relative;
    }
    
    .rank-tag {
        background: #F59E0B; color: black; font-weight: 900; 
        padding: 8px 16px; border-radius: 4px; 
        text-transform: uppercase; font-size: 0.8em; letter-spacing: 2px;
    }
    
    .hero-title {
        font-size: 3.8em; font-weight: 900; margin: 20px 0 10px 0; line-height: 1;
        background: -webkit-linear-gradient(#fff, #bbb);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    
    .hero-price { color: #FBBF24; font-size: 2.5em; font-weight: 800; margin-bottom: 25px; }

    /* --- DESCRIPTION BOX (แก้สีจม) --- */
    .desc-box {
        background: rgba(255, 255, 255, 0.08); /* พื้นหลังขาวจางๆ */
        border-left: 4px solid #F59E0B;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 30px;
    }
    .desc-text {
        color: #E2E8F0 !important; /* บังคับสีขาวเกือบสุด */
        font-size: 1.15em;
        line-height: 1.6;
        font-weight: 400;
    }

    /* STAT GRID */
    .stat-container {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 30px;
    }
    .stat-item { background: #111; padding: 15px; border-radius: 12px; border: 1px solid #333; text-align: center; }
    .stat-title { color: #888; font-size: 0.75em; font-weight: 700; letter-spacing: 1px; margin-bottom: 5px; text-transform: uppercase;}
    .stat-num { font-size: 1.8em; font-weight: 900; color: white; }
    .bar-bg { background: #333; height: 6px; border-radius: 3px; margin-top: 10px; overflow: hidden; }
    
    /* BUTTON */
    .amazon-btn {
        background: #F59E0B;
        color: black !important; padding: 18px 0; border-radius: 12px;
        text-decoration: none; font-weight: 800; font-size: 1.2em; display: block; text-align: center;
        transition: transform 0.2s;
    }
    .amazon-btn:hover { transform: scale(1.02); background: #fff; }

    /* ALTERNATIVES */
    .alt-item {
        background: #0A0A0A; border: 1px solid #222;
        padding: 20px; border-radius: 12px; margin-bottom: 12px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .alt-item:hover { border-color: #3B82F6; background: #111; }

</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("💎 TechChoose")
    st.caption("World-Class Algorithm")
    st.write("---")
    os_choice = st.selectbox("📱 Ecosystem", ["Any", "iOS (Apple)", "Android"])
    st.write("")
    lifestyle = st.selectbox("👤 User Persona", ["🎮 Hardcore Gamer", "📸 Content Creator", "💼 Business Pro", "💰 Student / Budget", "🛠️ Custom Manual"])
    st.write("")
    budget = st.slider("💰 Max Budget (USD)", 300, 2000, 2000, step=50)

    # --- 🧠 SMART ALGORITHM ---
    p, c, b, v = 5, 5, 5, 5
    if "Gamer" in lifestyle: p,c,b,v = 10, 3, 8, 4
    elif "Creator" in lifestyle: p,c,b,v = 7, 10, 8, 5
    elif "Business" in lifestyle: p,c,b,v = 8, 6, 9, 6
    elif "Student" in lifestyle: p,c,b,v = 5, 5, 7, 10
    
    # Dynamic Adjustment
    if budget >= 1000: # รวย -> เน้นของดี
        v = 2; p += 2; c += 2
    elif budget <= 600: # ประหยัด -> เน้นคุ้ม
        v = 12

    if "Custom" in lifestyle:
        st.divider()
        p = st.slider("Performance", 1,10,8)
        c = st.slider("Camera", 1,10,8)
        b = st.slider("Battery", 1,10,5)
        v = st.slider("Value", 1,10,5)

    st.divider()
    st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True)

# --- 5. HELPER FUNCTIONS (ใช้ textwrap แก้ HTML หลุด) ---
def get_verdict_html(row, mode):
    verdict = ""
    if "Gamer" in mode: verdict = f"The absolute gaming king. **{row['name']}** destroys benchmarks with elite sustained performance."
    elif "Creator" in mode: verdict = f"Cinematic quality in your hand. **{row['name']}** offers a studio-grade camera system."
    elif "Student" in mode: verdict = f"Unbeatable value. **{row['name']}** delivers flagship specs for a fraction of the price."
    else: verdict = f"The perfect daily driver. **{row['name']}** balances premium build quality, speed, and reliability."
    return verdict

def stat_html(label, score, color):
    # ใช้ dedent ล้างย่อหน้าทิ้ง
    return textwrap.dedent(f"""
        <div class='stat-item'>
            <div class='stat-title'>{label}</div>
            <div class='stat-num'>{score}/10</div>
            <div class='bar-bg'><div style='width:{score*10}%; height:100%; background:{color};'></div></div>
        </div>
    """)

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
        c1, c2 = st.columns([1.5, 1], gap="large")

        with c1:
            # ใช้ textwrap.dedent ครอบ HTML ทั้งก้อน (สำคัญมาก!)
            html_code = textwrap.dedent(f"""
                <div class='winner-box'>
                    <span class='rank-tag'>🏆 #1 Global Pick</span>
                    <div class='hero-title'>{winner['name']}</div>
                    <div class='hero-price'>${winner['price']:,}</div>
                    
                    <div class='desc-box'>
                        <div class='desc-text'>
                            <b>💡 AI Analysis:</b><br>
                            {get_verdict_html(winner, lifestyle)}
                        </div>
                    </div>
                    
                    <div class='stat-container'>
                        {stat_html("🚀 Speed", winner['performance'], "#3B82F6")}
                        {stat_html("📸 Camera", winner['camera'], "#A855F7")}
                        {stat_html("🔋 Battery", winner['battery'], "#10B981")}
                    </div>
                    
                    <a href="{winner['link']}" target="_blank" class="amazon-btn">
                        🛒 CHECK PRICE ON AMAZON
                    </a>
                </div>
            """)
            st.markdown(html_code, unsafe_allow_html=True)

        with c2:
            st.markdown("### 📊 Market Comparison")
            for i, row in df.iloc[1:5].iterrows():
                diff = winner['price'] - row['price']
                save_tag = f"<span style='color:#10B981; font-weight:bold;'>Save ${diff:,}</span>" if diff > 0 else ""
                
                alt_html = textwrap.dedent(f"""
                    <div class='alt-item'>
                        <div>
                            <div style='font-weight:700; font-size:1.1em; color:white;'>{i}. {row['name']}</div>
                            <div style='color:#888;'>${row['price']:,} &nbsp; {save_tag}</div>
                        </div>
                        <div style='color:#3B82F6; font-weight:900; font-size:1.2em;'>{row['match']:.0f}%</div>
                    </div>
                """)
                st.markdown(alt_html, unsafe_allow_html=True)

    else:
        st.warning(f"No smartphones found under ${budget:,}. Try increasing your budget.")
else:
    st.error("Database connection failed.")