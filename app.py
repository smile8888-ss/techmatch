import streamlit as st
import pandas as pd

# --- 1. CONFIG ---
st.set_page_config(
    page_title="TechChoose - Data Mode",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    # ลิงก์เดิมของพี่ (ไม่ต้องมีคอลัมน์ image ก็ทำงานได้)
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        return df
    except Exception:
        return pd.DataFrame()

# --- 3. CSS (Minimalist Dark) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp { background-color: #0F172A; color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    section[data-testid="stSidebar"] { background-color: #020617; border-right: 1px solid #1E293B; }
    section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }

    /* Winner Card - เน้นตัวหนังสือใหญ่ */
    .winner-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 2px solid #3B82F6; border-radius: 20px; padding: 40px;
        text-align: left; box-shadow: 0 0 30px rgba(59, 130, 246, 0.15);
        position: relative;
    }
    
    /* Alternatives Card */
    .alt-card {
        background: #1E293B; border: 1px solid #334155;
        padding: 20px; border-radius: 12px; margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .alt-card:hover { border-color: #3B82F6; transform: translateX(5px); }

    /* Button */
    .amazon-btn {
        background: linear-gradient(to bottom, #FFD814, #F7CA00);
        color: black !important; padding: 12px 30px; border-radius: 50px;
        text-decoration: none; font-weight: 800; display: inline-block; margin-top: 25px;
    }

    .price-big { color: #FBBF24; font-weight: 900; font-size: 3em; line-height: 1; }
    .score-badge { background: #172554; color: #60A5FA; padding: 5px 12px; border-radius: 8px; font-weight: bold; }
    
    /* Progress Bars Custom Colors */
    .stProgress > div > div > div > div { background: linear-gradient(90deg, #3B82F6 0%, #60A5FA 100%); }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("⚡ TechChoose")
    st.caption("AI Gadget Advisor")
    st.write("---")
    os_choice = st.selectbox("System", ["Any", "iOS", "Android"])
    st.write("")
    lifestyle = st.selectbox("Persona", ["🎮 Hardcore Gamer", "📸 Content Creator", "💼 Business / Work", "💰 Student / Budget Saver", "🛠️ Custom"])
    st.write("")
    budget = st.slider("Max Budget ($)", 300, 2000, 2000, step=50)

    # Weights Logic
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
    st.button("🔥 ANALYZE")

# --- 5. FUNCTIONS ---
def generate_verdict(row, mode):
    if "Gamer" in mode: return f"The <b>{row['name']}</b> is an absolute beast for gaming."
    elif "Creator" in mode: return f"Top-tier camera system on the <b>{row['name']}</b> for pro-level content."
    elif "Student" in mode: return f"<b>{row['name']}</b> gives you the best features for every dollar spent."
    else: return f"<b>{row['name']}</b> is the perfect all-rounder for your daily tasks."

# --- 6. MAIN LOGIC ---
df = load_data()

if not df.empty:
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']
    df = df[df['price'] <= budget]

    df['score'] = (df['performance']*p) + (df['camera']*c) + (df['battery']*b) + (df['value']*v)
    max_score = (10*p) + (10*c) + (10*b) + (10*v)
    df['match'] = (df['score'] / max_score) * 100
    df = df.sort_values(by='match', ascending=False).reset_index(drop=True)

    if len(df) > 0:
        winner = df.iloc[0]
        c1, c2 = st.columns([1.5, 1], gap="large")

        # --- WINNER (Left) ---
        with c1:
            st.markdown(f"""
            <div class='winner-card'>
                <span style='color:#F59E0B; font-weight:800; letter-spacing:1px; text-transform:uppercase;'>🏆 Top Recommendation</span>
                <h1 style='font-size:3.5em; margin:10px 0;'>{winner['name']}</h1>
                <div class='price-big'>${winner['price']:,}</div>
                <div style='margin-top:20px; font-size:1.1em; color:#CBD5E1;'>
                    {generate_verdict(winner, lifestyle)}
                </div>
                <a href="{winner['link']}" target="_blank" class="amazon-btn">Check Price on Amazon ></a>
            </div>
            """, unsafe_allow_html=True)
            
            # Stat Bars
            st.write("")
            st.caption("PERFORMANCE METRICS")
            c_p, c_c, c_b = st.columns(3)
            with c_p: st.progress(int(winner['performance']*10), f"Speed {winner['performance']}")
            with c_c: st.progress(int(winner['camera']*10), f"Cam {winner['camera']}")
            with c_b: st.progress(int(winner['battery']*10), f"Batt {winner['battery']}")

        # --- ALTERNATIVES (Right) ---
        with c2:
            st.markdown("### 🥈 Runner-ups")
            for i, row in df.iloc[1:5].iterrows():
                diff = winner['price'] - row['price']
                tag = f"<span style='color:#4ADE80; font-weight:bold; font-size:0.8em;'>Save ${diff:,}</span>" if diff > 0 else ""
                
                # HTML ชิดซ้าย แก้บั๊ก 100%
                st.markdown(f"""
<div class='alt-card'>
<div style='display:flex; justify-content:space-between; align-items:center;'>
<div>
<div style='font-size:1.2em; font-weight:bold;'>{i}. {row['name']}</div>
<div style='color:#94A3B8;'>Est. ${row['price']:,} {tag}</div>
</div>
<div style='text-align:right;'>
<div class='score-badge'>{row['match']:.0f}% Match</div>
<a href="{row['link']}" target="_blank" style='color:#F59E0B; font-size:0.8em; text-decoration:none; display:block; margin-top:5px;'>View ></a>
</div>
</div>
</div>
""", unsafe_allow_html=True)
                
    else:
        st.warning(f"No phones found under ${budget:,}")
else:
    st.error("Data Error")