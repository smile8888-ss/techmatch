import streamlit as st
import pandas as pd
import random

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Logic Fixed",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS (Blackout + Neon Green Winner + AI Box) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;900&display=swap');
    
    /* 1. บังคับพื้นหลังดำสนิท */
    .stApp { background-color: #000000 !important; }

    /* 2. แก้ตัวหนังสือกลืน */
    .stSelectbox label, .stNumberInput label, .stTextInput label {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }
    p, span, div { color: #FFFFFF; }

    /* 3. แก้กล่องขาว Expander */
    div[data-testid="stExpander"] details summary {
        background-color: #111111 !important;
        color: #FFFFFF !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stExpander"] details {
        background-color: #111111 !important;
        border-color: #333 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stExpander"] div[data-testid="stVerticalBlock"] {
        background-color: #111111 !important;
    }
    div[data-testid="stExpander"] details summary svg { fill: #FFFFFF !important; }
    div[data-testid="stExpander"] details summary:hover {
        border-color: #FBBF24 !important; color: #FBBF24 !important;
    }

    /* 4. Dropdown */
    div[data-baseweb="select"] > div {
        background-color: #222222 !important; border: 1px solid #444 !important; color: white !important;
    }
    div[data-baseweb="select"] span { color: white !important; }
    li[role="option"] { background-color: #222222 !important; color: white !important; }

    /* 5. Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #000; padding-bottom: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #111; border-radius: 5px; border: 1px solid #333; color: #888; }
    .stTabs [aria-selected="true"] { background-color: #222 !important; border-color: #3B82F6 !important; color: white !important; }

    /* 6. Cards & Layout */
    div[data-testid="stForm"] { background-color: #0e0e0e !important; border: 1px solid #333; padding: 20px; border-radius: 12px; }
    .winner-box { background: radial-gradient(circle at top right, #111, #000); border: 2px solid #3B82F6; border-radius: 20px; padding: 30px; margin-bottom: 30px; box-shadow: 0 0 50px rgba(59, 130, 246, 0.2); }
    .hero-title { font-size: 2.5em !important; font-weight: 900; color: white !important; margin-bottom: 5px; }
    .hero-price { color: #FBBF24 !important; font-size: 2em !important; font-weight: 800; font-family: 'JetBrains Mono'; margin-bottom: 15px; }
    .amazon-btn { background: #3B82F6 !important; color: white !important; padding: 12px; display: block; text-align: center; border-radius: 8px; font-weight: 900; text-decoration: none; margin-top: 15px; transition: 0.3s; }
    .amazon-btn:hover { background: #2563EB !important; }

    /* Alt Cards */
    .alt-link { text-decoration: none !important; display: block; }
    .alt-card { background: #111 !important; border: 1px solid #333; border-radius: 12px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; transition: 0.2s; }
    .alt-card:hover { border-color: #555; background: #161616 !important; transform: translateX(5px); }

    /* VS Card */
    .vs-card { background: #111 !important; border: 1px solid #333; border-radius: 15px; padding: 20px; text-align: center; height: 100%; }
    .vs-winner-border { border: 2px solid #00FF99; box-shadow: 0 0 30px rgba(0, 255, 153, 0.15); } /* Neon Green Border */
    
    .vs-row { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #222; padding: 12px 0; }
    .vs-label { display: flex; align-items: center; gap: 8px; color: #CCC !important; font-weight: bold; font-size: 0.9em; }
    
    /* Values Coloring */
    .val-win { 
        color: #00FF99 !important; /* Neon Green */
        font-weight: 900; 
        font-family: 'JetBrains Mono'; 
        font-size: 1.1em;
        text-shadow: 0 0 10px rgba(0, 255, 153, 0.3);
    }
    .val-lose { 
        color: #FF4444 !important; /* Soft Red */
        font-weight: 900; 
        font-family: 'JetBrains Mono'; 
        font-size: 1.1em; 
        opacity: 0.8;
    }
    
    /* AI Analysis Box */
    .ai-box {
        background-color: #0f172a;
        border-left: 4px solid #3B82F6;
        padding: 20px;
        border-radius: 4px;
        margin-top: 25px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95em;
        line-height: 1.6;
        color: #e2e8f0 !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .ai-header {
        color: #3B82F6 !important;
        font-weight: 900;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA & LOGIC FIX ---
@st.cache_data(ttl=60)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
    except Exception:
        return pd.DataFrame()

    if not df.empty:
        df = df.dropna(subset=['name', 'price'])
        
        # 1. OS
        def get_os(name):
            name_str = str(name).lower()
            if 'iphone' in name_str or 'ipad' in name_str: return 'iOS'
            return 'Android'
        df['os_type'] = df['name'].apply(get_os)
        
        # 2. Brand
        def get_brand_score(name):
            n = str(name).lower()
            if 'iphone' in n or 'apple' in n: return 10.0
            if 'samsung' in n or 'galaxy' in n: return 10.0
            if 'google' in n: return 9.5
            return 9.0 
        df['brand_score'] = df['name'].apply(get_brand_score)
        
        # 3. Calculate Norm Scores
        max_antutu = df['antutu'].max() if 'antutu' in df.columns else 1
        max_cam = df['camera'].max() if 'camera' in df.columns else 10
        max_batt = df['battery'].max() if 'battery' in df.columns else 10
        max_price = df['price'].max() if 'price' in df.columns else 2000
        
        if 'antutu' in df.columns: df['perf_score'] = (df['antutu'] / max_antutu) * 10
        else: df['perf_score'] = 5.0 
        
        if 'camera' in df.columns: df['cam_score'] = (df['camera'] / max_cam) * 10
        else: df['cam_score'] = 5.0
        
        if 'battery' in df.columns: df['batt_score'] = (df['battery'] / max_batt) * 10
        else: df['batt_score'] = 5.0

        # 🔥 4. FIXED: DYNAMIC VALUE SCORE 🔥
        # สูตร: คะแนนเต็ม 10 - ((ราคา / ราคาแพงสุด) * 10) -> ยิ่งแพง คะแนนยิ่งน้อย
        if max_price > 0:
            df['value'] = 10 * (1 - (df['price'] / max_price)) + 1 # +1 กันได้ 0
            df['value'] = df['value'].clip(0, 10)
        else:
            df['value'] = 5.0
            
        # Optional Fill
        if 'antutu' not in df.columns: df['antutu'] = df['price'] * 2000

        my_tag = "techchoose-20"
        df['link'] = df['link'].apply(lambda x: f"{x}&tag={my_tag}" if '?' in str(x) else f"{x}?tag={my_tag}")
    return df

df = load_data()

# --- 4. HELPERS & AI ---
def get_dynamic_badge(mode, price):
    if "High-End" in mode: return "💎 MARKET LEADER"
    elif "Gamer" in mode: return "🏆 GAMING BEAST"
    elif "Creator" in mode: return "🎥 CREATOR CHOICE"
    elif "Student" in mode: return "💰 BEST VALUE"
    else: return "⭐ TOP PICK"

def stat_bar_html(label, score, color):
    width = min(score * 10, 100)
    return f"<div style='background:#151515;padding:8px;border-radius:8px;text-align:center;border:1px solid #333;margin-bottom:5px;'><div style='color:#888 !important;font-size:0.65em;font-weight:700;margin-bottom:4px;'>{label}</div><div style='font-size:1.1em;font-weight:900;color:white !important;'>{score:.1f}</div><div style='background:#333;height:4px;border-radius:2px;margin-top:4px;overflow:hidden;'><div style='width:{width}%;height:100%;background:{color};'></div></div></div>"

def get_reason_badge_html(winner_row, current_row):
    badges = ""
    diff = winner_row['price'] - current_row['price']
    if diff >= 50:
        badges += f"<span style='background:rgba(16,185,129,0.2);color:#10B981 !important;border:1px solid #10B981;padding:2px 6px;border-radius:4px;font-size:0.7em;font-weight:bold;margin-left:8px;'>SAVE ${int(diff):,}</span>"
    if current_row['perf_score'] > (winner_row['perf_score'] + 0.3):
        badges += "<span style='background:rgba(59,130,246,0.2);color:#3B82F6 !important;border:1px solid #3B82F6;padding:2px 6px;border-radius:4px;font-size:0.7em;font-weight:bold;margin-left:8px;'>🚀 FASTER</span>"
    return badges

def get_score_badge_html(icon, label, score):
    if score >= 9.5: c, b = "#10B981", "rgba(16,185,129,0.4)"
    elif score >= 8.5: c, b = "#3B82F6", "rgba(59,130,246,0.4)"
    else: c, b = "#F59E0B", "rgba(245,158,11,0.4)"
    return f"<div style='display:inline-flex;align-items:center;background:rgba(0,0,0,0.5);border:1px solid {b};border-radius:6px;padding:3px 8px;margin-right:6px;'><span style='font-size:1em;margin-right:4px;'>{icon}</span><span style='color:#888 !important;font-size:0.6em;font-weight:700;margin-right:4px;text-transform:uppercase;'>{label}</span><span style='color:{c} !important;font-weight:900;font-family:monospace;font-size:0.9em;'>{score:.1f}</span></div>"

def generate_ai_analysis(winner, loser, reason_mode):
    w_name = winner['name']
    l_name = loser['name']
    
    perf_diff = ((winner['perf_score'] - loser['perf_score']) / loser['perf_score']) * 100
    price_diff = winner['price'] - loser['price']
    
    analysis = []
    
    openers = [
        f"Based on the data, **{w_name}** emerges as the superior choice for {reason_mode.lower()}.",
        f"After analyzing the specs, **{w_name}** takes the crown here.",
        f"For users prioritizing {reason_mode}, **{w_name}** wins this battle."
    ]
    analysis.append(random.choice(openers))
    
    if perf_diff > 15:
        analysis.append(f"It completely dominates with a **{perf_diff:.1f}% performance advantage**, making it a beast for heavy tasks.")
    elif perf_diff > 5:
        analysis.append(f"It offers a noticeable **{perf_diff:.1f}% speed boost**.")
    
    if winner['cam_score'] > loser['cam_score'] + 1:
        analysis.append(f"Photography enthusiasts will prefer its superior camera system (Score: {winner['cam_score']:.1f}).")
        
    if price_diff < 0:
        analysis.append(f"Best of all, it costs **${abs(price_diff):,} less** than the {l_name}, offering incredible value.")
    elif price_diff > 0:
        analysis.append(f"Although it costs **${price_diff:,} more**, the performance justifies the premium.")
        
    return " ".join(analysis)

# --- 5. MAIN APP ---
st.title("🛒 TechChoose AI")
st.markdown("<div style='margin-bottom:20px; color:#888 !important;'>✅ Data Verified: 20 Dec 2025 | 🤖 AI Engine: Active</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 FIND BEST MATCH", "⚔️ COMPARE MODELS"])

# ==========================================
# TAB 1: FIND BEST MATCH (LOGIC TUNED)
# ==========================================
with tab1:
    with st.expander("🔍 **TAP TO CUSTOMIZE**", expanded=True):
        c1, c2 = st.columns(2)
        with c1: os_choice = st.selectbox("Operating System", ["Any", "iOS", "Android"], key="t1_os")
        with c2: lifestyle = st.selectbox("User Persona", ["💎 Ultimate High-End", "🏠 General Use", "🎮 Gamer", "📸 Creator", "💰 Student"], key="t1_life")
        
        if st.button("🚀 UPDATE RESULTS", type="primary", use_container_width=True): st.rerun()

    st.divider()

    if not df.empty:
        df_f = df.copy()
        if "iOS" in os_choice: df_f = df_f[df_f['os_type']=='iOS']
        elif "Android" in os_choice: df_f = df_f[df_f['os_type']=='Android']
        
        # 🔥 WEIGHTING LOGIC FIX 🔥
        p, c, b, v, br = 5, 5, 5, 5, 2 
        
        if "High-End" in lifestyle: 
            p,c,b,v,br = 10, 10, 8, 1, 4  # ไม่สนความคุ้มค่า (v น้อย)
            budget = 9999
        elif "Gamer" in lifestyle: 
            p,c,b,v,br = 20, 5, 10, 5, 1
            budget = 2000
        elif "Creator" in lifestyle:
            p,c,b,v,br = 6, 20, 8, 5, 2
            budget = 2000
        elif "Student" in lifestyle:
            budget = 900 # จำกัดงบ
            p,c,b,v,br = 3, 5, 8, 40, 1 # 🔥 เน้นความคุ้มค่า (v=40)
        else: # General Use
            budget = 1500
            p,c,b,v,br = 5, 5, 5, 25, 2 # 🔥 เน้นความคุ้มค่า (v=25)
            
        df_f = df_f[df_f['price'] <= budget]
        df_f['final_score'] = (df_f['perf_score']*p) + (df_f['cam_score']*c) + (df_f['batt_score']*b) + (df_f['value']*v) + (df_f['brand_score']*br)
        df_f = df_f.sort_values('final_score', ascending=False).reset_index(drop=True)

        if len(df_f) > 0:
            winner = df_f.iloc[0]
            s1 = stat_bar_html('🚀 SPEED', winner['perf_score'], '#3B82F6')
            s2 = stat_bar_html('📸 CAM', winner['cam_score'], '#A855F7')
            s3 = stat_bar_html('🔋 BATT', winner['batt_score'], '#10B981')
            stats = f"<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:20px 0;'>{s1}{s2}{s3}</div>"
            
            st.markdown(f"""
            <div class='winner-box'>
                <div style='background:#F59E0B;color:black !important;padding:5px 15px;border-radius:20px;display:inline-block;font-weight:900;font-size:0.8em;margin-bottom:10px;'>{get_dynamic_badge(lifestyle, winner['price'])}</div>
                <div class='hero-title'>{winner['name']}</div>
                <div class='hero-price'>${winner['price']:,}</div>
                {stats}
                <a href='{winner['link']}' target='_blank' class='amazon-btn'>👉 VIEW DEAL</a>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("🥈 Top Alternatives")
            
            for i, row in df_f.iloc[1:6].iterrows():
                rank_num = i + 1
                rank_col = "#E0E0E0" if rank_num == 2 else "#E6AC75" if rank_num == 3 else "#333"
                badges = get_reason_badge_html(winner, row)
                scores = f"{get_score_badge_html('🚀','Speed',row['perf_score'])}{get_score_badge_html('📸','Cam',row['cam_score'])}{get_score_badge_html('🔋','Batt',row['batt_score'])}"
                
                st.markdown(f"""
                <a href='{row['link']}' target='_blank' class='alt-link'>
                    <div class='alt-card'>
                        <div style='display:flex;align-items:center;'>
                            <div style='width:35px;height:35px;background:{rank_col};color:{'black' if rank_num<4 else '#888'} !important;display:flex;align-items:center;justify-content:center;font-weight:900;border-radius:8px;margin-right:15px;font-size:1.2em;'>{rank_num}</div>
                            <div style='flex-grow:1;'>
                                <div style='color:white !important;font-weight:bold;font-size:1.1em;margin-bottom:5px;'>{row['name']} {badges}</div>
                                <div style='color:#FBBF24 !important;font-weight:bold;'>${row['price']:,}</div>
                                <div style='margin-top:8px;'>{scores}</div>
                            </div>
                            <div style='color:#F59E0B !important;font-weight:bold;font-size:0.8em;'>VIEW ></div>
                        </div>
                    </div>
                </a>
                """, unsafe_allow_html=True)

# ==========================================
# TAB 2: VS MODE
# ==========================================
with tab2:
    st.subheader("🥊 Head-to-Head Comparison")
    
    all_models = sorted(df['name'].unique())
    
    with st.form("compare_form"):
        c1, c2 = st.columns(2)
        with c1: p1_name = st.selectbox("Select Phone A", all_models, index=0)
        with c2: p2_name = st.selectbox("Select Phone B", all_models, index=1 if len(all_models)>1 else 0)
        
        judge = st.selectbox("Decide Winner By:", ["💎 Overall Specs", "🎮 Gaming Performance", "📸 Camera Quality"])
        
        submitted = st.form_submit_button("⚔️ ANALYZE & COMPARE", type="primary", use_container_width=True)
    
    if submitted:
        r1 = df[df['name'] == p1_name].iloc[0]
        r2 = df[df['name'] == p2_name].iloc[0]
        
        w_p, w_c, w_b, w_v, w_br = 1, 1, 1, 1, 1
        if "Gaming" in judge: w_p, w_c, w_b, w_v, w_br = 10, 0, 3, 1, 1
        elif "Camera" in judge: w_p, w_c, w_b, w_v, w_br = 2, 10, 3, 1, 1
        
        s1 = (r1['perf_score']*w_p) + (r1['cam_score']*w_c) + (r1['batt_score']*w_b) + (r1['value']*w_v) + (r1['brand_score']*w_br)
        s2 = (r2['perf_score']*w_p) + (r2['cam_score']*w_c) + (r2['batt_score']*w_b) + (r2['value']*w_v) + (r2['brand_score']*w_br)
        
        if s1 >= s2:
            win_row, lose_row = r1, r2
            win_idx = 1
        else:
            win_row, lose_row = r2, r1
            win_idx = 2

        # --- Visual Comparison Block ---
        c1_cls = "vs-winner-border" if win_idx == 1 else ""
        c2_cls = "vs-winner-border" if win_idx == 2 else ""
        rec1 = "<div style='color:#00FF99 !important;font-weight:900;margin-bottom:10px;'>👑 WINNER</div>" if win_idx == 1 else "<div style='height:29px'></div>"
        rec2 = "<div style='color:#00FF99 !important;font-weight:900;margin-bottom:10px;'>👑 WINNER</div>" if win_idx == 2 else "<div style='height:29px'></div>"

        def create_vs_row(icon, label, v1, v2, is_fmt=False):
            val1 = f"{int(v1):,}" if is_fmt else f"{v1:.1f}"
            val2 = f"{int(v2):,}" if is_fmt else f"{v2:.1f}"
            
            c1 = "val-win" if v1 >= v2 else "val-lose"
            c2 = "val-win" if v2 >= v1 else "val-lose"
            
            return f"<div class='vs-row'><div class='vs-label'><span>{icon}</span> {label}</div><div class='{c1}'>{val1}</div></div>", \
                   f"<div class='vs-row'><div class='vs-label'><span>{icon}</span> {label}</div><div class='{c2}'>{val2}</div></div>"

        r_chip = ("", "")
        if 'chipset' in df.columns:
             t1 = r1['chipset'] if pd.notna(r1['chipset']) else "-"
             t2 = r2['chipset'] if pd.notna(r2['chipset']) else "-"
             r_chip = (f"<div class='vs-row'><div class='vs-label'><span>🧠</span> Chipset</div><div style='color:white !important;font-weight:bold;'>{t1}</div></div>",
                       f"<div class='vs-row'><div class='vs-label'><span>🧠</span> Chipset</div><div style='color:white !important;font-weight:bold;'>{t2}</div></div>")

        r_antutu = create_vs_row("🚀", "AnTuTu", r1['antutu'], r2['antutu'], True)
        r_speed = create_vs_row("⚡", "Speed", r1['perf_score'], r2['perf_score'])
        r_cam = create_vs_row("📸", "Cam", r1['cam_score'], r2['cam_score'])
        r_batt = create_vs_row("🔋", "Batt", r1['batt_score'], r2['batt_score'])

        st.divider()
        
        # 🔥 AI Verdict
        ai_text = generate_ai_analysis(win_row, lose_row, judge)
        st.markdown(f"""
        <div class='ai-box'>
            <div class='ai-header'>
                <span>🤖</span> AI ANALYST VERDICT
            </div>
            {ai_text}
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") 

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            <div class='vs-card {c1_cls}'>
                {rec1}
                <div class='hero-title' style='font-size:1.5em !important;'>{r1['name']}</div>
                <div class='hero-price' style='font-size:1.5em !important;'>${r1['price']:,}</div>
                {r_chip[0]}{r_antutu[0]}{r_speed[0]}{r_cam[0]}{r_batt[0]}
                <a href='{r1['link']}' target='_blank' class='amazon-btn'>VIEW DEAL</a>
            </div>
            """, unsafe_allow_html=True)
            
        with col_b:
            st.markdown(f"""
            <div class='vs-card {c2_cls}'>
                {rec2}
                <div class='hero-title' style='font-size:1.5em !important;'>{r2['name']}</div>
                <div class='hero-price' style='font-size:1.5em !important;'>${r2['price']:,}</div>
                {r_chip[1]}{r_antutu[1]}{r_speed[1]}{r_cam[1]}{r_batt[1]}
                <a href='{r2['link']}' target='_blank' class='amazon-btn'>VIEW DEAL</a>
            </div>
            """, unsafe_allow_html=True)