import streamlit as st
import pandas as pd

# --- 1. CONFIG & SETUP ---
st.set_page_config(
    page_title="TechChoose - Smart Comparison",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State สำหรับเก็บค่าว่าลูกค้ากดดูตัวไหนอยู่
if 'compare_item' not in st.session_state:
    st.session_state.compare_item = None

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

# --- 3. PREMIUM DESIGN (NEON STYLE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');
    
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    /* Winner Section */
    .winner-box {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    
    /* Comparison Box (VS) */
    .vs-container {
        background-color: #172554; /* สีน้ำเงินเข้ม */
        border: 2px solid #3B82F6;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 30px;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }

    /* Progress Bar สวยๆ */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #F59E0B 0%, #FCD34D 100%);
        height: 12px !important; border-radius: 6px;
    }

    /* ปุ่ม Amazon */
    .amazon-btn {
        background: linear-gradient(to bottom, #FFD814, #F7CA00);
        color: black !important; padding: 12px 25px; border-radius: 30px;
        text-decoration: none; font-weight: 800; display: inline-block;
        margin-top: 15px; transition: transform 0.2s;
    }
    .amazon-btn:hover { transform: scale(1.05); }

    /* Card สินค้า */
    .product-card {
        background: #1E293B; border: 1px solid #334155;
        padding: 15px; border-radius: 12px; margin-bottom: 15px;
        transition: all 0.2s;
    }
    .product-card:hover { border-color: #F59E0B; transform: translateX(5px); }

    /* Text Colors */
    .price-tag { color: #FBBF24; font-weight: 900; font-size: 1.5em; }
    .match-score { color: #3B82F6; font-weight: 800; }
    
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🎯 Preference Setup")
    st.caption("Customize your perfect match.")
    st.divider()
    
    # 🌟 OS Filter
    os_choice = st.radio("System:", ["Any", "iOS (iPhone)", "Android"], index=0)
    st.write("---")

    # Helper function
    def get_score(label):
        return {"Don't Care": 1, "Nice to Have": 5, "Important": 8, "Essential!": 10}[label]

    # Select Sliders (แบบที่พี่ชอบ)
    p_opt = st.select_slider("Speed & Gaming", ["Don't Care", "Nice to Have", "Important", "Essential!"], "Important")
    c_opt = st.select_slider("Camera Quality", ["Don't Care", "Nice to Have", "Important", "Essential!"], "Important")
    b_opt = st.select_slider("Battery Life", ["Don't Care", "Nice to Have", "Important", "Essential!"], "Nice to Have")
    v_opt = st.select_slider("Price / Value", ["Don't Care", "Nice to Have", "Important", "Essential!"], "Nice to Have")

    w_perf, w_cam, w_batt, w_val = get_score(p_opt), get_score(c_opt), get_score(b_opt), get_score(v_opt)

    st.divider()
    if st.button("🚀 Find My Match", type="primary"):
        st.session_state.compare_item = None # Reset การเปรียบเทียบเมื่อกดหาใหม่
        st.rerun()

# --- 5. MAIN LOGIC ---
df = load_data()

if not df.empty:
    # Filter OS
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']

    # Calc Score
    df['score_raw'] = (df['performance']*w_perf) + (df['camera']*w_cam) + (df['battery']*w_batt) + (df['value']*w_val)
    max_possible = (10*w_perf) + (10*w_cam) + (10*w_batt) + (10*w_val)
    df['match_percent'] = (df['score_raw'] / max_possible) * 100
    df = df.sort_values(by='match_percent', ascending=False).reset_index(drop=True)
    
    winner = df.iloc[0]

    # --- SHOW COMPARISON (ถ้ามีการกดปุ่มเลือก) ---
    if st.session_state.compare_item is not None:
        challenger = st.session_state.compare_item
        st.markdown(f"### 🥊 Head-to-Head Comparison")
        
        with st.container():
            st.markdown(f"""
            <div class="vs-container">
                <div style="display:flex; justify-content:space-around; align-items:center; text-align:center;">
                    <div style="width:40%;">
                        <h2 style="color:#FBBF24;">{winner['name']}</h2>
                        <div style="font-size:2em;">${winner['price']:,}</div>
                        <div style="color:#FBBF24;">🏆 WINNER</div>
                    </div>
                    <div style="font-size:3em; font-weight:900; color:#3B82F6;">VS</div>
                    <div style="width:40%;">
                        <h2>{challenger['name']}</h2>
                        <div style="font-size:2em;">${challenger['price']:,}</div>
                        <div style="color:#94A3B8;">CHALLENGER</div>
                    </div>
                </div>
                <hr style="border-color:#3B82F6;">
                <div style="display:flex; justify-content:space-around;">
                    <div>Speed: <b>{winner['performance']}</b> vs {challenger['performance']}</div>
                    <div>Camera: <b>{winner['camera']}</b> vs {challenger['camera']}</div>
                    <div>Battery: <b>{winner['battery']}</b> vs {challenger['battery']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- LAYOUT หลัก ---
    col1, col2 = st.columns([1.5, 1.2], gap="large")

    # ฝั่งซ้าย: WINNER
    with col1:
        st.markdown(f"<div class='winner-box'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#FBBF24'>🏆 TOP PICK FOR YOU ({winner['match_percent']:.0f}%)</h3>", unsafe_allow_html=True)
        st.markdown(f"<h1>{winner['name']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div class='price-tag'>${winner['price']:,}</div>", unsafe_allow_html=True)
        
        st.write("---")
        st.progress(int(winner['performance']*10), f"⚡ Speed: {winner['performance']}/10")
        st.progress(int(winner['camera']*10), f"📸 Camera: {winner['camera']}/10")
        st.progress(int(winner['battery']*10), f"🔋 Battery: {winner['battery']}/10")
        
        st.markdown(f"""
            <a href="{winner['link']}" target="_blank" class="amazon-btn">
                🛒 See Best Deal on Amazon
            </a>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ฝั่งขวา: Runners-up (พร้อมปุ่ม Compare)
    with col2:
        st.subheader("🥈 Compare with Alternatives")
        for i, row in df.iloc[1:6].iterrows(): # โชว์แค่ 5 อันดับแรก
            
            # สร้างการ์ดสินค้า
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <div style="display:flex; justify-content:space-between;">
                        <b style="font-size:1.1em;">{row['name']}</b>
                        <span class="match-score">{row['match_percent']:.0f}%</span>
                    </div>
                    <div style="color:#94A3B8;">Est. ${row['price']:,}</div>
                """, unsafe_allow_html=True)
                
                # ปุ่ม Compare (Streamlit Button ต้องอยู่นอก HTML block)
                c1, c2 = st.columns([1, 1])
                with c1:
                    # ปุ่มกดเพื่อเปรียบเทียบ
                    if st.button(f"🆚 VS Winner", key=f"btn_{i}"):
                        st.session_state.compare_item = row
                        st.rerun()
                with c2:
                    st.markdown(f"<a href='{row['link']}' target='_blank' style='color:#FBBF24; text-decoration:none; font-weight:bold;'>View Deal ></a>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

    # --- Disclaimer ---
    st.write("---")
    st.caption("Disclaimer: TechChoose is a participant in the Amazon Services LLC Associates Program. Prices are accurate as of the date indicated.")

else:
    st.error("Please connect your Google Sheet CSV.")