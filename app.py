import streamlit as st
import pandas as pd

# --- 1. CONFIG ---
st.set_page_config(
    page_title="TechChoose - Pro Edition",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    # 👇👇👇 ใส่ลิงก์ CSV ของพี่เหมือนเดิมครับ 👇👇👇
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv" 
    try:
        df = pd.read_csv(sheet_url)
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        return df
    except:
        return pd.DataFrame()

# --- 3. PREMIUM DARK CSS (บังคับดำทั้งหน้าจอรวม Sidebar) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* พื้นหลังหลัก (Main Area) */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }

    /* 🔥 ปรับ Sidebar ให้ดำเข้ม ดูหรู 🔥 */
    section[data-testid="stSidebar"] {
        background-color: #020617; /* ดำสนิทกว่า Main นิดหน่อย */
        border-right: 1px solid #1E293B;
    }
    
    /* ปรับสีตัวหนังสือใน Sidebar */
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
    }

    /* Winner Box */
    .winner-box {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border: 2px solid #3B82F6;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.2);
    }
    
    /* Product Card */
    .product-card {
        background: #1E293B; border: 1px solid #334155;
        padding: 20px; border-radius: 12px; margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .product-card:hover { border-color: #3B82F6; transform: translateX(5px); }

    /* Button Style */
    .stButton > button {
        background: linear-gradient(90deg, #F59E0B, #D97706);
        color: white; border: none; font-weight: bold; width: 100%;
        padding: 15px; border-radius: 10px; transition: 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
        color: white;
    }

    /* Amazon Button Link */
    .amazon-btn {
        background: linear-gradient(to bottom, #FFD814, #F7CA00);
        color: #000000 !important; padding: 12px 30px; border-radius: 8px;
        text-decoration: none; font-weight: 800; display: inline-block;
        margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Text Styles */
    .price-big { color: #FBBF24; font-weight: 900; font-size: 2.2em; }
    .pros-text { color: #4ADE80; font-size: 0.9em; margin-bottom: 5px; text-align: left; }
    
    /* Progress Bar */
    .stProgress > div > div > div > div { background: linear-gradient(90deg, #3B82F6 0%, #60A5FA 100%); }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR (COMPACT VERSION) ---
with st.sidebar:
    st.title("💎 TechChoose")
    st.caption("AI Gadget Consultant")
    st.write("---")
    
    # 1. OS Selection (ใช้ Selectbox แทน Radio)
    os_choice = st.selectbox(
        "📱 Ecosystem Preference:",
        ["Any", "iOS (Apple)", "Android"]
    )
    
    st.write("") # เว้นวรรคนิดนึง
    
    # 2. Persona Selection (ใช้ Selectbox ประหยัดที่)
    lifestyle = st.selectbox(
        "👤 Select Your Persona:",
        [
            "🎮 Hardcore Gamer", 
            "📸 Content Creator", 
            "💼 Business / Work", 
            "💰 Student / Budget Saver", 
            "🛠️ Custom (Manual)"
        ]
    )

    # Info Box (แสดงการตั้งค่าปัจจุบันแบบย่อ)
    st.markdown("<br>", unsafe_allow_html=True)
    setting_msg = ""
    if lifestyle == "🎮 Hardcore Gamer":
        p, c, b, v = 10, 3, 8, 5
        setting_msg = "Focus: 🚀 Speed & 🔋 Battery"
    elif lifestyle == "📸 Content Creator":
        p, c, b, v = 7, 10, 8, 5
        setting_msg = "Focus: 📸 Camera & Storage"
    elif lifestyle == "💼 Business / Work":
        p, c, b, v = 8, 6, 9, 6
        setting_msg = "Focus: ⚖️ Balance & Stability"
    elif lifestyle == "💰 Student / Budget Saver":
        p, c, b, v = 5, 5, 7, 10
        setting_msg = "Focus: 💰 Best Value"
    else:
        # Custom Mode
        st.caption("⚙️ Manual Sliders")
        def get_score(label): return {"Ignore": 1, "Nice": 5, "Imp.": 8, "Max": 10}[label]
        # ย่อ label ให้สั้นลงจะได้ไม่รก
        p = get_score(st.select_slider("Speed", ["Ignore", "Nice", "Imp.", "Max"], "Imp."))
        c = get_score(st.select_slider("Camera", ["Ignore", "Nice", "Imp.", "Max"], "Imp."))
        b = get_score(st.select_slider("Battery", ["Ignore", "Nice", "Imp.", "Max"], "Nice"))
        v = get_score(st.select_slider("Price", ["Ignore", "Nice", "Imp.", "Max"], "Nice"))
        setting_msg = "Custom Configuration"

    if lifestyle != "🛠️ Custom (Manual)":
        st.info(f"✅ {setting_msg}")

    st.write("---")
    st.button("🔥 FIND MY MATCH") # ปุ่มใหญ่ เต็มความกว้าง

# --- 5. HELPER FUNCTIONS ---
def generate_verdict(row, mode):
    if "Gamer" in mode: return f"Absolute beast for gaming! Performance score: {row['performance']}/10."
    elif "Creator" in mode: return f"Top-tier camera system ({row['camera']}/10) for stunning photos."
    elif "Student" in mode or "Budget" in mode: return f"Best value for money at ${row['price']:,}."
    else: return f"Perfect all-rounder balancing speed, battery, and reliability."

def get_pros(row):
    pros = []
    if row['performance'] >= 9: pros.append("🚀 Top Performance")
    if row['camera'] >= 9: pros.append("📸 Pro Camera")
    if row['battery'] >= 9: pros.append("🔋 All-Day Battery")
    if row['value'] >= 8: pros.append("💰 Great Value")
    return pros

# --- 6. MAIN CONTENT ---
df = load_data()

if not df.empty:
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']

    # Calc
    df['score'] = (df['performance']*p) + (df['camera']*c) + (df['battery']*b) + (df['value']*v)
    max_score = (10*p) + (10*c) + (10*b) + (10*v)
    df['match'] = (df['score'] / max_score) * 100
    df = df.sort_values(by='match', ascending=False).reset_index(drop=True)
    winner = df.iloc[0]

    c1, c2 = st.columns([1.5, 1.2], gap="large")

    # Winner
    with c1:
        st.markdown(f"""
        <div class='winner-box'>
            <span style='background:#3B82F6; color:white; padding:4px 12px; border-radius:15px; font-size:0.8em; font-weight:bold;'>SELECTED FOR: {lifestyle.split(' ')[1].upper()}</span>
            <h1 style='margin-top:15px;'>{winner['name']}</h1>
            <div class='price-big'>${winner['price']:,}</div>
            <div style='background:#172554; padding:15px; border-radius:10px; margin-top:20px; text-align:left; border-left:4px solid #F59E0B;'>
                <b>💡 AI Analysis:</b><br>{generate_verdict(winner, lifestyle)}
            </div>
            <br>
        """, unsafe_allow_html=True)
        
        for pro in get_pros(winner):
            st.markdown(f"<div class='pros-text'>✅ {pro}</div>", unsafe_allow_html=True)

        st.markdown(f"""
            <a href="{winner['link']}" target="_blank" class="amazon-btn">
                🛒 Check Price on Amazon
            </a>
        </div>
        """, unsafe_allow_html=True)

    # Alternatives
    with c2:
        st.subheader("🥈 Top Alternatives")
        for i, row in df.iloc[1:4