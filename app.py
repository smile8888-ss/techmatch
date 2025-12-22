import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Final Compare Fix",
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
        
        # --- Brand Score ---
        def get_brand_score(name):
            n = str(name).lower()
            if 'iphone' in n or 'apple' in n: return 10.0
            if 'samsung' in n or 'galaxy' in n: return 10.0
            if 'google' in n or 'pixel' in n: return 9.5
            return 9.0 
        df['brand_score'] = df['name'].apply(get_brand_score)
        
        # --- Relative Scoring (เทียบกับตัวท็อป) ---
        max_antutu = df['antutu'].max() if 'antutu' in df.columns else 1
        max_cam = df['camera'].max() if 'camera' in df.columns else 10
        max_batt = df['battery'].max() if 'battery' in df.columns else 10
        
        if 'antutu' in df.columns:
            df['perf_score'] = (df['antutu'] / max_antutu) * 10
        else: df['perf_score'] = 8.0 
        
        if 'camera' in df.columns: df['cam_score'] = (df['camera'] / max_cam) * 10
        if 'battery' in df.columns: df['batt_score'] = (df['battery'] / max_batt) * 10
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
    return f"Excellent choice based on your preferences. Score: {row['final_score']:.1f}/100"

def stat_bar_html(label, score, color):
    width = min(score * 10, 100)
    return f"""<div class="stat-box"><div class="stat-label">{label}</div><div class="stat-val">{score:.1f}/10</div><div class="bar-bg"><div style="width:{width}%;height:100%;background:{color};"></div></div></div>"""

def get_reason_badge(winner_row, current_row):
    badges = ""
    price_diff = winner_row['price'] - current_row['price']
    if price_diff >= 50:
        badges += f"""<span style="background:rgba(16,185,129,0.2);color:#10B981;border:1px solid #10B981;padding:2px 6px;border-radius:4px;font-size:0.7em;font-weight:bold;margin-left:8px;">SAVE ${int(price_diff):,}</span>"""
    if current_row['perf_score'] > (winner_row['perf_score'] + 0.3):
        badges += """<span style="background:rgba(59,130,246,0.2);color:#3B82F6;border:1px solid #3B82F6;padding:2px 6px;border-radius:4px;font-size:0.7em;font-weight:bold;margin-left:8px;">🚀 FASTER</span>"""
    return badges

def get_score_badge(icon, label, score):
    if score >= 9.5: color = "#10B981"; border = "rgba(16,185,129,0.4)" 
    elif score >= 8.5: color = "#3B82F6"; border = "rgba(59,130,246,0.4)" 
    else: color = "#F59E0B"; border = "rgba(245,158,11,0.4)" 
    return f"""<div style="display:inline-flex;align-items:center;background:rgba(0,0,0,0.5);border:1px solid {border};border-radius:6px;padding:3px 8px;margin-right:6px;"><span style="font-size:1em;margin-right:4px;">{icon}</span><span style="color:#888;font-size:0.6em;font-weight:700;margin-right:4px;text-transform:uppercase;">{label}</span><span style="color:{color};font-weight:900;font-family:'JetBrains Mono',monospace;font-size:0.9em;">{score:.1f}</span></div>"""

# --- 4. CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Inter:wght@400;600;900&display=swap');
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; font-family: 'Inter', sans-serif; }

    /* UI Fixes */
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
    .winner-box { background: radial-gradient(circle at top right, #111, #000); border: 2px solid #3B82F6; border-radius: 20px; padding: 30px; box-shadow: 0 0 60px rgba(59, 130, 246, 0.25); margin-bottom: 30px; }
    .hero-title { font-size: 2.8em; font-weight: 900; color: white; line-height: 1.1; margin-bottom: 10px; }
    .hero-price { color: #FBBF24; font-size: 2.2em; font-weight: 800; font-family: 'JetBrains Mono'; margin-bottom: 15px; }
    .stat-box { background: #151515; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #333; }
    .stat-label { color: #888; font-size: 0.7em; font-weight: 700; margin-bottom: 5px; text-transform: uppercase; }
    .stat-val { font-size: 1.2em; font-weight: 900; color: white; }
    .bar-bg { background: #333; height: 4px; border-radius: 2px; margin-top: 5px; overflow: hidden; }
    .amazon-btn { background: #3B82F6; color: white !important; padding: 15px; display: block; text-align: center; border-radius: 12px; font-weight: 900; text-decoration: none; font-size: 1.1em; margin-top: 20px; transition: 0.3s; }
    .amazon-btn:hover { background: #2563EB; }

    /* ALT CARDS */
    .alt-link { text-decoration: none !important; display: block; }
    .alt-card { background: #111; border: 1px solid #333; border-radius: 12px; padding: 18px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; transition: all 0.2s ease; }
    .alt-card:hover { border-color: #555; background: #161616; transform: translateX(5px); }
    
    .rank-box { width: 35px; height: 35px; display: flex; align-items: center; justify-content: center; font-weight: 900; border-radius: 8px; font-size: 1.2em; margin-right: 20px; }
    .rank-2 { background: linear-gradient(135deg, #E0E0E0, #999); color: black; border: 1px solid #FFF; }
    .rank-3 { background: linear-gradient(135deg, #E6AC75, #A0522D); color: black; border: 1px solid #FFD700; }
    .rank-norm { background: #222; color: #888; border: 1px solid #444; }

    .alt-info { flex-grow: 1; }
    .alt-name { color: white; font-weight: 700; font-size: 1.2em; margin-bottom: 8px; display: flex; align-items: center; }
    .alt-price { color: #FBBF24; font-family: 'JetBrains Mono'; font-weight: bold; font-size: 1.1em; }
    
    .view-btn { color: #FF9900; font-weight: 900; font-size: 0.8em; text-transform: uppercase; letter-spacing: 1px; }

    /* VS CARD STYLES (FIXED SPACING) */
    .vs-card { background: #111; border: 1px solid #333; border-radius: 15px; padding: 25px; text-align: center; height: 100%; }
    .vs-winner-border { border: 2px solid #10B981; box-shadow: 0 0 30px rgba(16, 185, 129, 0.15); }
    .vs-title { font-size: 1.4em; font-weight: 900; margin-bottom: 5px; min-height: 50px; display:flex; align-items:center; justify-content:center; color: white !important;}
    .vs-price { font-family: 'JetBrains Mono'; color: #FBBF24; font-size: 1.5em; margin-bottom: 20px; font-weight: bold; }
    
    /* 🔥 FIX: Spaced Out Rows using Flexbox */
    .vs-row { 
        display: flex; 
        justify-content: space-between; /* ดันซ้าย-ขวาแยกกัน */
        align-items: center;
        border-bottom: 1px solid #222; 
        padding: 12px 0; 
        font-size: 0.95em; 
        color: #BBB; 
    }
    .vs-label { display: flex; align-items: center; gap: 8px; font-weight: bold; }
    .val-win { color: #10B981; font-weight: 900; font-family: 'JetBrains Mono'; } 
    .val-lose { color: #555; font-family: 'JetBrains Mono'; font-weight: bold;}

    @media only screen and (max-width: 600px) {
        .hero-title { font-size: 2.0em !important; }
        .alt-card { flex-direction: column; align-items: flex-start; }
    }
</style>
""", unsafe_allow_html=True)

# --- 5. HEADER ---
st.title("🛒 TechChoose")
st.markdown("<div style='background:#111; color:#00FF00; padding:5px 10px; border-radius:4px; display:inline-block; border:1px solid #333; margin-bottom:15px; font-size:0.8em;'>✅ Data Verified: 20 Dec 2025</div>", unsafe_allow_html=True)

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

        # Balanced Weights
        p, c, b, v, br = 5, 5, 5, 5, 2 
        price_penalty_threshold = 9999
        
        if "High-End" in lifestyle: p,c,b,v,br = 10, 10, 8, 0, 4
        elif "Gamer" in lifestyle: p,c,b,v,br = 20, 5, 10, 5, 1
        elif "Business" in lifestyle: p,c,b,v,br = 8, 8, 10, 5, 5
        elif "Student" in lifestyle: p,c,b,v,br = 6, 6, 8, 20, 1; price_penalty_threshold = 800

        if "Custom" in lifestyle:
            st.divider()
            cc1, cc2, cc3, cc4 = st.columns(4)
            with cc1: p = st.number_input("Speed", 1, 10, 8, key="t1_p")
            with cc2: c = st.number_input("Cam", 1, 10, 8, key="t1_c")
            with cc3: b = st.number_input("Batt", 1, 10, 5, key="t1_b")
            with cc4: br = st.number_input("Brand", 1, 10, 2, key="t1_br")

        if st.button("🚀 UPDATE RESULTS", type="primary", use_container_width=True, key="t1_btn"): st.rerun()

    st.divider()

    if not df.empty:
        df_f = df.copy()
        if "iOS" in os_choice: df_f = df_f[df_f['os_type']=='iOS']
        elif "Android" in os_choice: df_f = df_f[df_f['os_type']=='Android']
        df_f = df_f[df_f['price'] <= budget]
        
        score = (df_f['perf_score']*p) + (df_f['cam_score']*c) + (df_f['batt_score']*b) + (df_f['value']*v) + (df_f['brand_score']*br)
        price_pen = df_f['price'].apply(lambda x: (x - price_penalty_threshold) * 0.5 if x > price_penalty_threshold else 0)
        df_f['final_score'] = score - price_pen
        
        max_s = (10*p) + (10*c) + (10*b) + (10*v) + (10*br)
        df_f['match'] = (df_f['final_score'] / max_s) * 100
        df_f = df_f.sort_values('match', ascending=False).reset_index(drop=True)

        if len(df_f) > 0:
            winner = df_f.iloc[0]
            current_badge = get_dynamic_badge(lifestyle, winner['price'])
            
            stats_html = f"""<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:20px;'>{stat_bar_html('🚀 SPEED', winner['perf_score'], '#3B82F6')}{stat_bar_html('📸 CAM', winner['cam_score'], '#A855F7')}{stat_bar_html('🔋 BATT', winner['batt_score'], '#10B981')}</div>"""
            winner_card = f"""<div class='winner-box'><div style='background:#F59E0B; color:black; padding:6px 14px; border-radius:50px; display:inline-block; font-weight:900; font-size:0.75em; margin-bottom:15px; letter-spacing:1px;'>{current_badge}</div><div class='hero-title'>{winner['name']}</div><div class='hero-price'>${winner['price']:,}</div><div style='background:#111; border-left:4px solid #3B82F6; padding:12px; margin-bottom:20px; font-size:0.9em; color:#CCC;'>{get_expert_verdict(winner, lifestyle)}</div>{stats_html}<a href='{winner['link']}' target='_blank' class='amazon-btn'>👉 VIEW DEAL ON AMAZON</a><div style='text-align:center; color:#10B981; font-size:0.85em; margin-top:10px; font-weight:bold;'>⚡ Check today's price</div></div>"""
            st.markdown(winner_card, unsafe_allow_html=True)

            st.write("")
            st.markdown("### 🥈 Top Alternatives")
            
            for i, row in df_f.iloc[1:6].iterrows():
                rank_num = i + 1
                if rank_num == 2: rank_style = "background:linear-gradient(135deg,#E0E0E0,#999);color:black;border:1px solid white;"
                elif rank_num == 3: rank_style = "background:linear-gradient(135deg,#E6AC75,#A0522D);color:black;border:1px solid #FFD700;"
                else: rank_style = "background:#222;color:#888;border:1px solid #444;"
                
                reason_badge = get_reason_badge(winner, row)
                b_speed = get_score_badge("🚀", "Speed", row['perf_score'])
                b_cam = get_score_badge("📸", "Cam", row['cam_score'])
                b_batt = get_score_badge("🔋", "Batt", row['batt_score'])
                
                alt_card = f"""<a href="{row['link']}" target="_blank" class="alt-link"><div class="alt-card"><div style="display:flex;align-items:center;width:100%;"><div style="width:35px;height:35px;display:flex;align-items:center;justify-content:center;font-weight:900;border-radius:8px;font-size:1.2em;margin-right:20px;{rank_style}">{rank_num}</div><div style="flex-grow:1;"><div style="color:white;font-weight:700;font-size:1.1em;margin-bottom:6px;">{row['name']} {reason_badge}</div><div style="color:#FBBF24;font-family:'JetBrains Mono';font-weight:bold;font-size:1em;">${row['price']:,}</div><div style="margin-top:10px;display:flex;gap:5px;">{b_speed}{b_cam}{b_batt}</div></div><div class="view-btn">VIEW &gt;</div></div></div></a>"""
                st.markdown(alt_card, unsafe_allow_html=True)
        else:
            st.warning("No phones found under this budget.")

# ==========================================
# TAB 2: VS MODE (STABLE & SPACED UI)
# ==========================================
with tab2:
    st.markdown("### 🥊 Head-to-Head Comparison")
    
    judge = st.selectbox("⚖️ Decide Winner By:", ["💎 Overall Specs", "🎮 Gaming Performance", "📸 Camera Quality", "💰 Value for Money"], key="vs_judge")
    all_models = sorted(df['name'].unique())
    
    # 🔥 ANTI-JUMP: ใช้ Session State เก็บค่า
    if 'p1_idx' not in st.session_state: st.session_state.p1_idx = 0
    if 'p2_idx' not in st.session_state: st.session_state.p2_idx = 1 if len(all_models) > 1 else 0

    c1, c2 = st.columns(2)
    with c1: 
        p1_name = st.selectbox("Select Phone A", all_models, index=st.session_state.p1_idx, key="p1_select")
        st.session_state.p1_idx = all_models.index(p1_name) # Update State
    with c2: 
        p2_name = st.selectbox("Select Phone B", all_models, index=st.session_state.p2_idx, key="p2_select")
        st.session_state.p2_idx = all_models.index(p2_name) # Update State
    
    if p1_name and p2_name: 
        r1 = df[df['name'] == p1_name].iloc[0]
        r2 = df[df['name'] == p2_name].iloc[0]
        
        w_p, w_c, w_b, w_v, w_br = 1, 1, 1, 1, 1
        if "Gaming" in judge: w_p, w_c, w_b, w_v, w_br = 10, 0, 3, 1, 1
        elif "Camera" in judge: w_p, w_c, w_b, w_v, w_br = 2, 10, 3, 1, 1
        elif "Value" in judge: w_p, w_c, w_b, w_v, w_br = 3, 3, 3, 10, 1
        
        s1 = (r1['perf_score']*w_p) + (r1['cam_score']*w_c) + (r1['batt_score']*w_b) + (r1['value']*w_v) + (r1['brand_score']*w_br)
        s2 = (r2['perf_score']*w_p) + (r2['cam_score']*w_c) + (r2['batt_score']*w_b) + (r2['value']*w_v) + (r2['brand_score']*w_br)
        
        win1 = s1 >= s2
        c1_cls = "vs-winner-border" if win1 else ""
        c2_cls = "vs-winner-border" if not win1 else ""
        b1_html = "<div style='background:linear-gradient(135deg,#FFD700,#F59E0B);color:black;font-weight:900;padding:6px 15px;border-radius:50px;display:inline-block;margin-bottom:20px;font-size:0.8em;letter-spacing:1px;'>👑 RECOMMENDED</div>" if win1 else "<div style='height:40px;'></div>"
        b2_html = "<div style='background:linear-gradient(135deg,#FFD700,#F59E0B);color:black;font-weight:900;padding:6px 15px;border-radius:50px;display:inline-block;margin-bottom:20px;font-size:0.8em;letter-spacing:1px;'>👑 RECOMMENDED</div>" if not win1 else "<div style='height:40px;'></div>"
        
        def val_col(v1, v2): return "val-win" if v1 >= v2 else "val-lose"

        col_card1, col_card2 = st.columns(2)
        
        # 🔥 UI FIX: Spacing & Alignment
        def get_row_html(label, icon, val1, val2):
            cls1 = val_col(val1, val2)
            cls2 = val_col(val2, val1)
            # เราใช้ฟังก์ชันนี้สร้าง row สำหรับแต่ละการ์ด (แยกกัน)
            return "" 

        # สร้างการ์ดซ้าย
        with col_card1:
            rows_html = ""
            for lbl, ico, k in [("AnTuTu","🚀","antutu"), ("Speed","⚡","perf_score"), ("Camera","📸","cam_score"), ("Battery","🔋","batt_score")]:
                v1 = r1[k]; v2 = r2[k]
                val_str = f"{int(v1):,}" if k == "antutu" else f"{v1:.1f}"
                cls = "val-win" if v1 >= v2 else "val-lose"
                rows_html += f"""<div class='vs-row'><div class='vs-label'><span>{ico}</span> {lbl}</div><div class='{cls}'>{val_str}</div></div>"""
            
            st.markdown(f"""<div class='vs-card {c1_cls}'>{b1_html}<div class='vs-title'>{r1['name']}</div><div class='vs-price'>${r1['price']:,}</div>{rows_html}<a href='{r1['link']}' target='_blank' class='amazon-btn'>VIEW DEAL</a></div>""", unsafe_allow_html=True)

        # สร้างการ์ดขวา
        with col_card2:
            rows_html = ""
            for lbl, ico, k in [("AnTuTu","🚀","antutu"), ("Speed","⚡","perf_score"), ("Camera","📸","cam_score"), ("Battery","🔋","batt_score")]:
                v1 = r1[k]; v2 = r2[k]
                val_str = f"{int(v2):,}" if k == "antutu" else f"{v2:.1f}"
                cls = "val-win" if v2 >= v1 else "val-lose"
                rows_html += f"""<div class='vs-row'><div class='vs-label'><span>{ico}</span> {lbl}</div><div class='{cls}'>{val_str}</div></div>"""
            
            st.markdown(f"""<div class='vs-card {c2_cls}'>{b2_html}<div class='vs-title'>{r2['name']}</div><div class='vs-price'>${r2['price']:,}</div>{rows_html}<a href='{r2['link']}' target='_blank' class='amazon-btn'>VIEW DEAL</a></div>""", unsafe_allow_html=True)
            
        st.write("---")
        winner_name = r1['name'] if win1 else r2['name']
        st.success(f"**AI Verdict:** Based on **{judge}**, the **{winner_name}** wins.")