import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Final Precision Fixed",
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
        df = df.dropna(subset=['name', 'price'])
        
        def get_os(name):
            name_str = str(name).lower()
            if 'iphone' in name_str or 'ipad' in name_str: return 'iOS'
            return 'Android'
        df['os_type'] = df['name'].apply(get_os)
        
        # Smart Score Calculation
        if 'antutu' in df.columns:
            def calc_speed(score):
                if score >= 2800000: return 10.0
                elif score >= 1500000: return 9.0 + ((score-1500000)/1300000)
                else: return 7.0 + ((score-800000)/700000)*2
            df['perf_score'] = df['antutu'].apply(calc_speed).clip(upper=10.0)
        else: df['perf_score'] = 8.0 
        
        if 'camera' in df.columns: df['cam_score'] = df['camera']
        if 'battery' in df.columns: df['batt_score'] = df['battery']
        if 'value' not in df.columns: df['value'] = 8.0
        if 'antutu' not in df.columns: df['antutu'] = df['price'] * 2000

        my_tag = "techchoose-20"
        df['link'] = df['link'].apply(lambda x: f"{x}&tag={my_tag}" if '?' in str(x) else f"{x}?tag={my_tag}")

    return df

# --- 3. HELPER FUNCTIONS ---
def get_dynamic_badge(mode, price):
    if "High-End" in mode: return "💎 ABSOLUTE BEST"
    elif "Gamer" in mode: return "🏆 GAMING BEAST"
    elif "Creator" in mode: return "🎥 CREATOR CHOICE"
    elif "Student" in mode: return "💰 SMART SAVER"
    else: return "⭐ TOP FLAGSHIP"

def get_expert_verdict(row, mode):
    if "Gamer" in mode: return f"Speed Monster: <b>AnTuTu {int(row['antutu']):,}</b>"
    return f"Excellent choice based on your preferences."

def stat_bar_html(label, score, color):
    return f"<div class='stat-box'><div class='stat-label'>{label}</div><div class='stat-val'>{score:.1f}/10</div><div class='bar-bg'><div style='width:{score*10}%; height:100%; background:{color};'></div></div></div>"

def get_reason_badge(winner_row, current_row):
    price_diff = winner_row['price'] - current_row['price']
    if price_diff >= 100:
        return f"<span class='reason-tag tag-save'>💰 SAVE ${int(price_diff):,}</span>"
    if current_row['batt_score'] > (winner_row['batt_score'] + 0.5):
        return "<span class='reason-tag tag-spec'>🔋 BETTER BATT</span>"
    if current_row['cam_score'] > (winner_row['cam_score'] + 0.5):
        return "<span class='reason-tag tag-spec'>📸 BETTER CAM</span>"
    return ""

def get_score_badge(icon, label, score):
    if score >= 9.0: 
        color = "#10B981" # Green
        border = "rgba(16, 185, 129, 0.3)"
    elif score >= 8.0: 
        color = "#3B82F6" # Blue
        border = "rgba(59, 130, 246, 0.3)"
    else: 
        color = "#F59E0B" # Orange
        border = "rgba(245, 158, 11, 0.3)"
        
    # 🔥 Compressing HTML to avoid whitespace issues
    return f"<div style='display:inline-flex;align-items:center;background:rgba(0,0,0,0.4);border:1px solid {border};border-radius:6px;padding:4px 8px;margin-right:8px;'><span style='font-size:1.1em;margin-right:5px;'>{icon}</span><span style='color:#AAA;font-size:0.7em;font-weight:700;margin-right:5px;text-transform:uppercase;'>{label}</span><span style='color:{color};font-weight:900;font-family:JetBrains Mono;font-size:0.9em;'>{score:.1f}</span></div>"

# --- 4. CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Inter:wght@400;600;900&display=swap');
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; font-family: 'Inter', sans-serif; }

    /* UI TWEAKS */
    .streamlit-expanderHeader { background-color: #111 !important; color: white !important; border: 1px solid #333 !important; }
    div[data-testid="stExpander"] { background-color: transparent !important; border: none !important; }
    div[data-testid="stExpander"] details { background-color: #111 !important; border-color: #333 !important; }
    div[data-testid="stExpander"] summary { background-color: #111 !important; color: white !important; }
    div[data-testid="stExpander"] summary:hover { color: #FBBF24 !important; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #000; padding-bottom: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #111; border-radius: 5px; color: #888; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #222 !important; color: #3B82F6 !important; border: 1px solid #333; }

    label, p, .stMarkdown { color: #FFFFFF !important; }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { background-color: #111 !important; border: 1px solid #444 !important; color: white !important; }
    div[data-baseweb="select"] span { color: white !important; }
    div[data-baseweb="popover"], ul[role="listbox"] { background-color: #111 !important; color: white !important; }
    li[role="option"] { background-color: #111 !important; color: white !important; }
    li[role="option"]:hover { background-color: #333 !important; color: #FBBF24 !important; }
    div[data-testid="stNumberInput"] button { background-color: #222 !important; color: white !important; border-color: #444 !important; }
    div[data-testid="stNumberInput"] input { background-color: transparent !important; color: white !important; }

    /* WINNER CARD */
    .winner-box {
        background: radial-gradient(circle at top right, #111, #000);
        border: 2px solid #3B82F6; border-radius: 20px; padding: 40px;
        box-shadow: 0 0 60px rgba(59, 130, 246, 0.25); margin-bottom: 30px;
    }
    .hero-title { font-size: 3em; font-weight: 900; color: white; line-height: 1.1; margin-bottom: 10px; }
    .hero-price { color: #FBBF24; font-size: 2.5em; font-weight: 800; font-family: 'JetBrains Mono'; margin-bottom: 10px; }
    .stat-box { background: #151515; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #333; }
    .stat-label { color: #888; font-size: 0.7em; font-weight: 700; margin-bottom: 5px; text-transform: uppercase; }
    .stat-val { font-size: 1.2em; font-weight: 900; color: white; }
    .bar-bg { background: #333; height: 4px; border-radius: 2px; margin-top: 5px; overflow: hidden; }
    .amazon-btn { background: #3B82F6; color: white !important; padding: 18px; display: block; text-align: center; border-radius: 12px; font-weight: 900; text-decoration: none; font-size: 1.2em; margin-top: 20px; transition: 0.3s; }
    .amazon-btn:hover { background: #2563EB; }

    /* BADGES */
    .reason-tag { font-size: 0.7em; font-weight: 800; padding: 4px 8px; border-radius: 4px; margin-left: 10px; vertical-align: middle; display: inline-block; letter-spacing: 0.5px; }
    .tag-save { background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid #10B981; }
    .tag-spec { background: rgba(59, 130, 246, 0.15); color: #3B82F6; border: 1px solid #3B82F6; }

    /* ALT CARDS */
    .alt-link { text-decoration: none !important; display: block; }
    .alt-card {
        background: #111; border: 1px solid #333; border-radius: 12px; padding: 20px; margin-bottom: 15px;
        display: flex; justify-content: space-between; align-items: center; transition: all 0.2s ease;
    }
    .alt-card:hover { border-color: #555; background: #161616; transform: translateX(5px); }
    
    .rank-box { width: 35px; height: 35px; display: flex; align-items: center; justify-content: center; font-weight: 900; border-radius: 8px; font-size: 1.2em; margin-right: 20px; }
    .rank-2 { background: linear-gradient(135deg, #E0E0E0, #999); color: black; border: 1px solid #FFF; }
    .rank-3 { background: linear-gradient(135deg, #E6AC75, #A0522D); color: black; border: 1px solid #FFD700; }
    .rank-norm { background: #222; color: #888; border: 1px solid #444; }

    .alt-info { flex-grow: 1; }
    .alt-name { color: white; font-weight: 700; font-size: 1.2em; margin-bottom: 8px; }
    .alt-price { color: #FBBF24; font-family: 'JetBrains Mono'; font-weight: bold; font-size: 1.1em; }
    
    .view-btn { color: #FF9900; font-weight: 900; font-size: 0.8em; text-transform: uppercase; letter-spacing: 1px; }

    /* VS CARD */
    .vs-card { background: #111; border: 1px solid #333; border-radius: 15px; padding: 25px; text-align: center; height: 100%; }
    .vs-winner-border { border: 2px solid #10B981; box-shadow: 0 0 30px rgba(16, 185, 129, 0.15); }
    .vs-title { font-size: 1.4em; font-weight: 900; margin-bottom: 5px; min-height: 50px; display:flex; align-items:center; justify-content:center; color: white !important;}
    .vs-price { font-family: 'JetBrains Mono'; color: #FBBF24; font-size: 1.5em; margin-bottom: 20px; font-weight: bold; }
    .vs-row { display: flex; justify-content: space-between; border-bottom: 1px solid #222; padding: 12px 0; font-size: 0.95em; color: #BBB; }
    .val-win { color: #10B981; font-weight: 900; } .val-lose { color: #555; }
    .rec-badge { background: linear-gradient(135deg, #FFD700, #F59E0B); color: black; font-weight: 900; padding: 8px 20px; border-radius: 50px; display: inline-block; margin-bottom: 20px; font-size: 0.85em; letter-spacing: 1px; box-shadow: 0 0 15px rgba(245, 158, 11, 0.4); }

    @media only screen and (max-width: 600px) {
        .hero-title { font-size: 2.0em !important; }
        .alt-card { flex-direction: column; align-items: flex-start; }
        .view-btn { margin-top: 10px; }
    }
</style>
""", unsafe_allow_html=True)

# --- 5. HEADER ---
st.title("🛒 TechChoose")
st.markdown("<div class='update-badge'>✅ Data Verified: 20 Dec 2025</div>", unsafe_allow_html=True)

df = load_data()

# --- 6. TABS SYSTEM ---
tab1, tab2 = st.tabs(["🔍 FIND BEST MATCH", "⚔️ COMPARE MODELS"])

# ==========================================
# TAB 1: FIND BEST MATCH
# ==========================================
with tab1:
    with st.expander("🔍 **TAP HERE TO FILTER & CUSTOMIZE**", expanded=True):
        c1, c2 = st.columns(2)
        with c1: os_choice = st.selectbox("📱 Operating System", ["Any", "iOS (Apple)", "Android"], key="t1_os")
        with c2: lifestyle = st.selectbox("👤 User Persona", ["💎 Ultimate High-End", "🏠 General Use", "🎮 Hardcore Gamer", "📸 Content Creator", "💼 Business Pro", "💰 Student / Budget", "🛠️ Custom"], key="t1_life")

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
            cc1, cc2, cc3, cc4 = st.columns(4)
            with cc1: p = st.number_input("Speed", 1, 10, 8, key="t1_p")
            with cc2: c = st.number_input("Cam", 1, 10, 8, key="t1_c")
            with cc3: b = st.number_input("Batt", 1, 10, 5, key="t1_b")
            with cc4: v = st.number_input("Value", 1, 10, 5, key="t1_v")

        if st.button("🚀 UPDATE RESULTS", type="primary", use_container_width=True, key="t1_btn"): st.rerun()

    st.divider()

    if not df.empty:
        df_f = df.copy()
        if "iOS" in os_choice: df_f = df_f[df_f['os_type']=='iOS']
        elif "Android" in os_choice: df_f = df_f[df_f['os_type']=='Android']
        df_f = df_f[df_f['price'] <= budget]
        
        score = (df_f['perf_score']*p) + (df_f['cam_score']*c) + (df_f['batt_score']*b) + (df_f['value']*v)
        price_pen = df_f['price'].apply(lambda x: (x - price_penalty_threshold) * 0.5 if x > price_penalty_threshold else 0)
        df_f['final_score'] = score - price_pen
        max_s = (10*p) + (10*c) + (10*b) + (10*v)
        df_f['match'] = (df_f['final_score'] / max_s) * 100
        df_f = df_f.sort_values('match', ascending=False).reset_index(drop=True)

        if len(df_f) > 0:
            winner = df_f.iloc[0]
            current_badge = get_dynamic_badge(lifestyle, winner['price'])
            
            stats_html = f"{stat_bar_html('🚀 SPEED', winner['perf_score'], '#3B82F6')}{stat_bar_html('📸 CAM', winner['cam_score'], '#A855F7')}{stat_bar_html('🔋 BATT', winner['batt_score'], '#10B981')}"
            
            # 🔥 FIX: One-Liner HTML
            winner_card = f"""<div class='winner-box'><div style='background:#F59E0B; color:black; padding:8px 16px; border-radius:50px; display:inline-block; font-weight:900; font-size:0.8em; margin-bottom:15px;'>{current_badge}</div><div class='hero-title'>{winner['name']}</div><div class='hero-price'>${winner['price']:,}</div><div class='expert-verdict'>{get_expert_verdict(winner, lifestyle)}</div><div class='stat-container'>{stats_html}</div><a href='{winner['link']}' target='_blank' class='amazon-btn'>👉 VIEW DEAL ON AMAZON</a><div class='deal-hint'>⚡ Check today's price</div></div>"""
            st.markdown(winner_card, unsafe_allow_html=True)

            st.write("")
            st.markdown("### 🥈 Top Alternatives")
            
            for i, row in df_f.iloc[1:6].iterrows():
                rank_num = i + 1
                
                if rank_num == 2: rank_cls = "rank-2"
                elif rank_num == 3: rank_cls = "rank-3"
                else: rank_cls = "rank-norm"
                
                reason_badge = get_reason_badge(winner, row)
                b_speed = get_score_badge("🚀", "Speed", row['perf_score'])
                b_cam = get_score_badge("📸", "Cam", row['cam_score'])
                b_batt = get_score_badge("🔋", "Batt", row['batt_score'])
                
                # 🔥 FIX: One-Liner HTML (No Indentation!)
                alt_card = f"""<a href="{row['link']}" target="_blank" class="alt-link"><div class="alt-card"><div style="display:flex; align-items:center; width:100%;"><div class="rank-box {rank_cls}">{rank_num}</div><div class="alt-info"><div class="alt-name">{row['name']} {reason_badge}</div><div class="alt-price">${row['price']:,}</div><div style="margin-top:10px;">{b_speed}{b_cam}{b_batt}</div></div><div class="view-btn">VIEW ></div></div></div></a>"""
                st.markdown(alt_card, unsafe_allow_html=True)
        else:
            st.warning("No phones found under this budget.")

# ==========================================
# TAB 2: VS MODE (STABLE)
# ==========================================
with tab2:
    st.markdown("### 🥊 Head-to-Head Comparison")
    
    judge = st.selectbox("⚖️ Decide Winner By:", ["💎 Overall Specs", "🎮 Gaming Performance", "📸 Camera Quality", "💰 Value for Money"], key="vs_judge")
    all_models = sorted(df['name'].unique())
    
    if 'p1' not in st.session_state: st.session_state.p1 = all_models[0]
    if 'p2' not in st.session_state: st.session_state.p2 = all_models[1] if len(all_models) > 1 else all_models[0]

    c1, c2 = st.columns(2)
    with c1: 
        sel_p1 = st.selectbox("Select Phone A", all_models, index=all_models.index(st.session_state.p1), key="p1_select")
        st.session_state.p1 = sel_p1
    with c2: 
        sel_p2 = st.selectbox("Select Phone B", all_models, index=all_models.index(st.session_state.p2), key="p2_select")
        st.session_state.p2 = sel_p2
    
    if st.session_state.p1 and st.session_state.p2: 
        r1 = df[df['name'] == st.session_state.p1].iloc[0]
        r2 = df[df['name'] == st.session_state.p2].iloc[0]
        
        w_p, w_c, w_b, w_v = 1, 1, 1, 1
        if "Gaming" in judge: w_p, w_c, w_b, w_v = 10, 0, 3, 1
        elif "Camera" in judge: w_p, w_c, w_b, w_v = 2, 10, 3, 1
        elif "Value" in judge: w_p, w_c, w_b, w_v = 3, 3, 3, 10
        
        s1 = (r1['perf_score']*w_p) + (r1['cam_score']*w_c) + (r1['batt_score']*w_b) + (r1['value']*w_v)
        s2 = (r2['perf_score']*w_p) + (r2['cam_score']*w_c) + (r2['batt_score']*w_b) + (r2['value']*w_v)
        
        win1 = s1 >= s2
        c1_cls = "vs-winner-border" if win1 else ""
        c2_cls = "vs-winner-border" if not win1 else ""
        b1_html = "<div class='rec-badge'>👑 RECOMMENDED</div>" if win1 else "<div style='height:40px;'></div>"
        b2_html = "<div class='rec-badge'>👑 RECOMMENDED</div>" if not win1 else "<div style='height:40px;'></div>"
        
        def val_col(v1, v2): return "val-win" if v1 >= v2 else "val-lose"

        col_card1, col_card2 = st.columns(2)
        
        # 🔥 FIX: One-Liner HTML
        with col_card1:
            card1 = f"""<div class='vs-card {c1_cls}'>{b1_html}<div class='vs-title'>{r1['name']}</div><div class='vs-price'>${r1['price']:,}</div><div class='vs-row'><span>🚀 AnTuTu</span><span class='{val_col(r1['antutu'], r2['antutu'])}'>{int(r1['antutu']):,}</span></div><div class='vs-row'><span>⚡ Speed</span><span class='{val_col(r1['perf_score'], r2['perf_score'])}'>{r1['perf_score']:.1f}</span></div><div class='vs-row'><span>📸 Camera</span><span class='{val_col(r1['cam_score'], r2['cam_score'])}'>{r1['cam_score']}</span></div><div class='vs-row'><span>🔋 Battery</span><span class='{val_col(r1['batt_score'], r2['batt_score'])}'>{r1['batt_score']}</span></div><a href='{r1['link']}' target='_blank' class='amazon-btn'>VIEW DEAL</a></div>"""
            st.markdown(card1, unsafe_allow_html=True)

        with col_card2:
            card2 = f"""<div class='vs-card {c2_cls}'>{b2_html}<div class='vs-title'>{r2['name']}</div><div class='vs-price'>${r2['price']:,}</div><div class='vs-row'><span>🚀 AnTuTu</span><span class='{val_col(r2['antutu'], r1['antutu'])}'>{int(r2['antutu']):,}</span></div><div class='vs-row'><span>⚡ Speed</span><span class='{val_col(r2['perf_score'], r1['perf_score'])}'>{r2['perf_score']:.1f}</span></div><div class='vs-row'><span>📸 Camera</span><span class='{val_col(r2['cam_score'], r1['cam_score'])}'>{r2['cam_score']}</span></div><div class='vs-row'><span>🔋 Battery</span><span class='{val_col(r2['batt_score'], r1['batt_score'])}'>{r2['batt_score']}</span></div><a href='{r2['link']}' target='_blank' class='amazon-btn'>VIEW DEAL</a></div>"""
            st.markdown(card2, unsafe_allow_html=True)
            
        st.write("---")
        winner_name = r1['name'] if win1 else r2['name']
        st.success(f"**AI Verdict:** Based on **{judge}**, the **{winner_name}** wins.")