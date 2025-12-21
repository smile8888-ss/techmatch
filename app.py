import streamlit as st
import pandas as pd
import textwrap

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Market Master",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    # ลิงก์ Google Sheet ของพี่
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        
        # กันเหนียว: ถ้าลืมใส่คอลัมน์ไหนมา ให้เติมค่า 0 อัตโนมัติ แอปจะได้ไม่พัง
        if 'antutu' not in df.columns: df['antutu'] = 0
        if 'dxomark' not in df.columns: df['dxomark'] = 0
        if 'award' not in df.columns: df['award'] = "Top Choice"
            
        return df
    except Exception:
        return pd.DataFrame()

# --- 3. CSS (Real Market Theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;900&display=swap');
    
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #1A1A1A; }
    div[data-baseweb="select"] > div { background-color: #111 !important; color: white !important; border: 1px solid #333 !important; }
    div[data-baseweb="select"] span { color: white !important; }
    
    /* Winner Box */
    .winner-box {
        background: linear-gradient(160deg, #0F0F0F, #050505);
        border: 1px solid #3B82F6; border-top: 4px solid #3B82F6;
        border-radius: 16px; padding: 35px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }
    
    .award-badge {
        display: inline-block;
        background: rgba(59, 130, 246, 0.1); color: #3B82F6;
        border: 1px solid #3B82F6;
        padding: 6px 14px; border-radius: 50px;
        font-size: 0.8em; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;
        margin-bottom: 20px;
    }
    
    .hero-title { font-size: 3em; font-weight: 900; margin: 0 0 10px 0; line-height: 1.1; letter-spacing: -1px; }
    .hero-price { color: #FBBF24; font-size: 2.5em; font-weight: 800; font-family: 'JetBrains Mono', monospace; }

    /* Benchmark Grid */
    .benchmark-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 15px;
        margin: 30px 0;
        background: #0A0A0A; padding: 20px; border-radius: 12px; border: 1px solid #222;
    }
    .bench-item { text-align: left; }
    .bench-label { color: #666; font-size: 0.75em; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; }
    .bench-score { color: #fff; font-size: 1.6em; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
    .bench-sub { color: #444; font-size: 0.8em; }

    /* Verdict Box */
    .verdict-box {
        background: #111; border-left: 3px solid #10B981;
        padding: 15px 20px; border-radius: 0 8px 8px 0;
        margin-bottom: 25px; color: #ccc; line-height: 1.6;
    }

    /* Button */
    .amazon-btn {
        background: #fff; color: black !important; padding: 16px 0; border-radius: 8px;
        text-decoration: none; font-weight: 800; font-size: 1.1em; display: block; text-align: center;
        transition: 0.2s;
    }
    .amazon-btn:hover { background: #F59E0B; }

    /* Alternatives */
    .alt-item {
        background: #0A0A0A; border-bottom: 1px solid #222;
        padding: 15px; display: flex; justify-content: space-between; align-items: center;
    }
    .alt-item:hover { background: #111; }

</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🛒 TechChoose")
    st.caption("Amazon Market Analysis")
    st.write("---")
    os_choice = st.selectbox("System", ["Any", "iOS", "Android"])
    st.write("")
    lifestyle = st.selectbox("Usage Type", ["🎮 Hardcore Gamer", "📸 Content Creator", "💼 Business Pro", "💰 Student / Budget", "🛠️ Custom"])
    st.write("")
    
    # 🔥 แก้ตรงนี้ครับ: เริ่มต้นที่ $100 (เพื่อให้เจอของถูก)
    budget = st.slider("Max Budget ($)", 100, 2000, 2000, step=50)

    # --- 🧠 REAL WORLD LOGIC ---
    p, c, b, v = 5, 5, 5, 5
    if "Gamer" in lifestyle: p,c,b,v = 10, 3, 8, 4
    elif "Creator" in lifestyle: p,c,b,v = 7, 10, 8, 5
    elif "Business" in lifestyle: p,c,b,v = 8, 6, 9, 6
    elif "Student" in lifestyle: p,c,b,v = 5, 5, 7, 10
    
    # ปรับสูตรตามงบ (Smart Budgeting)
    if budget >= 1000: 
        v = 2; p += 2; c += 2 # งบเยอะ เน้นของดี
    elif budget <= 400: 
        v = 15 # งบน้อย ความคุ้มค่าคือพระเจ้า (ดันพวก Renewed/Budget ขึ้นมา)

    if "Custom" in lifestyle:
        st.divider()
        p = st.slider("Perf", 1,10,8); c = st.slider("Cam", 1,10,8); b = st.slider("Batt", 1,10,5); v = st.slider("Val", 1,10,5)

    st.divider()
    st.button("FIND BEST DEAL", type="primary", use_container_width=True)

# --- 5. FUNCTIONS ---
def get_verdict(row, mode):
    # ปรับคำพูดให้เข้ากับสินค้าหลากหลายประเภท
    if "Renewed" in row['name']:
        return f"💎 **Smart Choice:** Why pay full price? This **{row['name']}** offers flagship experience for a fraction of the cost."
    elif "Gamer" in mode:
        return f"🚀 **Gaming Pick:** With an AnTuTu score of **{int(row['antutu']):,}**, this device punches way above its price class."
    elif "Creator" in mode:
        return f"📸 **Creator Pick:** High DXOMARK score of **{int(row['dxomark'])}** ensures quality content creation."
    elif row['price'] < 300:
        return f"💰 **Budget King:** Incredible value. You get reliable performance and all-day battery without breaking the bank."
    else:
        return f"🏆 **Top Balanced:** Excellent all-rounder with strong benchmark scores across the board."

# --- 6. MAIN LOGIC ---
df = load_data()

if not df.empty:
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']
    df = df[df['price'] <= budget]

    # คำนวณคะแนน
    df['score'] = (df['performance']*p) + (df['camera']*c) + (df['battery']*b) + (df['value']*v)
    max_score = (10*p) + (10*c) + (10*b) + (10*v)
    df['match'] = (df['score'] / max_score) * 100
    df = df.sort_values(by='match', ascending=False).reset_index(drop=True)

    if len(df) > 0:
        winner = df.iloc[0]
        c1, c2 = st.columns([1.4, 1], gap="large")

        with c1:
            # ใช้ textwrap ป้องกัน HTML หลุด 100%
            html = textwrap.dedent(f"""
                <div class='winner-box'>
                    <div class='award-badge'>{winner['award']}</div>
                    <div class='hero-title'>{winner['name']}</div>
                    <div class='hero-price'>${winner['price']:,}</div>
                    
                    <div class='benchmark-grid'>
                        <div class='bench-item'>
                            <div class='bench-label'>🚀 AnTuTu Score</div>
                            <div class='bench-score' style='color:#3B82F6;'>{int(winner['antutu']):,}</div>
                            <div class='bench-sub'>Raw Performance</div>
                        </div>
                        <div class='bench-item'>
                            <div class='bench-label'>📸 DXOMARK</div>
                            <div class='bench-score' style='color:#A855F7;'>{int(winner['dxomark'])}</div>
                            <div class='bench-sub'>Camera Quality</div>
                        </div>
                    </div>

                    <div class='verdict-box'>
                        {get_verdict(winner, lifestyle)}
                    </div>
                    
                    <a href="{winner['link']}" target="_blank" class="amazon-btn">
                        CHECK AMAZON PRICE >
                    </a>
                </div>
            """)
            st.markdown(html, unsafe_allow_html=True)

        with c2:
            st.markdown("### 📉 Best Alternatives")
            for i, row in df.iloc[1:6].iterrows():
                diff = winner['price'] - row['price']
                save_tag = f"<span style='color:#10B981; font-weight:bold; font-size:0.8em;'>SAVE ${diff:,}</span>" if diff > 0 else ""
                
                alt_html = textwrap.dedent(f"""
                    <div class='alt-item'>
                        <div>
                            <div style='font-weight:700; font-size:1.1em; color:white;'>{i}. {row['name']}</div>
                            <div style='color:#888; font-family:"JetBrains Mono"; font-size:0.9em;'>
                                AnTuTu: {int(row['antutu']):,} | ${row['price']:,}
                            </div>
                        </div>
                        <div style='text-align:right;'>
                            <div style='color:#3B82F6; font-weight:900; font-size:1.2em;'>{row['match']:.0f}%</div>
                            <div>{save_tag}</div>
                        </div>
                    </div>
                """)
                st.markdown(alt_html, unsafe_allow_html=True)

    else:
        st.warning(f"No smartphones found under ${budget:,}. Try increasing the budget.")
else:
    st.error("Cannot connect to Database.")