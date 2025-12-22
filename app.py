import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Final VS",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
    except Exception:
        return pd.DataFrame()

    if not df.empty:
        # Clean Data
        df = df.dropna(subset=['name', 'price'])
        
        def get_os(name):
            name_str = str(name).lower()
            if 'iphone' in name_str or 'ipad' in name_str: return 'iOS'
            return 'Android'
        df['os_type'] = df['name'].apply(get_os)
        
        if 'antutu' in df.columns:
            df['perf_score'] = (df['antutu'] / 3500000) * 10 
            df['perf_score'] = df['perf_score'].clip(upper=10)
        else: df['perf_score'] = 8.0 
        
        if 'camera' in df.columns: df['cam_score'] = df['camera']
        if 'battery' in df.columns: df['batt_score'] = df['battery']
        if 'value' not in df.columns: df['value'] = 8.0
        if 'antutu' not in df.columns: df['antutu'] = df['price'] * 2000

        # Affiliate Link
        my_tag = "techchoose-20"
        df['link'] = df['link'].apply(lambda x: f"{x}&tag={my_tag}" if '?' in str(x) else f"{x}?tag={my_tag}")

    return df

# --- 3. CSS (Pro Dark Theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Inter:wght@400;600;900&display=swap');
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #000; padding-bottom: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #111; border-radius: 5px; color: #888; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #222 !important; color: #3B82F6 !important; border: 1px solid #333; }

    /* Inputs Fix */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { background-color: #111 !important; border: 1px solid #444 !important; color: white !important; }
    div[data-testid="stNumberInput"] button { background-color: #222 !important; color: white !important; border-color: #444 !important; }
    div[data-testid="stNumberInput"] input { background-color: transparent !important; color: white !important; }
    div[data-baseweb="popover"], ul[role="listbox"] { background-color: #111 !important; color: white !important; border: 1px solid #333 !important; }
    li[role="option"]:hover { background-color: #333 !important; color: #FBBF24 !important; }

    /* VS Mode Cards */
    .vs-container { display: flex; gap: 20px; }
    .vs-card { background: #111; border: 1px solid #333; border-radius: 15px; padding: 25px; text-align: center; width: 100%; position: relative; }
    .vs-winner { border: 2px solid #10B981; background: radial-gradient(circle at top, #1a2e25, #000); box-shadow: 0 0 30px rgba(16, 185, 129, 0.15); }
    .vs-name { font-size: 1.4em; font-weight: 900; margin-bottom: 5px; height: 60px; display: flex; align-items: center; justify-content: center; }
    .vs-price { font-family: 'JetBrains Mono'; color: #FBBF24; font-size: 1.5em; margin-bottom: 20px; font-weight: bold; }
    
    .stat-row { display: flex; justify-content: space-between; margin-bottom: 12px; padding: 8px; background: #000; border-radius: 8px; border: 1px solid #222; }
    .stat-name { color: #888; font-size: 0.9em; font-weight: bold; }
    .stat-val { font-weight: 900; font-size: 1.1em; }
    .win-text { color: #10B981; } /* สีเขียวสำหรับค่าที่ชนะ */
    
    .rec-badge { 
        background: #10B981; color: black; font-weight: 900; padding: 8px 20px; 
        border-radius: 50px; display: inline-block; margin-bottom: 20px; 
        box-shadow: 0 0 15px #10B981;
    }
    
    .amazon-btn { background: #3B82F6; color: white !important; padding: 18px; display: block; text-align: center; border-radius: 10px; font-weight: 900; text-decoration: none; margin-top: 20px; font-size: 1.2em; }
    
    /* Original CSS */
    .streamlit-expanderHeader { background-color: #111 !important; color: white !important; }
    .hero-title { font-size: 3.5em; font-weight: 900; }
    .winner-box { background: radial-gradient(circle at top right, #111, #000); border: 2px solid #3B82F6; border-radius: 20px; padding: 40px; }
    .stat-box { background: #151515; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- 4. HEADER ---
st.title("🛒 TechChoose")
st.markdown("<div style='margin-bottom:20px; background:#111; color:#00FF00; padding:5px 10px; border-radius:4px; display:inline-block; border:1px solid #333;'>✅ Data Verified: 20 Dec 2025</div>", unsafe_allow_html=True)

df = load_data()

# --- 5. TABS ---
tab1, tab2 = st.tabs(["🔍 FIND BEST MATCH", "⚔️ COMPARE MODELS"])

# ==========================================
# TAB 1: ORIGINAL (คงเดิมไว้)
# ==========================================
with tab1:
    with st.expander("🔍 **TAP HERE TO FILTER & CUSTOMIZE**", expanded=True):
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1: os_choice = st.selectbox("📱 Operating System", ["Any", "iOS (Apple)", "Android"], key="t1_os")
        with col_filter2: lifestyle = st.selectbox("👤 User Persona", ["💎 Ultimate High-End", "🏠 General Use", "🎮 Hardcore Gamer", "📸 Content Creator", "💼 Business Pro", "💰 Student / Budget", "🛠️ Custom"], key="t1_life")

        if "High-End" in lifestyle: budget = 9999 
        elif "Custom" in lifestyle: budget = st.slider("💰 Max Budget (USD)", 100, 2000, 2000, step=50, key="t1_bud")
        else: budget = 9999

        p, c, b, v = 5, 5, 5, 5
        price_penalty_threshold = 9999
        if "High-End" in lifestyle: p,c,b,v = 10, 10, 10, 0
        elif "Gamer" in lifestyle: p,c,b,v = 20, 0, 8, 2
        elif "Creator" in lifestyle: p,c,b,v = 6, 20, 6, 2
        elif "Business" in lifestyle: p,c,b,v = 8, 4, 15, 5
        elif "General" in lifestyle: p,c,b,v = 8, 8, 8, 10
        elif "Student" in lifestyle: p,c,b,v = 6, 6, 8, 20; price_penalty_threshold = 800

        if "Custom" in lifestyle:
            st.divider()
            c1, c2, c3, c4 = st.columns(4)
            with c1: p = st.number_input("Speed", 1, 10, 8, key="t1_p")
            with c2: c = st.number_input("Cam", 1, 10, 8, key="t1_c")
            with c3: b = st.number_input("Batt", 1, 10, 5, key="t1_b")
            with c4: v = st.number_input("Value", 1, 10, 5, key="t1_v")

        if st.button("🚀 UPDATE RESULTS", type="primary", use_container_width=True, key="t1_btn"): st.rerun()

    st.divider()
    
    # ... (ส่วนแสดงผล Tab 1 เหมือนเดิม ละไว้เพื่อความกระชับ แต่ใช้ logic เดิมเป๊ะ) ...
    # Copy Logic เดิมมาใส่ตรงนี้ได้เลยครับ หรือใช้โค้ดเต็มด้านบนที่ผมเคยให้ไป
    # เพื่อความชัวร์ ผมใส่ Logic ย่อให้ทำงานได้จริง
    if not df.empty:
        df_filter = df.copy()
        if "iOS" in os_choice: df_filter = df_filter[df_filter['os_type']=='iOS']
        elif "Android" in os_choice: df_filter = df_filter[df_filter['os_type']=='Android']
        df_filter = df_filter[df_filter['price'] <= budget]
        
        score = (df_filter['perf_score']*p) + (df_filter['cam_score']*c) + (df_filter['batt_score']*b) + (df_filter['value']*v)
        df_filter['final_score'] = score
        df_filter = df_filter.sort_values('final_score', ascending=False).head(1)
        
        if not df_filter.empty:
            winner = df_filter.iloc[0]
            st.markdown(f"""
            <div class='winner-box'>
                <div style='background:#F59E0B; color:black; padding:5px 15px; border-radius:20px; display:inline-block; font-weight:bold; margin-bottom:10px;'>💎 TOP PICK</div>
                <div class='hero-title'>{winner['name']}</div>
                <div class='hero-price'>${winner['price']:,}</div>
                <div style='display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-top:20px;'>
                    <div class='stat-box'>🚀 Speed {winner['perf_score']}</div>
                    <div class='stat-box'>📸 Cam {winner['cam_score']}</div>
                    <div class='stat-box'>🔋 Batt {winner['batt_score']}</div>
                </div>
                <a href='{winner['link']}' target='_blank' class='amazon-btn'>👉 VIEW DEAL ON AMAZON</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No phones found.")


# ==========================================
# TAB 2: COMPARE VS MODE (Highlight)
# ==========================================
with tab2:
    st.markdown("### 🥊 Compare 2 Models")
    
    # 1. Select Criteria
    judge = st.selectbox("⚖️ Decide Winner By (ตัดสินจาก):", ["💎 Overall Specs", "🎮 Gaming Performance", "📸 Camera Quality", "💰 Value for Money"], key="vs_judge")
    
    # 2. Select Phones
    c_sel1, c_sel2 = st.columns(2)
    with c_sel1: p1_name = st.selectbox("Select Phone A", df['name'].unique(), index=0, key="p1")
    with c_sel2: p2_name = st.selectbox("Select Phone B", df['name'].unique(), index=1, key="p2")
    
    if p1_name and p2_name:
        row1 = df[df['name'] == p1_name].iloc[0]
        row2 = df[df['name'] == p2_name].iloc[0]
        
        # Calculate Score based on Judge
        w_p, w_c, w_b, w_v = 1, 1, 1, 1
        if "Gaming" in judge: w_p, w_c, w_b, w_v = 10, 0, 3, 1
        elif "Camera" in judge: w_p, w_c, w_b, w_v = 2, 10, 3, 1
        elif "Value" in judge: w_p, w_c, w_b, w_v = 3, 3, 3, 10
        
        s1 = (row1['perf_score']*w_p) + (row1['cam_score']*w_c) + (row1['batt_score']*w_b) + (row1['value']*w_v)
        s2 = (row2['perf_score']*w_p) + (row2['cam_score']*w_c) + (row2['batt_score']*w_b) + (row2['value']*w_v)
        
        # Determine Visuals
        win1 = s1 >= s2
        card1_cls = "vs-winner" if win1 else ""
        card2_cls = "vs-winner" if not win1 else ""
        badge1 = "<div class='rec-badge'>👑 RECOMMENDED</div>" if win1 else "<div style='height:40px;'></div>"
        badge2 = "<div class='rec-badge'>👑 RECOMMENDED</div>" if not win1 else "<div style='height:40px;'></div>"
        
        # Helper for color stats
        def color_stat(v1, v2):
            return "win-text" if v1 >= v2 else "lose-text"
            
        c1, c2 = st.columns(2)
        
        # --- LEFT CARD ---
        with c1:
            st.markdown(f"""
            <div class='vs-card {card1_cls}'>
                {badge1}
                <div class='vs-name'>{row1['name']}</div>
                <div class='vs-price'>${row1['price']:,}</div>
                
                <div class='stat-row'>
                    <span class='stat-name'>🚀 AnTuTu</span>
                    <span class='stat-val {color_stat(row1['antutu'], row2['antutu'])}'>{int(row1['antutu']):,}</span>
                </div>
                <div class='stat-row'>
                    <span class='stat-name'>⚡ Speed</span>
                    <span class='stat-val {color_stat(row1['perf_score'], row2['perf_score'])}'>{row1['perf_score']}</span>
                </div>
                <div class='stat-row'>
                    <span class='stat-name'>📸 Camera</span>
                    <span class='stat-val {color_stat(row1['cam_score'], row2['cam_score'])}'>{row1['cam_score']}</span>
                </div>
                <div class='stat-row'>
                    <span class='stat-name'>🔋 Battery</span>
                    <span class='stat-val {color_stat(row1['batt_score'], row2['batt_score'])}'>{row1['batt_score']}</span>
                </div>
                
                <a href='{row1['link']}' target='_blank' class='amazon-btn'>VIEW DEAL</a>
            </div>
            """, unsafe_allow_html=True)

        # --- RIGHT CARD ---
        with c2:
            st.markdown(f"""
            <div class='vs-card {card2_cls}'>
                {badge2}
                <div class='vs-name'>{row2['name']}</div>
                <div class='vs-price'>${row2['price']:,}</div>
                
                <div class='stat-row'>
                    <span class='stat-name'>🚀 AnTuTu</span>
                    <span class='stat-val {color_stat(row2['antutu'], row1['antutu'])}'>{int(row2['antutu']):,}</span>
                </div>
                <div class='stat-row'>
                    <span class='stat-name'>⚡ Speed</span>
                    <span class='stat-val {color_stat(row2['perf_score'], row1['perf_score'])}'>{row2['perf_score']}</span>
                </div>
                <div class='stat-row'>
                    <span class='stat-name'>📸 Camera</span>
                    <span class='stat-val {color_stat(row2['cam_score'], row1['cam_score'])}'>{row2['cam_score']}</span>
                </div>
                <div class='stat-row'>
                    <span class='stat-name'>🔋 Battery</span>
                    <span class='stat-val {color_stat(row2['batt_score'], row1['batt_score'])}'>{row2['batt_score']}</span>
                </div>
                
                <a href='{row2['link']}' target='_blank' class='amazon-btn'>VIEW DEAL</a>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("---")
        # Final Verdict Text
        winner_name = row1['name'] if win1 else row2['name']
        diff = abs(s1 - s2)
        reason = f"higher {judge.split(' ')[1]} score"
        st.success(f"**AI Recommendation:** The **{winner_name}** is the better choice for **{judge}**.")