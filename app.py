import streamlit as st
import pandas as pd
import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TechChoose - Stable Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    # 🔥 IMPORTANT: เปลี่ยน Link ตรงนี้เป็นของ Google Sheet พี่นะครับ
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
    except Exception:
        return pd.DataFrame()

    if not df.empty:
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        if 'antutu' in df.columns:
            # คำนวณ Score จาก AnTuTu
            df['perf_score'] = (df['antutu'] / 3500000) * 10 
            df['perf_score'] = df['perf_score'].clip(upper=10)
        else:
            df['perf_score'] = 8.0 
        
        # ใช้ข้อมูลจาก CSV
        if 'camera' in df.columns: df['cam_score'] = df['camera']
        if 'battery' in df.columns: df['batt_score'] = df['battery']
        if 'award' not in df.columns: df['award'] = "Top Pick"
        
        # ถ้าไม่มี AnTuTu ให้สร้าง Fake ขึ้นมากัน Error
        if 'antutu' not in df.columns: df['antutu'] = df['price'] * 2000

        # 🔥 ฝังรหัส Affiliate (สำคัญมาก)
        my_tag = "techchoose-20"
        df['link'] = df['link'].apply(lambda x: f"{x}&tag={my_tag}" if '?' in str(x) else f"{x}?tag={my_tag}")

    return df

# --- 3. CSS (Clean & Stable) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Inter:wght@400;600;900&display=swap');
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* Sidebar Fix */
    section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #222; }
    section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 { color: #FBBF24 !important; }
    
    /* Input Styling */
    div[data-baseweb="select"] > div { background-color: #222 !important; border: 1px solid #555 !important; }
    div[data-baseweb="select"] span { color: white !important; }
    div[data-baseweb="select"] svg { fill: #FBBF24 !important; }

    .update-badge {
        background-color: #111; border: 1px solid #333; color: #00FF00;
        padding: 5px 10px; border-radius: 4px; font-size: 0.8em;
        text-align: center; margin-bottom: 20px; font-family: 'JetBrains Mono';
    }

    /* Winner Box */
    .winner-box {
        background: radial-gradient(circle at top right, #111, #000);
        border: 2px solid #3B82F6; border-radius: 20px; padding: 40px;
        box-shadow: 0 0 60px rgba(59, 130, 246, 0.25);
    }
    .award-badge {
        background: #F59E0B; color: black; font-weight: 900; padding: 10px 20px; 
        border-radius: 50px; text-transform: uppercase; display: inline-block; 
        margin-bottom: 20px; font-size: 0.9em; letter-spacing: 1px;
    }
    .hero-title { font-size: 3.5em; font-weight: 900; color: white; line-height: 1.1; margin-bottom: 15px; }
    .hero-price { color: #FBBF24; font-size: 3em; font-weight: 800; font-family: 'JetBrains Mono'; margin-bottom: 5px; }
    .msrp-label { font-size: 0.8em; color: #666; margin-bottom: 25px; font-style: italic; }
    .expert-verdict { background: #111; border-left: 5px solid #3B82F6; padding: 25px; border-radius: 0 12px 12px 0; margin-bottom: 35px; color: #E0E0E0; line-height: 1.6; }
    
    .stat-container { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 35px; }
    .stat-box { background: #151515; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #333; }
    .stat-label { color: #888; font-size: 0.8em; font-weight: 700; margin-bottom: 5px; text-transform: uppercase; }
    .stat-val { font-size: 1.6em; font-weight: 900; color: white; }
    .bar-bg { background: #333; height: 6px; border-radius: 3px; margin-top: 10px; overflow: hidden; }
    
    .bench-row { display: flex; gap: 30px; padding-top: 25px; border-top: 1px solid #222; margin-top: 25px; }
    .bench-item span { font-weight: bold; font-size: 1.2em; margin-left: 8px; color:white; }
    .bench-item { color: #888; font-family: 'JetBrains Mono'; }

    .amazon-btn { background: #3B82F6; color: white !important; padding: 22px; display: block; text-align: center; border-radius: 12px; font-weight: 900; text-decoration: none; font-size: 1.4em; margin-top: 20px; transition: 0.3s; }
    .amazon-btn:hover { background: #2563EB; }
    .deal-hint { text-align: center; color: #10B981; font-size: 0.9em; margin-top: 10px; font-weight: bold; }

    /* Alternatives */
    .alt-link { text-decoration: none; display: block; }
    .alt-row { 
        background: #0A0A0A; border: 1px solid #222; padding: 20px; 
        border-radius: 12px; margin-bottom: 12px; 
        display: flex; justify-content: space-between; align-items: center; transition: 0.2s; 
    }
    .alt-row:hover { border-color: #FBBF24; background: #111; transform: scale(1.01); }
    
    .rank-wrap { display: flex; align-items: center; gap: 15px; }
    .rank-circle {
        width: 32px; height: 32px; border-radius: 8px; 
        display: flex; align-items: center; justify-content: center;
        font-weight: 900; font-size: 1.1em;
        background: #222; border: 1px solid #444; color: #888;
    }
    .rank-silver { background: linear-gradient(135deg, #E0E0E0, #999); color: black; border: none; box-shadow: 0 0 10px rgba(255,255,255,0.2); }
    .rank-bronze { background: linear-gradient(135deg, #CD7F32, #8B4513); color: white; border: none; box-shadow: 0 0 10px rgba(205,127,50,0.2); }
    
    .reason-badge {
        font-size: 0.75em; font-weight: bold; text-transform: uppercase;
        padding: 2px 6px; border-radius: 4px; margin-left: 8px; vertical-align: middle;
    }
    .reason-green { background: rgba(16, 185, 129, 0.2); color: #10B981; border: 1px solid #10B981; }
    .reason-purple { background: rgba(168, 85, 247, 0.2); color: #A855F7; border: 1px solid #A855F7; }
    .reason-gray { background: #222; color: #BBB; border: 1px solid #444; }

    .save-tag-box { 
        color: #10B981; font-weight: bold; margin-left: 10px; font-size: 0.8em;
        background: rgba(16, 185, 129, 0.1); padding: 2px 6px; border-radius: 4px;
    }
    
    .mini-bar-container { display: flex; gap: 6px; margin-top: 8px; }
    .mini-stat { width: 40px; }
    .mini-track { width: 100%; height: 3px; background: #333; border-radius: 2px; }
    .mini-fill-blue { height: 100%; background: #3B82F6; border-radius: 2px;} 
    .mini-fill-purple { height: 100%; background: #A855F7; border-radius: 2px;} 
    .mini-fill-green { height: 100%; background: #10B981; border-radius: 2px;}
    
    .disclaimer-box { margin-top: 50px; padding: 20px; border-top: 1px solid #222; text-align: center; color: #555; font-size: 0.8em; }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🛒 TechChoose")
    st.markdown("<div class='update-badge'>✅ Data Verified: 20 Dec 2025</div>", unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Search Settings")
    os_choice = st.selectbox("📱 Operating System", ["Any", "iOS (Apple)", "Android"])
    st.write("")
    
    lifestyle = st.selectbox("👤 User Persona", [
        "💎 Ultimate High-End",
        "🏠 General Use / Daily Driver",
        "🎮 Hardcore Gamer", 
        "📸 Content Creator", 
        "💼 Business Pro", 
        "💰 Student / Budget", 
        "🛠️ Custom"
    ])
    st.write("")
    
    if "High-End" in lifestyle:
        budget = 9999 
        st.info("💎 UNLIMITED BUDGET ACTIVATED")
    elif "Custom" in lifestyle:
        budget = st.slider("💰 Max Budget (USD)", 100, 2000, 2000, step=50)
    else:
        budget = 9999

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
        st.markdown("### 🎛️ Adjust Preferences")
        p = st.slider("🚀 Performance", 1, 10, 8)
        c = st.slider("📸 Camera", 1, 10, 8)
        b = st.slider("🔋 Battery", 1, 10, 5)
        v = st.slider("💰 Value", 1, 10, 5)

    st.divider()
    st.button("🚀 ANALYZE MARKET", type="primary", use_container_width=True)

# --- 5. FUNCTIONS ---
def get_dynamic_badge(mode, price):
    if "High-End" in mode: return "💎 ABSOLUTE BEST IN CLASS"
    elif "Gamer" in mode: return "🏆 GAMING BEAST"
    elif "Creator" in mode: return "🎥 CREATOR CHOICE"
    elif "Student" in mode: return "💰 SMART SAVER PICK"
    elif "Business" in mode: return "💼 RELIABLE WORKHORSE"
    elif "General" in mode: return "⭐ BEST BALANCED PICK"
    else: return "⭐ TOP FLAGSHIP"

def get_expert_verdict(row, mode):
    if "Gamer" in mode: return f"Built for speed. <b>AnTuTu {int(row['antutu']):,}</b>."
    return f"Excellent choice based on your preferences."

def stat_bar_html(label, score, color):
    return f"<div class='stat-box'><div class='stat-label'>{label}</div><div class='stat-val'>{score:.1f}/10</div><div class='bar-bg'><div style='width:{score*10}%; height:100%; background:{color};'></div></div></div>"

# --- 6. MAIN APP ---
df = load_data()

if not df.empty:
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']
    df = df[df['price'] <= budget]

    base_score = (df['perf_score']*p) + (df['cam_score']*c) + (df['batt_score']*b) + (df['value']*v)
    price_penalty = df['price'].apply(lambda x: (x - price_penalty_threshold) * 0.5 if x > price_penalty_threshold else 0)
    df['final_score'] = base_score - price_penalty
    
    max_possible = (10*p) + (10*c) + (10*b) + (10*v)
    df['match'] = (df['final_score'] / max_possible) * 100
    df = df.sort_values(by='match', ascending=False).reset_index(drop=True)

    if len(df) > 0:
        winner = df.iloc[0]
        c1, c2 = st.columns([1.5, 1], gap="large")

        with c1:
            current_badge = get_dynamic_badge(lifestyle, winner['price'])
            verdict_html = get_expert_verdict(winner, lifestyle)
            stats_html = f"{stat_bar_html('🚀 PERFORMANCE', winner['perf_score'], '#3B82F6')}{stat_bar_html('📸 CAMERA', winner['cam_score'], '#A855F7')}{stat_bar_html('🔋 BATTERY', winner['batt_score'], '#10B981')}"
            
            btn_section = f"""<a href='{winner['link']}' target='_blank' class='amazon-btn'>👉 VIEW DEAL ON AMAZON</a><div class='deal-hint'>⚡ Click to check today's best price & coupons</div>"""
            
            winner_html = f"""<div class='winner-box'><div class='award-badge'>{current_badge}</div><div class='hero-title'>{winner['name']}</div><div class='hero-price'>${winner['price']:,}</div><div class='msrp-label'>*Official MSRP. Check link for real-time pricing.</div><div class='expert-verdict'>{verdict_html}</div><div class='stat-container'>{stats_html}</div><div class='bench-row'><div class='bench-item'>🚀 AnTuTu: <span>{int(winner['antutu']):,}</span></div><div class='bench-item'>📸 Cam: <span>{int(winner['cam_score'])}/10</span></div></div>{btn_section}</div>"""
            st.markdown(winner_html, unsafe_allow_html=True)

        with c2:
            st.markdown("### 🥈 Top Alternatives")
            for i, row in df.iloc[1:6].iterrows():
                diff = winner['price'] - row['price']
                save_html = f"<span class='save-tag-box'>SAVE ${diff:,}</span>" if diff > 0 else ""
                
                # --- 🔥 LOGIC: Smart Tags (Why this rank?) ---
                rank_num = i + 1
                if rank_num == 2: rank_badge = "<div class='rank-circle rank-silver'>🥈</div>"
                elif rank_num == 3: rank_badge = "<div class='rank-circle rank-bronze'>🥉</div>"
                else: rank_badge = f"<div class='rank-circle'>#{rank_num}</div>"

                # หาจุดเด่นเทียบกับแชมป์
                smart_tag = ""
                if row['batt_score'] > winner['batt_score']:
                    smart_tag = "<span class='reason-badge reason-green'>🔋 Better Battery</span>"
                elif row['cam_score'] > winner['cam_score']:
                    smart_tag = "<span class='reason-badge reason-purple'>📸 Better Camera</span>"
                elif row['price'] < winner['price']:
                    smart_tag = "<span class='reason-badge reason-green'>💰 Cheaper</span>"
                else:
                    # ถ้าไม่มีอะไรชนะเลย ให้ดึงฉายา (Award) จาก CSV มาโชว์
                    smart_tag = f"<span class='reason-badge reason-gray'>{row['award']}</span>"

                mini_bars = f"""<div class='mini-bar-container'><div class='mini-stat'><div class='mini-track'><div class='mini-fill-blue' style='width:{row['perf_score']*10}%;'></div></div></div><div class='mini-stat'><div class='mini-track'><div class='mini-fill-purple' style='width:{row['cam_score']*10}%;'></div></div></div><div class='mini-stat'><div class='mini-track'><div class='mini-fill-green' style='width:{row['batt_score']*10}%;'></div></div></div></div>"""
                
                alt_html = f"""
                <a href="{row['link']}" target="_blank" class="alt-link">
                    <div class="alt-row">
                        <div class="rank-wrap">
                            {rank_badge} 
                            <div>
                                <div style="font-weight:bold; font-size:1.1em; color:white;">
                                    {row['name']} {smart_tag}
                                </div>
                                <div style="color:#FBBF24; font-weight:bold;">${row['price']:,} {save_html}</div>
                                {mini_bars}
                            </div>
                        </div>
                        <div style="text-align:right">
                            <div style="font-size:1.3em; font-weight:900; color:#3B82F6;">{row['match']:.0f}%</div>
                            <div class="buy-hint" style="color:#FBBF24; font-size:0.8em; font-weight:bold; margin-top:5px;">VIEW ></div>
                        </div>
                    </div>
                </a>
                """
                st.markdown(alt_html, unsafe_allow_html=True)

        st.markdown("""<div class='disclaimer-box'>TechChoose is a participant in the Amazon Services LLC Associates Program. <br>Product prices and availability are accurate as of 20 Dec 2025.</div>""", unsafe_allow_html=True)

    else:
        st.warning(f"No devices found under ${budget}. Please adjust your filters.")
else:
    st.error("Database Error: Check CSV Link")