import streamlit as st
import pandas as pd
import random

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Final Fix",
    page_icon="🛒",
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
        
        # --- ระบบกันเหนียว (Auto-Fill) ---
        # ถ้าใน Excel พี่ไม่มีคอลัมน์ antutu (หรือยังไม่อัปเดต) โค้ดนี้จะกันไม่ให้แอปพัง
        # และใส่เลขสมมติให้ดูเป็นตัวอย่างไปก่อน
        if 'antutu' not in df.columns: 
            df['antutu'] = df['price'].apply(lambda x: x * 2500 if x > 0 else 500000)
        if 'dxomark' not in df.columns: 
            df['dxomark'] = df['camera'].apply(lambda x: x * 15 + 20)
        if 'award' not in df.columns: 
            df['award'] = "Best Choice"
            
        return df
    except Exception:
        return pd.DataFrame()

# --- 3. CSS (High Contrast Fix) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Inter:wght@400;600;900&display=swap');
    
    /* พื้นหลังหลัก */
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* --- SIDEBAR FIX (แก้ให้มองเห็นชัดๆ) --- */
    section[data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #333; }
    
    /* บังคับกล่องเลือกเป็น "สีขาว" ตัวหนังสือ "สีดำ" (High Contrast) */
    div[data-baseweb="select"] > div { 
        background-color: #FFFFFF !important; 
        color: #000000 !important; 
        border: 2px solid #3B82F6 !important; 
    }
    div[data-baseweb="select"] span { 
        color: #000000 !important; /* ตัวหนังสือในกล่องเป็นสีดำ */
        font-weight: bold;
    }
    /* สีของ Dropdown ตอนกด */
    ul[data-baseweb="menu"] { background-color: #FFFFFF !important; }
    li[data-baseweb="option"] { color: #000000 !important; }

    /* ป้าย Label ใน Sidebar */
    .stMarkdown label p { font-size: 1.1em; font-weight: bold; color: #F59E0B !important; }

    /* --- WINNER BOX --- */
    .winner-box {
        background: #0A0A0A;
        border: 2px solid #3B82F6;
        border-radius: 16px; padding: 30px;
        text-align: left;
    }
    .hero-title { font-size: 3em; font-weight: 900; margin-bottom: 10px; line-height: 1.2; color: #FFF; }
    .hero-price { color: #FBBF24; font-size: 2.8em; font-weight: 800; font-family: 'JetBrains Mono'; margin-bottom: 20px;}
    
    /* BENCHMARK GRID */
    .bench-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 20px 0; background: #151515; padding: 15px; border-radius: 10px;}
    .bench-item { text-align: center; }
    .bench-score { font-size: 1.5em; font-weight: 800; color: white; }
    .bench-label { font-size: 0.8em; color: #AAA; }

    /* BUTTON */
    .amazon-btn {
        display: block; width: 100%; background-color: #F59E0B; color: #000; 
        padding: 15px; text-align: center; border-radius: 8px; font-weight: 900; 
        text-decoration: none; font-size: 1.2em; margin-top: 20px;
    }
    .amazon-btn:hover { background-color: #FFF; }

    /* ALTERNATIVES */
    .alt-row { background: #111; padding: 15px; margin-bottom: 10px; border-radius: 8px; border: 1px solid #222; display:flex; justify-content:space-between; align-items:center;}
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🛒 TechChoose")
    st.markdown("### ⚙️ ตัวเลือกการค้นหา") # ใช้ Markdown ให้ตัวใหญ่ขึ้น
    
    os_choice = st.selectbox("📱 ระบบปฏิบัติการ (System)", ["Any", "iOS", "Android"])
    st.write("")
    lifestyle = st.selectbox("👤 รูปแบบการใช้งาน (Usage)", ["🎮 Hardcore Gamer", "📸 Content Creator", "💼 Business Pro", "💰 Student / Budget", "🛠️ Custom"])
    st.write("")
    budget = st.slider("💰 งบประมาณสูงสุด ($)", 100, 2000, 2000, step=50)

    # Logic
    p, c, b, v = 5, 5, 5, 5
    if "Gamer" in lifestyle: p,c,b,v = 10, 3, 8, 4
    elif "Creator" in lifestyle: p,c,b,v = 7, 10, 8, 5
    elif "Business" in lifestyle: p,c,b,v = 8, 6, 9, 6
    elif "Student" in lifestyle: p,c,b,v = 5, 5, 7, 15 # เน้นคุ้มมากๆ
    
    if budget >= 1000: v = 2; p += 2; c += 2
    elif budget <= 400: v = 20 # งบน้อย บูสต์ความคุ้มค่าสุดๆ

    if "Custom" in lifestyle:
        st.divider()
        p = st.slider("Perf", 1,10,8); c = st.slider("Cam", 1,10,8); b = st.slider("Batt", 1,10,5); v = st.slider("Val", 1,10,5)

    st.divider()
    st.button("🔍 ค้นหามือถือที่ใช่", type="primary", use_container_width=True)

# --- 5. MAIN APP ---
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
            # --- HTML STRING แบบบรรทัดเดียว (แก้โค้ดหลุด 100%) ---
            # ผมเอา indentation ออกหมด เพื่อไม่ให้ Markdown เข้าใจผิดว่าเป็น code block
            winner_html = f"""
<div class='winner-box'>
<div style='color:#3B82F6; font-weight:bold; margin-bottom:10px;'>🏆 {winner['award']}</div>
<div class='hero-title'>{winner['name']}</div>
<div class='hero-price'>${winner['price']:,}</div>
<div class='bench-grid'>
<div class='bench-item'><div class='bench-score' style='color:#3B82F6'>🚀 {int(winner['antutu']):,}</div><div class='bench-label'>AnTuTu Score</div></div>
<div class='bench-item'><div class='bench-score' style='color:#A855F7'>📸 {int(winner['dxomark'])}</div><div class='bench-label'>DXOMARK</div></div>
</div>
<div style='color:#CCC; line-height:1.6; margin-bottom:20px;'>
<b>💡 AI Verdict:</b> This device matches <b>{winner['match']:.1f}%</b> of your requirement profile. Best in class for {lifestyle} usage.
</div>
<a href="{winner['link']}" target="_blank" class='amazon-btn'>🛒 CHECK AMAZON PRICE</a>
</div>
"""
            st.markdown(winner_html, unsafe_allow_html=True)

        with c2:
            st.markdown("### 📉 Best Alternatives")
            for i, row in df.iloc[1:6].iterrows():
                diff = winner['price'] - row['price']
                save_tag = f"<span style='color:#10B981; font-weight:bold;'>SAVE ${diff:,}</span>" if diff > 0 else ""
                
                # HTML บรรทัดเดียวเช่นกัน
                alt_html = f"""
<div class='alt-row'>
<div><div style='font-weight:bold; font-size:1.1em;'>{i}. {row['name']}</div><div style='color:#888; font-size:0.9em;'>AnTuTu: {int(row['antutu']):,} | ${row['price']:,}</div></div>
<div style='text-align:right;'><div style='color:#3B82F6; font-weight:bold; font-size:1.2em;'>{row['match']:.0f}%</div><div>{save_tag}</div></div>
</div>
"""
                st.markdown(alt_html, unsafe_allow_html=True)

    else:
        st.warning(f"ไม่พบมือถือในช่วงราคาต่ำกว่า ${budget} ลองเพิ่มงบอีกนิดนะครับ")
else:
    st.error("เชื่อมต่อฐานข้อมูลไม่ได้")