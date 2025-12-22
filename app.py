import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Final Tabs",
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
        if 'award' not in df.columns: df['award'] = "Top Pick"
        if 'antutu' not in df.columns: df['antutu'] = df['price'] * 2000

        # Affiliate Link
        my_tag = "techchoose-20"
        df['link'] = df['link'].apply(lambda x: f"{x}&tag={my_tag}" if '?' in str(x) else f"{x}?tag={my_tag}")

    return df

# --- 3. CSS (Original Dark Style + Tabs) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Inter:wght@400;600;900&display=swap');
    
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }

    /* 🔥 Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #000;
        padding-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #111;
        border-radius: 5px;
        color: #888;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #222 !important;
        color: #3B82F6 !important; /* สีฟ้า */
        border: 1px solid #333;
    }

    /* 🔥 Original Styles */
    .streamlit-expanderHeader { background-color: #111 !important; color: white !important; border: 1px solid #333 !important; }
    div[data-testid="stExpander"] details { background-color: #111 !important; border-color: #333 !important; }
    div[data-testid="stExpander"] summary { background-color: #222 !important; color: white !important; }
    div[data-testid="stExpander"] summary:hover { color: #FBBF24 !important; }
    div[data-testid="stExpander"] * { color: white !important; }
    div[data-testid="stExpander"] svg { fill: white !important; }

    label[data-testid="stWidgetLabel"] p { color: #FFFFFF !important; font-size: 1.1rem !important; font-weight: 700 !important; }
    
    div[data-baseweb="select"] > div { background-color: #111 !important; border: 1px solid #444 !important; color: white !important; }
    div[data-baseweb="select"] span { color: white !important; }
    div[data-baseweb="select"] svg { fill: white !important; }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] { background-color: #111 !important; color: white !important; border: 1px solid #333 !important; }
    li[role="option"] { color: white !important; background-color: #111 !important; }
    li[role="option"]:hover, li[role="option"][aria-selected="true"] { background-color: #333 !important; color: #FBBF24 !important; }
    
    /* Input & Buttons Fix */
    div[data-testid="stNumberInput"] div[data-baseweb="input"] { background-color: #111 !important; border: 1px solid #444 !important; color: white !important; }
    div[data-testid="stNumberInput"] input { background-color: transparent !important; color: white !important; }
    div[data-testid="stNumberInput"] button { background-color: #222 !important; color: white !important; border-color: #444 !important; }
    div[data-baseweb="input"] > div { background-color: #111 !important; }

    /* Responsive */
    .hero-title { font-size: 3.5em; font-weight: 900; color: white; line-height: 1.1; margin-bottom: 10px; }
    .hero-price { color: #FBBF24; font-size: 3em; font-weight: 800; font-family: 'JetBrains Mono'; margin-bottom: 5px; }

    @media only screen and (max-width: 1024px) {
        .hero-title { font-size: 2.5em !important; }
        .hero-price { font-size: 2.5em !important; }
        .amazon-btn { padding: 18px !important; font-size: 1.2em !important; }
    }
    @media only screen and (max-width: 600px) {
        .hero-title { font-size: 2.0em !important; }
        .hero-price { font-size: 2.0em !important; }
        .winner-box { padding: 20px !important; }
    }
    
    .update-badge { background-color: #111; border: 1px solid #333; color: #00FF00; padding: 5px 10px; border-radius: 4px; font-size: 0.8em; display: inline-block; margin-bottom: 15px; }
    .winner-box { background: radial-gradient(circle at top right, #111, #000); border: 2px solid #3B82F6; border-radius: 20px; padding: 40px; box-shadow: 0 0 60px rgba(59, 130, 246, 0.25); }
    .award-badge { background: #F59E0B; color: black; font-weight: 900; padding: 8px 16px; border-radius: 50px; text-transform: uppercase; display: inline-block; margin-bottom: 15px; font-size: 0.8em; letter-spacing: 1px; }
    .expert-verdict { background: #111; border-left: 5px solid #3B82F6; padding: 15px; border-radius: 0 12px 12px 0; margin-bottom: 25px; color: #E0E0E0; line-height: 1.5; font-size: 0.9em; }
    
    .stat-container { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 25px; }
    .stat-box { background: #151515; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #333; }
    .stat-label { color: #888; font-size: 0.7em; font-weight: 700; margin-bottom: 5px; text-transform: uppercase; }
    .stat-val { font-size: 1.2em; font-weight: 900; color: white; }
    .bar-bg { background: #333; height: 4px; border-radius: 2px; margin-top: 5px; overflow: hidden; }
    
    .amazon-btn { background: #3B82F6; color: white !important; padding: 22px; display: block; text-align: center; border-radius: 12px; font-weight: 900; text-decoration: none; font-size: 1.4em; margin-top: 20px; transition: 0.3s; }
    .deal-hint { text-align: center; color: #10B981; font-size: 0.9em; margin-top: 10px; font-weight: bold; }

    .alt-link { text-decoration: none; display: block; }
    .alt-row { background: #0A0A0A; border: 1px solid #222; padding: 15px; border-radius: 12px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }
    .rank-wrap { display: flex; align-items: center; gap: 12px; }
    .rank-circle { width: 28px; height: 28px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 900; background: #222; border: 1px solid #444; color: #888; }
    .rank-silver { background: linear-gradient(135deg, #E0E0E0, #999); color: black; border: none; }
    .rank-bronze { background: linear-gradient(135deg, #CD7F32, #8B4513); color: white; border: none; }
    
    .reason-badge { font-size: 0.7em; font-weight: bold; text-transform: uppercase; padding: 2px 6px; border-radius: 4px; margin-left: 5px; vertical-align: middle; }
    .reason-green { background: rgba(16, 185, 129, 0.2); color: #10B981; border: 1px solid #10B981; }
    .reason-purple { background: rgba(168, 85, 247, 0.2); color: #A855F7; border: 1px solid #A855F7; }
    .reason-gray { background: #222; color: #BBB; border: 1px solid #444; }

    .mini-bar-container { display: flex; gap: 4px; margin-top: 6px; }
    .mini-stat { width: 30px; }
    .mini-track { width: 100%; height: 3px; background: #333; border-radius: 2px; }
    .mini-fill-blue { height: 100%; background: #3B82F6; } .mini-fill-purple { height: 100%; background: #A855F7; } .mini-fill-green { height: 100%; background: #10B981; }
    .disclaimer-box { margin-top: 50px; padding: 20px; border-top: 1px solid #222; text-align: center; color: #555; font-size: 0.8em; }
    
    /* VS Tab Specific */
    .vs-card { background: #111; border: 1px solid #333; border-radius: 15px; padding: 20px; text-align: center; height: 100%; }
    .vs-winner-border { border: 2px solid #10B981; box-shadow: 0 0 20px rgba(16, 185, 129, 0.2); }
</style>
""", unsafe_allow_html=True)

# --- 4. HEADER ---
st.title("🛒 TechChoose")
st.markdown("<div class='update-badge'>✅ Data Verified: 20 Dec 2025</div>", unsafe_allow_html=True)

df = load_data()

# --- 5. TABS ---
tab1, tab2 = st.tabs(["🔍 FIND BEST MATCH", "⚔️ COMPARE MODELS"])

# ==========================================
# TAB 1: ORIGINAL APP (หน้าเดิมที่พี่ชอบ)
# ==========================================
with tab1:
    with st.expander("🔍 **TAP HERE TO FILTER & CUSTOMIZE**", expanded=True):
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            os_choice = st.selectbox("📱 Operating System", ["Any", "iOS (Apple)", "Android"])
        with col_filter2:
            lifestyle = st.selectbox("👤 User Persona", ["💎 Ultimate High-End", "🏠 General Use", "🎮 Hardcore Gamer", "📸 Content Creator", "💼 Business Pro", "💰 Student / Budget", "🛠️ Custom"])

        if "High-End" in lifestyle: budget = 9999 
        elif "Custom" in lifestyle: budget = st.slider("💰 Max Budget (USD)", 100, 2000, 2000, step=50)
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
            with c1: p = st.number_input("Speed", 1, 10, 8)
            with c2: c = st.number_input("Cam", 1, 10, 8)
            with c3: b = st.number_input("Batt", 1, 10, 5)
            with c4: v = st.number_input("Value", 1, 10, 5)

        if st.button("🚀 UPDATE RESULTS", type="primary", use_container_width=True): st.rerun()

    st.divider()

    # Functions (Original)
    def get_dynamic_badge(mode, price):
        if "High-End" in mode: return "💎 ABSOLUTE BEST"
        elif "Gamer" in mode: return "🏆 GAMING BEAST"
        elif "Creator" in mode: return "🎥 CREATOR CHOICE"
        elif "Student" in mode: return "💰 SMART SAVER"
        elif "Business" in mode: return "💼 WORKHORSE"
        elif "General" in mode: return "⭐ BALANCED PICK"
        else: return "⭐ TOP FLAGSHIP"

    def get_expert_verdict(row, mode):
        if "Gamer" in mode: return f"Built for speed. <b>AnTuTu {int(row['antutu']):,}</b>."
        return f"Excellent choice based on your preferences."

    def stat_bar_html(label, score, color):
        return f"<div class='stat-box'><div class='stat-label'>{label}</div><div class='stat-val'>{score:.1f}/10</div><div class='bar-bg'><div style='width:{score*10}%; height:100%; background:{color};'></div></div></div>"

    if not df.empty:
        if "iOS" in os_choice: df_filter = df[df['os_type'] == 'iOS']
        elif "Android" in os_choice: df_filter = df[df['os_type'] == 'Android']
        else: df_filter = df.copy()
        
        df_filter = df_filter[df_filter['price'] <= budget]

        base_score = (df_filter['perf_score']*p) + (df_filter['cam_score']*c) + (df_filter['batt_score']*b) + (df_filter['value']*v)
        price_penalty = df_filter['price'].apply(lambda x: (x - price_penalty_threshold) * 0.5 if x > price_penalty_threshold else 0)
        df_filter['final_score'] = base_score - price_penalty
        max_possible = (10*p) + (10*c) + (10*b) + (10*v)
        df_filter['match'] = (df_filter['final_score'] / max_possible) * 100
        df_filter = df_filter.sort_values(by='match', ascending=False).reset_index(drop=True)

        if len(df_filter) > 0:
            winner = df_filter.iloc[0]
            current_badge = get_dynamic_badge(lifestyle, winner['price'])
            
            # HTML Rendering
            stats_html = f"{stat_bar_html('🚀 SPEED', winner['perf_score'], '#3B82F6')}{stat_bar_html('📸 CAM', winner['cam_score'], '#A855F7')}{stat_bar_html('🔋 BATT', winner['batt_score'], '#10B981')}"
            btn_section = f"""<a href='{winner['link']}' target='_blank' class='amazon-btn'>👉 VIEW DEAL ON AMAZON</a><div class='deal-hint'>⚡ Check today's price</div>"""
            
            winner_html = f"""<div class='winner-box'><div class='award-badge'>{current_badge}</div><div class='hero-title'>{winner['name']}</div><div class='hero-price'>${winner['price']:,}</div><div class='expert-verdict'>{get_expert_verdict(winner, lifestyle)}</div><div class='stat-container'>{stats_html}</div>{btn_section}</div>"""
            st.markdown(winner_html, unsafe_allow_html=True)

            st.write("")
            st.markdown("### 🥈 Top Alternatives")
            for i, row in df_filter.iloc[1:6].iterrows():
                rank_num = i + 1
                rank_badge = f"<div class='rank-circle'>{rank_num}</div>"
                if rank_num == 2: rank_badge = "<div class='rank-circle rank-silver'>2</div>"
                if rank_num == 3: rank_badge = "<div class='rank-circle rank-bronze'>3</div>"

                mini_bars = f"""<div class='mini-bar-container'><div class='mini-stat'><div class='mini-track'><div class='mini-fill-blue' style='width:{row['perf_score']*10}%;'></div></div></div><div class='mini-stat'><div class='mini-track'><div class='mini-fill-purple' style='width:{row['cam_score']*10}%;'></div></div></div><div class='mini-stat'><div class='mini-track'><div class='mini-fill-green' style='width:{row['batt_score']*10}%;'></div></div></div></div>"""
                
                alt_html = f"""
                <a href="{row['link']}" target="_blank" class="alt-link">
                    <div class="alt-row">
                        <div class="rank-wrap">
                            {rank_badge} 
                            <div>
                                <div style="font-weight:bold; font-size:1em; color:white;">{row['name']}</div>
                                <div style="color:#FBBF24; font-weight:bold; font-size:0.9em;">${row['price']:,}</div>
                                {mini_bars}
                            </div>
                        </div>
                        <div style="text-align:right">
                            <div style="font-size:1.1em; font-weight:900; color:#3B82F6;">{row['match']:.0f}%</div>
                            <div style="color:#FBBF24; font-size:0.7em; font-weight:bold;">VIEW ></div>
                        </div>
                    </div>
                </a>"""
                st.markdown(alt_html, unsafe_allow_html=True)
            st.markdown("""<div class='disclaimer-box'>TechChoose is a participant in the Amazon Services LLC Associates Program.</div>""", unsafe_allow_html=True)
        else:
            st.warning(f"No devices found under ${budget}.")
    else:
        st.error("Database Error.")

# ==========================================
# TAB 2: VS MODE (อันใหม่ แยกมาอยู่หน้านี้)
# ==========================================
with tab2:
    st.write("### 🥊 Head-to-Head Comparison")
    
    # Simple Selectors
    judge_mode = st.selectbox("⚖️ Criteria (เกณฑ์ตัดสิน)", ["💎 Overall Power", "🎮 Gaming", "📸 Photography", "💰 Value"], key="judge_tab2")
    
    col_a, col_b = st.columns(2)
    with col_a: model_a = st.selectbox("Left Side", df['name'].unique(), index=0, key="a")
    with col_b: model_b = st.selectbox("Right Side", df['name'].unique(), index=1, key="b")
    
    if model_a and model_b:
        row_a = df[df['name'] == model_a].iloc[0]
        row_b = df[df['name'] == model_b].iloc[0]
        
        # Calculate Logic
        jp, jc, jb, jv = 1,1,1,1
        if "Gaming" in judge_mode: jp, jc, jb, jv = 20, 0, 5, 2
        elif "Photo" in judge_mode: jp, jc, jb, jv = 5, 20, 5, 2
        elif "Value" in judge_mode: jp, jc, jb, jv = 5, 5, 5, 20
        
        score_a = (row_a['perf_score']*jp) + (row_a['cam_score']*jc) + (row_a['batt_score']*jb) + (row_a['value']*jv)
        score_b = (row_b['perf_score']*jp) + (row_b['cam_score']*jc) + (row_b['batt_score']*jb) + (row_b['value']*jv)
        
        border_a = "vs-winner-border" if score_a >= score_b else ""
        border_b = "vs-winner-border" if score_b > score_a else ""
        badge_a = "<div style='color:#10B981; font-weight:bold;'>👑 WINNER</div>" if score_a >= score_b else ""
        badge_b = "<div style='color:#10B981; font-weight:bold;'>👑 WINNER</div>" if score_b > score_a else ""
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class='vs-card {border_a}'>
                {badge_a}
                <div style='font-size:1.2em; font-weight:bold; margin-top:5px;'>{row_a['name']}</div>
                <div style='color:#FBBF24;'>${row_a['price']:,}</div>
                <hr style='border-color:#333;'>
                <div>🚀 {row_a['perf_score']} | 📸 {row_a['cam_score']}</div>
                <a href='{row_a['link']}' target='_blank' class='amazon-btn'>VIEW</a>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div class='vs-card {border_b}'>
                {badge_b}
                <div style='font-size:1.2em; font-weight:bold; margin-top:5px;'>{row_b['name']}</div>
                <div style='color:#FBBF24;'>${row_b['price']:,}</div>
                <hr style='border-color:#333;'>
                <div>🚀 {row_b['perf_score']} | 📸 {row_b['cam_score']}</div>
                <a href='{row_b['link']}' target='_blank' class='amazon-btn'>VIEW</a>
            </div>
            """, unsafe_allow_html=True)