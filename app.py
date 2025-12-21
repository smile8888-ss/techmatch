import streamlit as st
import pandas as pd

# --- 1. CONFIG ---
st.set_page_config(
    page_title="TechChoose - Ultimate AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    # 👇 ลิงก์ CSV ของพี่ (อันเดิมที่ใช้ได้เลย)
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        
        # ป้องกัน Error กรณีลืมใส่รูป
        if 'image' not in df.columns:
            df['image'] = None
            
        return df
    except Exception:
        return pd.DataFrame()

# --- 3. ULTIMATE CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* Main Theme */
    .stApp { background-color: #0F172A; color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #020617; border-right: 1px solid #1E293B; }
    section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }

    /* Winner Card */
    .winner-card {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border: 2px solid #F59E0B; border-radius: 24px; padding: 30px;
        text-align: center; box-shadow: 0 0 40px rgba(245, 158, 11, 0.15);
        position: relative; overflow: hidden;
    }
    .winner-img {
        width: 220px; height: 220px; object-fit: contain;
        margin: 20px auto; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.5));
        transition: transform 0.3s;
    }
    .winner-img:hover { transform: scale(1.05); }

    /* Alternatives */
    .alt-card {
        background: #1E293B; border: 1px solid #334155;
        padding: 15px; border-radius: 16px; margin-bottom: 15px;
        display: flex; align-items: center; gap: 20px;
        transition: all 0.2s;
    }
    .alt-card:hover { border-color: #3B82F6; transform: translateX(5px); background: #253346; }
    .alt-img {
        width: 70px; height: 70px; object-fit: contain;
        background: #0F172A; border-radius: 10px; padding: 5px;
    }

    /* Buttons */
    .amazon-btn {
        background: linear-gradient(to bottom, #FFD814, #F7CA00);
        color: black !important; padding: 14px 35px; border-radius: 50px;
        text-decoration: none; font-weight: 800; display: inline-block; margin-top: 20px;
        box-shadow: 0 4px 10px rgba(247, 202, 0, 0.4); transition: transform 0.2s;
    }
    .amazon-btn:hover { transform: scale(1.05); }
    
    .stButton>button { 
        background: linear-gradient(90deg, #3B82F6, #2563EB); 
        color: white; border: none; padding: 15px; font-weight: bold; border-radius: 12px;
    }
    .stButton>button:hover { box-shadow: 0 5px 15px rgba(37, 99, 235, 0.4); }

    /* Text */
    .price-text { color: #FBBF24; font-weight: 900; font-size: 2.2em; letter-spacing: -1px; }
    .match-badge { background: #172554; color: #60A5FA; padding: 4px 8px; border-radius: 6px; font-size: 0.8em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("💎 TechChoose")
    st.caption("Ultimate Edition 2025")
    st.write("---")
    
    os_choice = st.selectbox("📱 Ecosystem:", ["Any", "iOS (Apple)", "Android"])
    
    st.write("")
    lifestyle = st.selectbox("👤 Persona Mode:", [
        "🎮 Hardcore Gamer", "📸 Content Creator", 
        "💼 Business / Work", "💰 Student / Budget Saver", "🛠️ Custom"
    ])

    # 🔥 NEW FEATURE: BUDGET SLIDER 🔥
    st.write("")
    budget = st.slider("💰 Max Budget ($):", 300, 2000, 2000, step=50)
    
    # Logic Weights
    p, c, b, v = 5, 5, 5, 5
    if lifestyle == "🎮 Hardcore Gamer": p,c,b,v = 10,3,8,5
    elif lifestyle == "📸 Content Creator": p,c,b,v = 7,10,8,5
    elif lifestyle == "💼 Business / Work": p,c,b,v = 8,6,9,6
    elif lifestyle == "💰 Student / Budget Saver": p,c,b,v = 5,5,7,10
    else: 
        st.divider()
        def score(l): return {"Ignore":1, "Nice":5, "Imp.":8, "Max":10}[l]
        p = score(st.select_slider("Speed", ["Ignore","Nice","Imp.","Max"],"Imp."))
        c = score(st.select_slider("Camera", ["Ignore","Nice","Imp.","Max"],"Imp."))
        b = score(st.select_slider("Battery", ["Ignore","Nice","Imp.","Max"],"Nice"))
        v = score(st.select_slider("Price", ["Ignore","Nice","Imp.","Max"],"Nice"))

    st.divider()
    st.button("🔥 FIND MY MATCH")

# --- 5. FUNCTIONS ---
def get_img_tag(url, size="100px", class_name=""):
    if pd.isna(url) or str(url).strip() == "" or str(url) == "nan":
        return f'<div style="width:{size}; height:{size}; display:flex; align-items:center; justify-content:center; background:#1E293B; border-radius:12px; font-size:2em; margin:0 auto;">📱</div>'
    return f'<img src="{url}" class="{class_name}">'

def generate_verdict(row, mode):
    if "Gamer" in mode: return f"🚀 <b>Gaming Beast:</b> With a performance score of {row['performance']}/10, the {row['name']} handles AAA games with ease."
    elif "Creator" in mode: return f"📸 <b>Pro Camera:</b> Capture cinematic 8K video and stunning portraits with its {row['camera']}/10 rated system."
    elif "Student" in mode: return f"💰 <b>Best Value:</b> Get premium features without breaking the bank. The smart choice for students."
    else: return f"✨ <b>Perfect Balance:</b> The ultimate all-rounder that excels in speed, battery, and daily reliability."

# --- 6. MAIN APP ---
df = load_data()

if not df.empty:
    # 1. Filter OS
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']
    
    # 2. Filter Budget (Feature ใหม่!)
    df = df[df['price'] <= budget]

    # 3. Calculate Score
    df['score'] = (df['performance']*p) + (df['camera']*c) + (df['battery']*b) + (df['value']*v)
    max_score = (10*p) + (10*c) + (10*b) + (10*v)
    df['match'] = (df['score'] / max_score) * 100
    df = df.sort_values(by='match', ascending=False).reset_index(drop=True)

    if len(df) > 0:
        winner = df.iloc[0]
        c1, c2 = st.columns([1.2, 1], gap="large")

        # --- WINNER SECTION ---
        with c1:
            st.markdown(f"""
            <div class='winner-card'>
                <div style='text-align:center; margin-bottom:15px;'>
                    <span style='background:#F59E0B; color:black; padding:6px 16px; border-radius:20px; font-weight:800; text-transform:uppercase; letter-spacing:1px; font-size:0.8em;'>
                        🏆 #1 Recommendation
                    </span>
                </div>
                <h1 style='margin:10px 0; font-size:2.5em;'>{winner['name']}</h1>
                {get_img_tag(winner['image'], "220px", "winner-img")}
                <div class='price-text'>${winner['price']:,}</div>
                <div style='background:rgba(255,255,255,0.05); padding:15px; border-radius:12px; margin-top:20px; text-align:left; font-size:0.95em; line-height:1.5;'>
                    {generate_verdict(winner, lifestyle)}
                </div>
                <a href="{winner['link']}" target="_blank" class="amazon-btn">
                    🛒 Check Price on Amazon
                </a>
            </div>
            """, unsafe_allow_html=True)

        # --- ALTERNATIVES SECTION ---
        with c2:
            st.markdown(f"<h3 style='margin-bottom:20px;'>🥈 Top Alternatives (Under ${budget:,})</h3>", unsafe_allow_html=True)
            
            # Show top 3 alternatives
            for i, row in df.iloc[1:4].iterrows():
                diff = winner['price'] - row['price']
                tag = ""
                if diff > 0: tag = f"<span style='color:#4ADE80; font-weight:bold; font-size:0.8em;'>Save ${diff:,}</span>"
                
                # HTML Block (Clean Indentation)
                html_card = f"""
<div class='alt-card'>
    {get_img_tag(row['image'], "70px", "alt-img")}
    <div style='flex-grow:1;'>
        <div style='font-weight:bold; font-size:1.1em;'>{row['name']}</div>
        <div style='color:#94A3B8; font-size:0.9em; margin-top:2px;'>Est. ${row['price']:,}</div>
        {tag}
    </div>
    <div style='text-align:right;'>
        <div class='match-badge'>{row['match']:.0f}% Match</div>
        <a href="{row['link']}" target="_blank" style='color:#F59E0B; text-decoration:none; font-size:0.85em; font-weight:bold; display:block; margin-top:5px;'>View ></a>
    </div>
</div>
"""
                st.markdown(html_card, unsafe_allow_html=True)
                
            if len(df) < 2:
                st.info("No other matches found in this budget. Try increasing your budget!")

    else:
        st.warning(f"No phones found under ${budget:,}. Please increase your budget.")
else:
    st.error("Please connect your Google Sheet correctly.")