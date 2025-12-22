import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Ultimate VS",
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
        # OS Logic
        def get_os(name):
            name_str = str(name).lower()
            if 'iphone' in name_str or 'ipad' in name_str: return 'iOS'
            return 'Android'
        df['os_type'] = df['name'].apply(get_os)
        
        # Normalize Scores
        if 'antutu' in df.columns:
            df['perf_score'] = (df['antutu'] / 3500000) * 10 
            df['perf_score'] = df['perf_score'].clip(upper=10)
        else: df['perf_score'] = 8.0 
        
        if 'camera' in df.columns: df['cam_score'] = df['camera']
        if 'battery' in df.columns: df['batt_score'] = df['battery']
        if 'antutu' not in df.columns: df['antutu'] = df['price'] * 2000

        # Affiliate Link
        my_tag = "techchoose-20"
        df['link'] = df['link'].apply(lambda x: f"{x}&tag={my_tag}" if '?' in str(x) else f"{x}?tag={my_tag}")

    return df

# --- 3. CSS (Ultra Dark + Tabs + Compare UI) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Inter:wght@400;600;900&display=swap');
    
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }

    /* Tabs Styling */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #888 !important;
        font-weight: 700 !important;
        font-size: 1.2em !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: white !important;
        border-bottom: 3px solid #3B82F6 !important;
    }
    
    /* Input Fixes (Black Theme) */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #111 !important;
        border: 1px solid #444 !important;
        color: white !important;
    }
    div[data-baseweb="select"] span, input { color: white !important; }
    div[data-baseweb="popover"], ul[role="listbox"] {
        background-color: #111 !important; color: white !important;
    }
    li[role="option"]:hover { background-color: #333 !important; color: #FBBF24 !important; }

    /* Compare Cards */
    .vs-card {
        background: #111; border: 1px solid #333; border-radius: 15px; padding: 20px; text-align: center;
    }
    .vs-winner {
        border: 2px solid #10B981; box-shadow: 0 0 30px rgba(16, 185, 129, 0.2);
        background: radial-gradient(circle at top, #1a2e25, #111);
    }
    .vs-name { font-size: 1.5em; font-weight: 900; margin-bottom: 5px; }
    .vs-price { font-family: 'JetBrains Mono'; color: #FBBF24; font-size: 1.3em; margin-bottom: 15px; }
    
    .win-badge {
        background: #10B981; color: black; font-weight: bold; padding: 5px 15px; border-radius: 20px;
        display: inline-block; margin-bottom: 10px; font-size: 0.8em;
    }

    /* Common UI */
    .stat-box { background: #000; padding: 8px; border-radius: 6px; margin-bottom: 5px; border: 1px solid #222; }
    .amazon-btn { background: #3B82F6; color: white !important; padding: 15px; display: block; text-align: center; border-radius: 8px; font-weight: 900; text-decoration: none; margin-top: 15px; }
    
    .update-badge { background-color: #111; border: 1px solid #333; color: #00FF00; padding: 5px 10px; border-radius: 4px; font-size: 0.8em; display: inline-block; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# --- 4. HEADER & LOGIC SETUP ---
st.title("🛒 TechChoose")
st.markdown("<div class='update-badge'>✅ Data Verified: 20 Dec 2025</div>", unsafe_allow_html=True)

df = load_data()

# --- 5. TABS SYSTEM ---
tab1, tab2 = st.tabs(["🔍 FIND BEST MATCH", "⚔️ COMPARE TWO MODELS"])

# ==========================================
# TAB 1: FIND BEST MATCH (Original Mode)
# ==========================================
with tab1:
    with st.expander("⚙️ **FILTER & CUSTOMIZE**", expanded=True):
        c1, c2 = st.columns(2)
        with c1: os_choice = st.selectbox("📱 Operating System", ["Any", "iOS", "Android"], key="os1")
        with c2: lifestyle = st.selectbox("👤 User Persona", ["💎 Ultimate High-End", "🏠 General Use", "🎮 Hardcore Gamer", "📸 Content Creator", "💰 Student / Budget", "🛠️ Custom"], key="life1")
        
        # Logic Setting
        p, c, b, v = 5, 5, 5, 5
        price_limit = 9999
        if "High-End" in lifestyle: p,c,b,v = 10,10,10,0
        elif "Gamer" in lifestyle: p,c,b,v = 20,0,8,2
        elif "Creator" in lifestyle: p,c,b,v = 6,20,6,2
        elif "Student" in lifestyle: p,c,b,v = 6,6,8,20; price_limit = 800
        
        if "Custom" in lifestyle:
            st.divider()
            cc1, cc2, cc3, cc4 = st.columns(4)
            with cc1: p = st.number_input("Speed", 1, 10, 8)
            with cc2: c = st.number_input("Cam", 1, 10, 8)
            with cc3: b = st.number_input("Batt", 1, 10, 5)
            with cc4: v = st.number_input("Value", 1, 10, 5)

        if st.button("🚀 FIND MY PHONE", type="primary", use_container_width=True):
            st.rerun()

    if not df.empty:
        # Filter & Calculate
        filtered_df = df.copy()
        if "iOS" in os_choice: filtered_df = filtered_df[filtered_df['os_type']=='iOS']
        elif "Android" in os_choice: filtered_df = filtered_df[filtered_df['os_type']=='Android']
        filtered_df = filtered_df[filtered_df['price'] <= price_limit]
        
        filtered_df['score'] = (filtered_df['perf_score']*p) + (filtered_df['cam_score']*c) + (filtered_df['batt_score']*b) + (filtered_df['value']*v)
        filtered_df = filtered_df.sort_values('score', ascending=False).head(5)
        
        if not filtered_df.empty:
            top = filtered_df.iloc[0]
            st.markdown(f"""
            <div class='vs-card vs-winner' style='margin-top:20px;'>
                <div class='win-badge'>🏆 BEST CHOICE FOR YOU</div>
                <div class='vs-name'>{top['name']}</div>
                <div class='vs-price'>${top['price']:,}</div>
                <div style='display:flex; justify-content:space-around; margin-bottom:15px;'>
                    <div>🚀 {top['perf_score']}/10</div>
                    <div>📸 {top['cam_score']}/10</div>
                    <div>🔋 {top['batt_score']}/10</div>
                </div>
                <a href='{top['link']}' target='_blank' class='amazon-btn'>👉 VIEW DEAL</a>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            st.caption("🥈 Runner Ups:")
            for i, row in filtered_df.iloc[1:].iterrows():
                st.info(f"{i}. **{row['name']}** - ${row['price']:,}")

# ==========================================
# TAB 2: COMPARE TWO MODELS (New Feature!)
# ==========================================
with tab2:
    st.write("### 🥊 Head-to-Head Comparison")
    st.write("Select two models to see which one fits your persona better.")
    
    # 1. Select Persona for Judging
    judge_mode = st.selectbox("⚖️ Judging Criteria (ตัดสินจากมุมมองไหน)", ["💎 Overall Power", "🎮 Gaming", "📸 Photography", "💰 Value"], key="judge")
    
    # Define Weights based on Judge Mode
    jp, jc, jb, jv = 1,1,1,1
    if "Gaming" in judge_mode: jp, jc, jb, jv = 20, 0, 5, 2
    elif "Photo" in judge_mode: jp, jc, jb, jv = 5, 20, 5, 2
    elif "Value" in judge_mode: jp, jc, jb, jv = 5, 5, 5, 20
    
    col_a, col_b = st.columns(2)
    with col_a:
        model_a_name = st.selectbox("Phone A (Left)", df['name'].unique(), index=0)
    with col_b:
        # Try to set default to index 1 if exists
        idx_b = 1 if len(df) > 1 else 0
        model_b_name = st.selectbox("Phone B (Right)", df['name'].unique(), index=idx_b)

    if model_a_name and model_b_name:
        # Get Data
        row_a = df[df['name'] == model_a_name].iloc[0]
        row_b = df[df['name'] == model_b_name].iloc[0]
        
        # Calculate Scores
        score_a = (row_a['perf_score']*jp) + (row_a['cam_score']*jc) + (row_a['batt_score']*jb) + (row_a['value']*jv)
        score_b = (row_b['perf_score']*jp) + (row_b['cam_score']*jc) + (row_b['batt_score']*jb) + (row_b['value']*jv)
        
        # Determine Winner
        a_class = "vs-winner" if score_a >= score_b else ""
        b_class = "vs-winner" if score_b > score_a else ""
        a_badge = "<div class='win-badge'>👑 WINNER</div>" if score_a >= score_b else ""
        b_badge = "<div class='win-badge'>👑 WINNER</div>" if score_b > score_a else ""

        # Display Side-by-Side
        c1, c2 = st.columns(2)
        
        # --- LEFT CARD ---
        with c1:
            st.markdown(f"""
            <div class='vs-card {a_class}'>
                {a_badge}
                <div class='vs-name'>{row_a['name']}</div>
                <div class='vs-price'>${row_a['price']:,}</div>
                <div class='stat-box'>🚀 Speed: {row_a['perf_score']}</div>
                <div class='stat-box'>📸 Cam: {row_a['cam_score']}</div>
                <div class='stat-box'>🔋 Batt: {row_a['batt_score']}</div>
                <a href='{row_a['link']}' target='_blank' class='amazon-btn'>VIEW DEAL</a>
            </div>
            """, unsafe_allow_html=True)

        # --- RIGHT CARD ---
        with c2:
            st.markdown(f"""
            <div class='vs-card {b_class}'>
                {b_badge}
                <div class='vs-name'>{row_b['name']}</div>
                <div class='vs-price'>${row_b['price']:,}</div>
                <div class='stat-box'>🚀 Speed: {row_b['perf_score']}</div>
                <div class='stat-box'>📸 Cam: {row_b['cam_score']}</div>
                <div class='stat-box'>🔋 Batt: {row_b['batt_score']}</div>
                <a href='{row_b['link']}' target='_blank' class='amazon-btn'>VIEW DEAL</a>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("---")
        if score_a > score_b:
            st.success(f"**AI Verdict:** Based on **{judge_mode}**, the **{row_a['name']}** is the better choice.")
        elif score_b > score_a:
            st.success(f"**AI Verdict:** Based on **{judge_mode}**, the **{row_b['name']}** is the better choice.")
        else:
            st.info("It's a Tie! Both are equally good for this criteria.")