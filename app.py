import streamlit as st
import pandas as pd

# --- 1. CONFIG ---
st.set_page_config(
    page_title="TechChoose - Pro Edition",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA (ฝังลิงก์ให้แล้วครับ ✅) ---
@st.cache_data(ttl=60)
def load_data():
    # ลิงก์ของพี่ครับ
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        # แปลงชื่อรุ่นให้เช็ค OS ง่ายๆ
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        return df
    except Exception as e:
        return pd.DataFrame()

# --- 3. PREMIUM DARK CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* พื้นหลังหลัก */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }

    /* ปรับ Sidebar ให้ดำเข้ม */
    section[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1E293B;
    }
    
    /* สีตัวหนังสือใน Sidebar */
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p {
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

    /* Amazon Button */
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

# --- 4. SIDEBAR (COMPACT & CLEAN) ---
with st.sidebar:
    st.title("💎 TechChoose")
    st.caption("AI Gadget Consultant")
    st.write("---")
    
    # 1. OS Selection (Dropdown)
    os_choice = st.selectbox(
        "📱 Ecosystem Preference:",
        ["Any", "iOS (Apple)", "Android"]
    )
    
    st.write("") 
    
    # 2. Persona Selection (Dropdown)
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

    # Info Box logic
    setting_msg = ""
    p, c, b, v = 5, 5, 5, 5 # Default values

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
        st.write("---")
        st.caption("⚙️ Manual Sliders")
        def get_score(label): return {"Ignore": 1, "Nice": 5, "Imp.": 8, "Max": 10}[label]
        p = get_score(st.select_slider("Speed", ["Ignore", "Nice", "Imp.", "Max"], "Imp."))
        c = get_score(st.select_slider("Camera", ["Ignore", "Nice", "Imp.", "Max"], "Imp."))
        b = get_score(st.select_slider("Battery", ["Ignore", "Nice", "Imp.", "Max"], "Nice"))
        v = get_score(st.select_slider("Price", ["Ignore", "Nice", "Imp.", "Max"], "Nice"))
        setting_msg = "Custom Configuration"

    if lifestyle != "🛠️ Custom (Manual)":
        st.write("")
        st.info(f"✅ {setting_msg}")

    st.write("---")
    st.button("🔥 FIND MY MATCH")

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
    
    # Check if we have data
    if len(df) > 0:
        winner = df.iloc[0]

        c1, c2 = st.columns([1.5, 1.2], gap="large")

        # Winner Section
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

        # Alternatives Section
        with c2:
            st.subheader("🥈 Top Alternatives")
            
            # วนลูปแสดงแค่ 3 ตัวรอง (ลำดับที่ 2-4)
            # ใช้ df.iloc[1:4] เพื่อดึงตัวที่ 2 ถึง 4
            alternatives = df.iloc[1:4]
            
            for i, row in alternatives.iterrows():
                diff = winner['price'] - row['price']
                tag = ""
                if diff > 0: 
                    tag = f"<span style='color:#34D399; background:#064E3B; padding:2px 6px; border-radius:4px; font-size:0.75em;'>Save ${diff:,}</span>"
                
                # ใช้ HTML แบบตรงไปตรงมาเพื่อกัน Error
                st.markdown(f"""
                <div class="product-card">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <b>{row['name']}</b>
                            <div style="color:#94A3B8; font-size:0.9em;">Est. ${row['price']:,}</div>
                            {tag}
                        </div>
                        <div style="text-align:right;">
                            <span style="color:#3B82F6; font-weight:bold;">{row['match']:.0f}%</span><br>
                            <a href="{row['link']}" target="_blank" style="color:#F59E0B; text-decoration:none; font-size:0.8em;">View Deal ></a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No products found matching your criteria.")

else:
    st.error("Cannot connect to Google Sheet. Please check the link.")