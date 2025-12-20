import streamlit as st
import pandas as pd

# --- 1. SETUP ---
st.set_page_config(
    page_title="TechChoose - Smart Gadget Finder",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CONNECT DATABASE ---
@st.cache_data(ttl=60)
def load_data():
    # 👇👇👇 ลิงก์เดิมของพี่ (อย่าลืมใส่นะครับ) 👇👇👇
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv" 
    # 👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆
    try:
        df = pd.read_csv(sheet_url)
        return df
    except:
        return pd.DataFrame()

# --- 3. PREMIUM DESIGN (NEON & GLOW) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');
    
    .stApp {
        background-color: #0F172A; /* สีน้ำเงินดำ ลึกกว่าเดิม */
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }

    /* Progress Bar แต่งใหม่ ให้เหมือนหลอดพลังงานเกม */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #F59E0B 0%, #FCD34D 100%); /* ไล่สีทอง */
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.5); /* ใส่เงาเรืองแสง */
        border-radius: 10px;
        height: 12px !important;
    }
    .stProgress > div > div {
        background-color: #334155 !important; /* พื้นหลังหลอดสีเทาเข้ม ตัดกันชัดเจน */
        border-radius: 10px;
        height: 12px !important;
    }

    /* ตกแต่งตัวเลขคะแนน */
    .spec-score {
        font-size: 0.9em;
        font-weight: 700;
        color: #FCD34D;
        margin-bottom: -5px;
    }

    /* Metric ราคา */
    [data-testid="stMetricValue"] {
        color: #FBBF24 !important;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px rgba(251, 191, 36, 0.3);
    }

    /* ปุ่ม Amazon */
    .amazon-btn {
        background: linear-gradient(to bottom, #FFD814, #F7CA00);
        border: 1px solid #FCD200;
        color: #111 !important;
        padding: 15px;
        border-radius: 25px; /* ปุ่มมน ดูทันสมัย */
        text-align: center;
        font-weight: 800;
        text-decoration: none;
        display: block;
        margin-top: 20px;
        transition: transform 0.2s;
    }
    .amazon-btn:hover {
        transform: scale(1.05);
        background: #F7CA00;
    }

    /* Card */
    .product-card {
        background: #1E293B;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR (LOGIC ใหม่: เลือกเป็นคำพูด) ---
with st.sidebar:
    st.title("🎯 Preference Setup")
    st.caption("Customize your perfect match.")
    st.divider()
    
    # ฟังก์ชันแปลงคำพูดเป็นตัวเลข
    def get_score(label):
        mapping = {
            "Don't Care": 1,
            "Nice to Have": 5,
            "Important": 8,
            "Essential!": 10
        }
        return mapping[label]

    # ตัวเลือกแบบ Select Slider (เลือกคำพูด)
    st.subheader("🎮 Gaming & Speed")
    p_opt = st.select_slider("How much speed do you need?", options=["Don't Care", "Nice to Have", "Important", "Essential!"], value="Important")
    
    st.subheader("📸 Camera Quality")
    c_opt = st.select_slider("Do you take lots of photos?", options=["Don't Care", "Nice to Have", "Important", "Essential!"], value="Important")
    
    st.subheader("🔋 Battery Life")
    b_opt = st.select_slider("Need all-day battery?", options=["Don't Care", "Nice to Have", "Important", "Essential!"], value="Nice to Have")
    
    st.subheader("💰 Budget Friendly")
    v_opt = st.select_slider("Is price a major factor?", options=["Don't Care", "Nice to Have", "Important", "Essential!"], value="Nice to Have")

    # แปลงกลับเป็นตัวเลขเพื่อคำนวณ
    w_perf = get_score(p_opt)
    w_cam = get_score(c_opt)
    w_batt = get_score(b_opt)
    w_val = get_score(v_opt)

    st.divider()
    if st.button("🚀 Find My Match", type="primary"):
        load_data.clear()
        st.rerun()

# --- 5. MAIN CONTENT ---
df = load_data()

if not df.empty:
    # Logic คำนวณ (เหมือนเดิมแต่แม่นขึ้นเพราะ input ชัดเจนขึ้น)
    df['score_raw'] = (df['performance'] * w_perf) + (df['camera'] * w_cam) + (df['battery'] * w_batt) + (df['value'] * w_val)
    max_possible = (10*w_perf) + (10*w_cam) + (10*w_batt) + (10*w_val)
    df['match_percent'] = (df['score_raw'] / max_possible) * 100
    df = df.sort_values(by='match_percent', ascending=False).reset_index(drop=True)
    winner = df.iloc[0]

    col1, col2 = st.columns([1.8, 1.2], gap="large")
    
    # --- WINNER ---
    with col1:
        st.markdown(f"<span style='color:#FBBF24; font-weight:bold; font-size:1.2em;'>🏆 BEST MATCH FOR YOU ({winner['match_percent']:.0f}%)</span>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='margin-top:-10px;'>{winner['name']}</h1>", unsafe_allow_html=True)
        
        st.metric("Estimated Price", f"${winner['price']:,}")
        
        st.write("---")
        st.markdown("#### ⚡ Performance Analysis")
        
        # Custom Progress Bars with Labels
        st.markdown(f"<div class='spec-score'>Gaming & Speed: {winner['performance']}/10</div>", unsafe_allow_html=True)
        st.progress(int(winner['performance']*10))
        
        st.markdown(f"<div class='spec-score'>Camera Quality: {winner['camera']}/10</div>", unsafe_allow_html=True)
        st.progress(int(winner['camera']*10))
        
        st.markdown(f"<div class='spec-score'>Battery Life: {winner['battery']}/10</div>", unsafe_allow_html=True)
        st.progress(int(winner['battery']*10))

        st.markdown(f"""
            <a href="{winner['link']}" target="_blank" class="amazon-btn">
                🛒 View Best Deal on Amazon
            </a>
        """, unsafe_allow_html=True)

    # --- RUNNERS UP ---
    with col2:
        st.subheader("🥈 Other Great Options")
        for i, row in df.iloc[1:].iterrows():
            st.markdown(f"""
            <div class="product-card">
                <div style="display:flex; justify-content:space-between;">
                    <b>{row['name']}</b>
                    <span style="color:#3B82F6; font-weight:900;">{row['match_percent']:.0f}%</span>
                </div>
                <div style="font-size:0.9em; color:#94A3B8;">${row['price']:,}</div>
                <a href="{row['link']}" target="_blank" style="color:#FBBF24; font-weight:bold; text-decoration:none; font-size:0.9em; display:block; margin-top:5px;">
                    👉 Check Price >
                </a>
            </div>
            """, unsafe_allow_html=True)

else:
    st.error("⚠️ Data connect error. Check CSV link.")