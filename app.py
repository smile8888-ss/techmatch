import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Global Standard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    # ลิงก์ Google Sheet เดิมของพี่
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        # สร้างคอลัมน์ os_type อัตโนมัติ
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        return df
    except Exception:
        return pd.DataFrame()

# --- 3. PRO CSS (Black & Neon Theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* พื้นหลังหลัก */
    .stApp { background-color: #0B0E14; color: #E2E8F0; font-family: 'Inter', sans-serif; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #1A1A1A; }
    
    /* แก้ไข Input ให้ชัดเจน (พื้นหลังเข้ม ตัวหนังสือขาว) */
    div[data-baseweb="select"] > div { background-color: #151515 !important; color: white !important; border: 1px solid #333 !important; }
    div[data-baseweb="select"] span { color: white !important; }
    
    /* --- WINNER CARD DESIGN --- */
    .winner-box {
        background: linear-gradient(180deg, #111827 0%, #0B0E14 100%);
        border: 2px solid #3B82F6; 
        border-radius: 24px; 
        padding: 40px;
        box-shadow: 0 0 50px rgba(59, 130, 246, 0.15);
        position: relative;
    }
    
    .rank-tag {
        background: #F59E0B; color: black; font-weight: 900; 
        padding: 6px 14px; border-radius: 20px; 
        text-transform: uppercase; font-size: 0.75em; letter-spacing: 1px;
    }
    
    .hero-title {
        font-size: 3.2em; font-weight: 900; margin: 15px 0; line-height: 1.1;
        background: -webkit-linear-gradient(#fff, #9CA3AF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    
    .hero-price { color: #FBBF24; font-size: 2.2em; font-weight: 800; margin-bottom: 30px; }

    /* --- STAT GRID (ตารางค่าพลัง) --- */
    .stat-container {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;
        background: #1F2937; padding: 20px; border-radius: 16px; border: 1px solid #374151;
    }
    .stat-item { text-align: center; }
    .stat-title { color: #9CA3AF; font-size: 0.8em; font-weight: 700; letter-spacing: 1px; margin-bottom: 5px; text-transform: uppercase;}
    .stat-num { font-size: 1.5em; font-weight: 800; color: white; }
    .bar-bg { background: #374151; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden; }
    
    /* --- ALTERNATIVES --- */
    .alt-item {
        background: #111827; border: 1px solid #1F2937;
        padding: 20px; border-radius: 12px; margin-bottom: 12px;
        display: flex; justify-content: space-between; align-items: center;
        transition: all 0.2s ease;
    }
    .alt-item:hover { border-color: #3B82F6; background: #1F2937; transform: translateX(5px); }

    /* BUTTON */
    .amazon-btn {
        background: linear-gradient(90deg, #F59E0B, #D97706);
        color: white !important; padding: 16px 32px; border-radius: 50px;
        text-decoration: none; font-weight: 800; display: inline-block; margin-top: 30px;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
        transition: transform 0.2s;
    }
    .amazon-btn:hover { transform: scale(1.05); color: white !important; }

</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR INPUTS ---
with st.sidebar:
    st.title("💎 TechChoose")
    st.caption("Global Rank Algorithm")
    st.write("---")
    
    os_choice = st.selectbox("📱 Ecosystem", ["Any", "iOS (Apple)", "Android"])
    st.write("")
    lifestyle = st.selectbox("👤 User Persona", [
        "🎮 Hardcore Gamer", 
        "📸 Content Creator", 
        "💼 Business Pro", 
        "💰 Student / Budget", 
        "🛠️ Custom Manual"
    ])
    st.write("")
    budget = st.slider("💰 Max Budget (USD)", 300, 2000, 2000, step=50)

    # --- 🧠 5. SMART ALGORITHM (สูตรลับระดับโลก) ---
    # ค่าเริ่มต้น
    p, c, b, v = 5, 5, 5, 5
    
    # Step 1: ปรับตาม Persona
    if "Gamer" in lifestyle: p,c,b,v = 10, 3, 8, 4   # Gamer เน้นแรง ไม่เน้นคุ้มมาก
    elif "Creator" in lifestyle: p,c,b,v = 7, 10, 8, 5
    elif "Business" in lifestyle: p,c,b,v = 8, 6, 9, 6
    elif "Student" in lifestyle: p,c,b,v = 5, 5, 7, 10 # Student เน้นคุ้มสุดๆ
    
    # Step 2: Dynamic Budget Weighting (ทีเด็ด!)
    # ถ้างบเยอะ (> $1,000) -> คนรวยไม่แคร์ความคุ้ม -> ลด Value, เพิ่ม Spec
    if budget >= 1000:
        v = 2       # ลดความสำคัญของความคุ้มค่าลงต่ำมาก
        p += 2      # เพิ่มคะแนนความแรง
        c += 2      # เพิ่มคะแนนกล้อง
    
    # ถ้างบน้อย (< $600) -> คนงบน้อยแคร์ความคุ้มที่สุด
    elif budget <= 600:
        v = 12      # ความคุ้มค่า (Value) คือพระเจ้า
    
    # (Custom Mode)
    if "Custom" in lifestyle:
        st.divider()
        p = st.slider("Performance", 1,10,8)
        c = st.slider("Camera", 1,10,8)
        b = st.slider("Battery", 1,10,5)
        v = st.slider("Value", 1,10,5)

    st.divider()
    st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True)

# --- 6. HELPER FUNCTIONS ---
def get_verdict(row, mode):
    # คำคม AI
    if "Gamer" in mode: return f"The absolute gaming king. **{row['name']}** destroys benchmarks with a performance score of {row['performance']}/10."
    elif "Creator" in mode: return f"Cinematic quality in your hand. **{row['name']}** offers a studio-grade camera system."
    elif "Student" in mode: return f"Unbeatable value for money. **{row['name']}** outperforms everything in its price class."
    else: return f"The perfect daily driver. **{row['name']}** balances premium specs with reliability."

def stat_html(label, score, color):
    # สร้าง HTML หลอดพลัง (เขียนชิดซ้ายเพื่อกันบั๊ก Indentation)
    return f"""
    <div class='stat-item'>
        <div class='stat-title'>{label}</div>
        <div class='stat-num'>{score}/10</div>
        <div class='bar-bg'><div style='width:{score*10}%; height:100%; background:{color};'></div></div>
    </div>
    """

# --- 7. MAIN LOGIC ---
df = load_data()

if not df.empty:
    # Filter 1: OS
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']
    
    # Filter 2: Budget
    df = df[df['price'] <= budget]

    # Calculation
    df['score'] = (df['performance']*p) + (df['camera']*c) + (df['battery']*b) + (df['value']*v)
    max_score = (10*p) + (10*c) + (10*b) + (10*v)
    df['match'] = (df['score'] / max_score) * 100
    df = df.sort_values(by='match', ascending=False).reset_index(drop=True)

    if len(df) > 0:
        winner = df.iloc[0]
        c1, c2 = st.columns([1.4, 1], gap="large")

        # --- WINNER SECTION ---
        with c1:
            st.markdown(f"""
            <div class='winner-box'>
                <span class='rank-tag'>🏆 #1 Global Pick</span>
                <div class='hero-title'>{winner['name']}</div>
                <div class='hero-price'>${winner['price']:,}</div>
                
                <p style='color:#9CA3AF; font-size:1.1em; line-height:1.6; margin-bottom:30px;'>
                    {get_verdict(winner, lifestyle)}
                </p>
                
                <div class='stat-container'>
                    {stat_html("🚀 SPEED", winner['performance'], "#3B82F6")}
                    {stat_html("📸 CAMERA", winner['camera'], "#A855F7")}
                    {stat_html("🔋 BATTERY", winner['battery'], "#10B981")}
                </div>

                <a href="{winner['link']}" target="_blank" class="amazon-btn">
                    🛒 CHECK PRICE ON AMAZON
                </a>
            </div>
            """, unsafe_allow_html=True)

        # --- ALTERNATIVES SECTION ---
        with c2:
            st.markdown("### 📊 Market Comparison")
            st.caption(f"Showing top matches under ${budget:,}")
            
            for i, row in df.iloc[1:5].iterrows():
                diff = winner['price'] - row['price']
                save_tag = f"<span style='color:#10B981; font-weight:bold; font-size:0.85em;'>Save ${diff:,}</span>" if diff > 0 else ""
                
                st.markdown(f"""
                <div class='alt-item'>
                    <div>
                        <div style='font-weight:700; font-size:1.1em; color:white;'>{i}. {row['name']}</div>
                        <div style='color:#9CA3AF; margin-top:4px;'>${row['price']:,} &nbsp; {save_tag}</div>
                    </div>
                    <div style='text-align:right;'>
                        <div style='color:#3B82F6; font-weight:900; font-size:1.2em;'>{row['match']:.0f}%</div>
                        <a href="{row['link']}" target="_blank" style='color:#F59E0B; text-decoration:none; font-size:0.8em; font-weight:600;'>View ></a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.warning(f"No smartphones found under ${budget:,}. Try increasing your budget.")
else:
    st.error("Error: Cannot connect to database.")